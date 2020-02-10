import re

from SPARQLWrapper import SPARQLWrapper, JSON
from SPARQLWrapper.Wrapper import EndPointInternalError
from urllib.error import HTTPError
from wikidata.client import Client

from core.exceptions import WikidataSparQLError, WikidataResultError
from db import session
from db.models import Object, ObjectCategory, ObjectAlias
from .constants import SPARQL_BASE_URL, SPARQL_WIKIDATA_QUERY, USER_AGENT


class ObjectFactory:

    filters = []  # [{'property': 'P31', 'entity': 'Q3624078'}]
    language = 'en'
    category_name = None
    aliases = []

    def __init__(self, logger):
        if not self.filters or not self.category_name:
            raise NotImplementedError('Set filters and category name')
        self.logger = logger
        self.query = self.prepare_query()
        self.data = self.load_data()
        self.client = None

    def prepare_query(self):
        return SPARQL_WIKIDATA_QUERY.format(
            language=self.language,
            filters=self.generate_filter()
        )

    def generate_filter(self):
        wd_filters = ''
        for wd_filter in self.filters:
            wd_prop, wd_entity = wd_filter.values()
            wd_filters += f'    ?item wdt:{wd_prop} wd:{wd_entity}.\n'
        return wd_filters

    def load_data(self):
        try:
            sparql = SPARQLWrapper(SPARQL_BASE_URL, agent=USER_AGENT)
            self.logger.info('Get SparQL request from Wikidata')
            sparql.setQuery(self.query)
            sparql.setReturnFormat(JSON)
            results = sparql.query().convert()
        except (HTTPError, EndPointInternalError) as e:
            raise WikidataSparQLError

        try:
            return self.parse_wikidata_results(results)
        except KeyError:
            raise WikidataResultError

    def save_data_to_db(self):
        self.logger.info('Starting to save data')
        self.client = Client()
        category = ObjectCategory(name=self.category_name)
        session.add(category)
        session.commit()
        props = [self.client.get(alias, load=True) for alias in self.aliases]
        for obj in self.data:
            try:
                db_obj = Object(category_id=category.id, **obj)
                session.add(db_obj)
                session.commit()

                self.logger.info(f"Saved {obj['name']} to database")

                wikidata_obj = self.client.get(obj['wikidata_id'], load=True)
                self.save_aliases(wikidata_obj, props, db_obj)
            except Exception as e:
                self.logger.error(f'Can not save to db: {obj}. Error: {e}')
        return category.id

    def save_aliases(self, wikidata_obj, props, db_obj):
        try:
            for alias in wikidata_obj.attributes['aliases'][self.language]:
                self.logger.info(f"{alias['value']} found. Saving to db")
                if alias.get('value') and re.match('\w+', alias['value']):
                    session.add(ObjectAlias(name=alias['value'],
                                            object_id=db_obj.id))
        except Exception as e:
            self.logger.error(f'Unexpected error while loading aliases: {e}')
        else:
            session.commit()
        try:
            for prop in props:
                alias = wikidata_obj.get(prop)
                if alias:
                    self.logger.info(f"Alias {alias.label[self.language]} found."
                                f" Saving to db")
                    session.add(ObjectAlias(name=alias.label[self.language],
                                            object_id=db_obj.id))
        except Exception as e:
            self.logger.error(f'Unexpected error while loading aliases: {e}')
        else:
            session.commit()

    def parse_wikidata_results(self, results):
        return list(map(self._parse_obj, results['results']['bindings']))

    @staticmethod
    def _parse_obj(obj):
        return {
            'name': obj['itemLabel']['value'],
            'wikidata_id': obj['item']['value'].split('/')[-1]}

from .base_factory import ObjectFactory


class CountryFactory(ObjectFactory):
    category_name = 'Countries'
    filters = [{'property': 'P31', 'entity': 'Q3624078'}]


class PresidentOfUSAFactory(ObjectFactory):
    category_name = 'Presidents of USA'
    filters = [{'property': 'P39', 'entity': 'Q11696'}]
    aliases = ['P734']

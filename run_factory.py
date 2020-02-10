import logging

from factories.factories import CountryFactory
from db import session
from db.models import QuestionType

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

if __name__ == '__main__':
    factory = CountryFactory(logger)
    category_id = factory.save_data_to_db()
    session.add(QuestionType(
        text='What the country is this?',
        category_id=category_id,
        image_question_wikidata_prop='P18'))
    session.add(QuestionType(
        text='What the country is this?',
        category_id=category_id,
        image_question_wikidata_prop='P41'))
    session.add(QuestionType(
        text='What the country is this?',
        category_id=category_id,
        image_question_wikidata_prop='P242'))
    session.commit()


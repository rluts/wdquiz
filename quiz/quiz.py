from random import choice

from sqlalchemy.sql.expression import func, and_
from wikidata.client import Client

from db import session
from db.models import QuestionType, Object, ObjectCategory, ObjectAlias


class Quiz:
    def __init__(self, category_id):
        self.category = session.query(ObjectCategory).get(category_id)
        self.question_types = session.query(QuestionType).filter_by(
            category_id=category_id).all()
        self.client = Client()

    def get_random_type(self):
        return choice(self.question_types)

    def get_random_object(self):
        return next(iter(session.query(Object).filter(
            and_(Object.category_id == self.category.id,
                 Object.name != Object.wikidata_id)).order_by(
            func.random()).limit(1).all()), None)

    def img_ask(self):
        question_type = self.get_random_type()
        prop = self.client.get(question_type.image_question_wikidata_prop)
        obj = self.get_random_object()
        if not obj:
            return None, None
        wikidata_obj = self.client.get(obj.wikidata_id)
        img = wikidata_obj.get(prop)
        aliases = session.query(ObjectAlias).filter_by(
            object_id=obj.id).values('name')
        image_url = img.image_url if img else None
        return image_url, [obj.name] + [alias[0] for alias in aliases]

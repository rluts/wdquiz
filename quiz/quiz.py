import json
from random import choice

from sqlalchemy.sql.expression import func, and_, desc
from wikidata.client import Client

from db import session
from db.models import QuestionType, Object, ObjectAlias, Question
from .game import Game


class Quiz:
    def __init__(self, initiator, category_id, room_id, backend):
        self.room_id = room_id
        self.game = Game.get_game(room_id) or Game(
            initiator, category_id, room_id, backend)
        self.question_types = session.query(QuestionType).filter_by(
            category_id=category_id).all()
        self.client = Client()

    @classmethod
    def get_answers(cls, room_id=None, questions_id=None):
        if not any([room_id, questions_id]):
            raise ValueError('Room ID or Question ID is required')
        if room_id:
            obj = session.query(Question).filter_by(
                room_id=room_id).order_by(desc(Question.ask_date)).first()
        else:
            obj = session.query(Question).get(questions_id)
        if obj:
            return json.loads(obj.right_answers)

    def get_random_type(self):
        return choice(self.question_types)

    def get_random_object(self):
        return next(iter(session.query(Object).filter(
            and_(Object.category_id == self.game.category.id,
                 Object.name != Object.wikidata_id)).order_by(
            func.random()).limit(1).all()), None)

    @staticmethod
    def get_aliases(obj):
        aliases = session.query(ObjectAlias).filter_by(
            object_id=obj.id).values('name')
        return [alias[0] for alias in aliases]

    def get_answer_list(self, obj):
        answers = self.get_aliases(obj)
        answers.insert(0, obj.name)
        answers_json = json.dumps(answers)
        question = Question(
            game_id=self.game.game_db_obj.id,
            room_id=self.game.game_db_obj.room_id,
            right_answers=answers_json)
        session.add(question)
        session.commit()
        return answers, question.id

    def get_image_url_from_object(self, obj, question_type):
        prop = self.client.get(question_type.image_question_wikidata_prop)
        wikidata_obj = self.client.get(obj.wikidata_id)
        img = wikidata_obj.get(prop)
        image_url = img.image_url if img else None
        return image_url

    @staticmethod
    def _format_result_image_type(image_url, answer_list, question_id):
        return

    def ask_image_type(self):
        question_type = self.get_random_type()
        obj = self.get_random_object()
        if not obj:
            return None, None
        image_url = self.get_image_url_from_object(obj, question_type)
        answer_list, question_id = self.get_answer_list(obj)
        return image_url, answer_list, question_id

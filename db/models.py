from datetime import datetime

import sqlalchemy as db
from sqlalchemy.orm import relationship

from . import Base
from .utils import get_expired_datetime


class User(Base):
    __tablename__ = 'users'

    id = db.Column(db.BIGINT, primary_key=True)
    external_id = db.Column(db.BIGINT, index=True)
    backend = db.Column(db.String, index=True)
    created_games = relationship(
        'Game', foreign_keys='Game.initiator_id', back_populates='initiator')
    participants_games = relationship(
        'Game', foreign_keys='Game.participant_id',
        back_populates='participant')
    answers = relationship('Answer', back_populates='user')
    questions = relationship('Question', back_populates='associated_user')
    is_superuser = db.Column(db.Boolean, default=False)


class Question(Base):
    __tablename__ = 'questions'

    id = db.Column(db.BIGINT, primary_key=True)
    game_id = db.Column(db.BIGINT, db.ForeignKey('games.id'))
    room_id = db.Column(db.BIGINT)
    ask_date = db.Column(db.DateTime, default=datetime.now, index=True)
    right_answers = db.Column(db.JSON)
    associated_user_id = db.Column(db.BIGINT, db.ForeignKey('users.id'),
                                   nullable=True)
    answers = relationship('Answer', back_populates='question')
    game = relationship('Game', back_populates='questions')
    associated_user = relationship('User', back_populates='questions')


class Answer(Base):
    __tablename__ = 'answers'

    id = db.Column(db.BIGINT, primary_key=True)
    question_id = db.Column(db.BIGINT, db.ForeignKey('questions.id'))
    user_id = db.Column(db.BIGINT, db.ForeignKey('users.id'))
    question = relationship('Question', back_populates='answers')
    user = relationship('User', back_populates='answers')


class Game(Base):
    __tablename__ = 'games'

    id = db.Column(db.BIGINT, primary_key=True)
    initiator_id = db.Column(db.BIGINT, db.ForeignKey('users.id'))
    participant_id = db.Column(db.BIGINT, db.ForeignKey('users.id'),
                               nullable=True)
    category_id = db.Column(db.BIGINT, db.ForeignKey('object_categories.id'))
    room_id = db.Column(db.BIGINT, index=True)
    backend = db.Column(db.String, index=True)
    created_time = db.Column(db.DateTime, default=datetime.now)
    started = db.Column(db.Boolean, default=False)
    finished = db.Column(db.Boolean, default=False)
    start_time = db.Column(db.DateTime, nullable=True)
    end_time = db.Column(db.DateTime, nullable=True)

    initiator = relationship(
        'User', foreign_keys='Game.initiator_id',
        back_populates='created_games')
    participant = relationship('User', foreign_keys='Game.participant_id',
                               back_populates='participants_games')
    questions = relationship('Question', back_populates='game')
    category = relationship('ObjectCategory', back_populates='games')


class Object(Base):
    __tablename__ = 'objects'

    id = db.Column(db.BIGINT, primary_key=True)
    name = db.Column(db.String)
    wikidata_id = db.Column(db.String)
    category_id = db.Column(db.BIGINT, db.ForeignKey('object_categories.id'))
    aliases = relationship('ObjectAlias', back_populates='object')
    category = relationship('ObjectCategory', back_populates='objects')

    __table_args__ = (db.UniqueConstraint('category_id', 'wikidata_id'),
                      db.UniqueConstraint('category_id', 'name'))


class ObjectCategory(Base):
    __tablename__ = 'object_categories'

    id = db.Column(db.BIGINT, primary_key=True)
    wikidata_parent_entity = db.Column(db.String, nullable=True)
    name = db.Column(db.String)

    objects = relationship('Object', back_populates='category')
    question_types = relationship('QuestionType', back_populates='category')
    games = relationship('Game', back_populates='category')


class ObjectAlias(Base):
    __tablename__ = 'object_aliases'

    id = db.Column(db.BIGINT, primary_key=True)
    name = db.Column(db.String)
    object_id = db.Column(db.BIGINT, db.ForeignKey('objects.id'))

    object = relationship('Object', back_populates='aliases')


class QuestionType(Base):
    __tablename__ = 'question_types'

    id = db.Column(db.BIGINT, primary_key=True)
    text = db.Column(db.String)
    category_id = db.Column(db.BIGINT, db.ForeignKey('object_categories.id'))
    text_question_wikidata_prop = db.Column(db.String, nullable=True)
    image_question_wikidata_prop = db.Column(db.String, nullable=True)
    sound_question_wikidata_prop = db.Column(db.String, nullable=True)
    coords_question_wikidata_prop = db.Column(db.String, nullable=True)
    is_question_in_child = db.Column(db.String, nullable=True)
    child_prop = db.Column(db.String, nullable=True)

    category = relationship('ObjectCategory', back_populates='question_types')

    def __init__(self, text, category_id, text_question_wikidata_prop=None,
                 image_question_wikidata_prop=None,
                 sound_question_wikidata_prop=None,
                 coords_question_wikidata_prop=None, is_question_in_child=None,
                 child_prop=None):
        if not any([text_question_wikidata_prop, image_question_wikidata_prop,
                    sound_question_wikidata_prop,
                    coords_question_wikidata_prop]):
            raise ValueError('Some of wikidata props must be set')
        self.text = text
        self.category_id = category_id
        self.text_question_wikidata_prop = text_question_wikidata_prop
        self.image_question_wikidata_prop = image_question_wikidata_prop
        self.sound_question_wikidata_prop = sound_question_wikidata_prop
        self.is_question_in_child = is_question_in_child
        self.child_prop = child_prop


# class QuestionCache(Base):
#     __tablename = 'question_cache'
#     expired = db.Column(db.DateTime, default=get_expired_datetime)
#     # question_type_is
# TODO: add question cache


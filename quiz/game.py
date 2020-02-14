from datetime import datetime, timedelta

from sqlalchemy.sql.expression import false

from core.exceptions import BackendDoesNotExist
from db import session
from db.models import Game as GameModel, ObjectCategory, User
from backends import Backends


class Game:

    def __init__(self, initiator, category_id, room_id, backend,
                 game_db_obj=None):
        if backend not in Backends.values():
            raise BackendDoesNotExist
        self.category = session.query(ObjectCategory).get(category_id)
        self.participant = None
        self.backend = backend
        self.started = False
        self.started_time = None
        self.initiator = self.get_or_create_user(initiator)
        self.game_db_obj = game_db_obj or GameModel(
            category_id=category_id,
            backend=backend,
            room_id=room_id,
            initiator_id=self.initiator.id)
        session.add(self.game_db_obj)
        session.commit()

    @classmethod
    def get_game(cls, room_id):
        game_db_obj = session.query(GameModel).filter(
            GameModel.room_id == room_id,
            GameModel.created_time < datetime.now() - timedelta(hours=1),
            GameModel.finished == false()
        ).first()
        if game_db_obj:
            return cls(game_db_obj.initiator_id, game_db_obj.category_id,
                       game_db_obj.room_id, game_db_obj.backend, game_db_obj)

    def get_or_create_user(self, external_id):
        user = session.query(User).filter_by(external_id=external_id,
                                             backend=self.backend).first()
        if not user:
            user = User(external_id=external_id, backend=self.backend)
            session.add(user)
            session.commit()
        return user

    def join(self, participant):
        self.game_db_obj.participant = self.get_or_create_user(participant)
        self.start_game()
        session.commit()

    def _setattr(self, key, value):
        setattr(self, key, value)
        setattr(self.game_db_obj, key, value)

    def start_game(self):
        self._setattr('started', True)
        self._setattr('start_time', datetime.now())

    def finish_game(self):
        self._setattr('finished', True)
        self._setattr('end_time', datetime.now())

    def is_multiple_game(self):
        return bool(self.participant)


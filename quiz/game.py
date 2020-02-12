from datetime import datetime

from core.exceptions import BackendDoesNotExist
from db import session
from db.models import Game as GameModel, ObjectCategory, User
from backends import Backends


class Game:

    def __init__(self, initiator, category_id, room_id, backend):
        if backend not in Backends.values():
            raise BackendDoesNotExist
        self.category = session.query(ObjectCategory).get(category_id)
        self.participant = None
        self.backend = backend
        self.started = False
        self.started_time = None
        self.initiator = self.get_or_create_user(initiator)
        self.game = GameModel(
            category_id=category_id,
            backend=backend,
            room_id=room_id,
            initiator_id=self.initiator.id)
        session.add(self.game)
        session.commit()

    def get_or_create_user(self, external_id):
        user = session.query(User).filter_by(external_id=external_id,
                                             backend=self.backend).first()
        if not user:
            user = User(external_id=external_id, backend=self.backend)
            session.add(user)
            session.commit()
        return user

    def join(self, participant):
        self.game.participant = self.get_or_create_user(participant)
        self.start_game()
        session.commit()

    def _setattr(self, key, value):
        setattr(self, key, value)
        setattr(self.game, key, value)

    def start_game(self):
        self._setattr('started', True)
        self._setattr('start_time', datetime.now())

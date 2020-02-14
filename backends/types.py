import enum


class WDQuizEnum(enum.Enum):
    @classmethod
    def values(cls):
        return [x.value for x in cls]


class Backends(WDQuizEnum):
    telegram = 'telegram'
    api = 'api'

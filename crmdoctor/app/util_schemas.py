from enum import Enum

from ninja import Schema


class Petrovich(Schema):
    first_name: str
    middle_name: str
    last_name: str


class Padej(str, Enum):
    GENITIVE = 'родительный'
    DATIVE = 'дательный'
    ACCUSATIVE = 'винительный'
    INSTRUMENTAL = 'творительный'
    PREPOSITIONAL = 'предложный'


class MyGender(str, Enum):
    MALE = 'он'
    FEMALE = 'она'
    ANDROGYNOUS = 'оно'

from enum import Enum


class CharacterStatus(str, Enum):
    ALIVE = 'Alive'
    DEAD = 'Dead'
    UNKNOWN = 'Unknown'

class CharacterGender(str, Enum):
    MALE = 'Male'
    FEMALE = 'Female'
    GENDERLESS = 'Genderless'
    UNKNOWN = 'Unknown'
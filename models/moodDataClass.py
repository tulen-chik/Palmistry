from dataclasses import dataclass

from enum import Enum

class mood(Enum):
    EXTRO = 1
    INTRO = 2
    AMBI = 3
    HUE = 4


@dataclass
class Mood_dataclass:
    mood_id: int
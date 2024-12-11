from dataclasses import dataclass

@dataclass
class User_dataclass:
    id: int
    id_telegram: str
    mood_id: int

    latitude: float
    longitude: float
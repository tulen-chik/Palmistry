from dataclasses import dataclass

@dataclass
class Place_dataclass:
    id: int
    id_user: int
    name: str
    avatar: str
    points: int
    review: str

    latitude: float
    longitude: float
    category: str
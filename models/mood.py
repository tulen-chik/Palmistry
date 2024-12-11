from sqlalchemy import Column, Integer, String
from config import Base

class Mood(Base):
    __tablename__ = 'mood'

    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False, unique=True)

    def __repr__(self):
        return f'<Mood {self.name}>'
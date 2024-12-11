from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from config import Base

class TypePlace(Base):
    __tablename__ = 'type_place'

    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False, unique=True)
    mood_id = Column(Integer, ForeignKey('mood.id'), nullable=True)  # Внешний ключ на таблицу mood

    # Связь с моделью Mood
    mood = relationship('Mood', backref='type_places', lazy=True)

    def __repr__(self):
        return f'<TypePlace {self.name}>'
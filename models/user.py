from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from config import Base

class Users(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    id_telegram = Column(Integer, nullable=False, unique=True)
    mood_id = Column(Integer, ForeignKey('mood.id'), nullable=True)  # Внешний ключ на таблицу mood

    # Связь с моделью Mood
    mood = relationship('Mood', backref='users', lazy=True)

    def __repr__(self):
        return f'<Users {self.id_telegram}>'
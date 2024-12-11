from sqlalchemy import Column, Integer, String, ForeignKey, Boolean
from sqlalchemy.orm import relationship
from config import Base

class Place(Base):
    __tablename__ = 'place'

    id = Column(Integer, primary_key=True)
    id_user = Column(Integer, ForeignKey('users.id'), nullable=False)
    name = Column(String(100), nullable=False)
    avatar = Column(String(200), nullable=True)
    points = Column(Integer, nullable=True)
    review = Column(Boolean, nullable=True)

    # Связь с моделью Users
    user = relationship('Users', backref='places', lazy=True)

    def __repr__(self):
        return f'<Place {self.name}>'
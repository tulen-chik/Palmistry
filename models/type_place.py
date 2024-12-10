from config import Base, db

class TypePlace(Base):
    __tablename__ = 'type_place'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    mood_id = db.Column(db.Integer, db.ForeignKey('mood.id'), nullable=True)  # Внешний ключ на таблицу mood

    # Связь с моделью Mood
    mood = db.relationship('Mood', backref='type_places', lazy=True)

    def __repr__(self):
        return f'<TypePlace {self.name}>'
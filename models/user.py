from config import Base

class Users(Base):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    id_telegram = db.Column(db.String(100), nullable=False)
    mood_id = db.Column(db.Integer, db.ForeignKey('mood.id'), nullable=True)  # Внешний ключ на таблицу mood

    # Relationship to Place
    places = db.relationship('Place', backref='user', lazy=True)

    # Связь с моделью Mood
    mood = db.relationship('Mood', backref='users', lazy=True)

    def __repr__(self):
        return f'<Users {self.id_telegram}>'
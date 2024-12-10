from cofig import Base

class Place(Base):
    __tablename__ = 'place'

    id = db.Column(db.Integer, primary_key=True)
    id_user = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    name = db.Column(db.String(100), nullable=False)
    avatar = db.Column(db.String(200), nullable=True)
    points = db.Column(db.Integer, nullable=True)
    review = db.Column(db.String(255), nullable=True)

    def __repr__(self):
        return f'<Place {self.name}>'
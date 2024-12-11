from config import Session
from models.place import Place

def add_place(id_user, name, avatar=None, points=None, review=None):
    session = Session()
    new_place = Place(id_user=id_user, name=name, avatar=avatar, points=points, review=review)
    session.add(new_place)
    session.commit()
    session.close()

def get_place(place_id):
    session = Session()
    place = session.query(Place).filter_by(id=place_id).first()
    session.close()
    return place

def update_place(place_id, name=None, avatar=None, points=None, review=None):
    session = Session()
    place = session.query(Place).filter_by(id=place_id).first()
    if place:
        if name is not None:
            place.name = name
        if avatar is not None:
            place.avatar = avatar
        if points is not None:
            place.points = points
        if review is not None:
            place.review = review
        session.commit()
    session.close()

def delete_place(place_id):
    session = Session()
    place = session.query(Place).filter_by(id=place_id).first()
    if place:
        session.delete(place)
        session.commit()
    session.close()
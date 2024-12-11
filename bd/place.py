from config import Session
from models.place import Place
from bd.user import get_user

def add_place(id_user, name, avatar=None, points=None, review=None):
    session = Session()
    new_place = Place(id_user=get_user(id_user).id, name=name, avatar=avatar, points=points, review=review)
    session.add(new_place)
    session.commit()
    session.close()

def get_place(place_id):
    session = Session()
    place = session.query(Place).filter_by(id=place_id).first()
    session.close()
    return place


from sqlalchemy import func


def get_all_places(sort_by_visits=False, sort_by_points=False):
    session = Session()

    # Начальный запрос к таблице Place с агрегацией для подсчета визитов и суммированием очков
    query = session.query(
        Place.name,
        func.count(Place.id).label('count'),
        func.sum(Place.points).label('total_points')
    ).group_by(Place.name)

    # Сортировка по количеству мест или очков
    if sort_by_visits:
        query = query.order_by(func.count(Place.id).desc())
    elif sort_by_points:
        query = query.order_by(func.sum(Place.points).desc())

    results = query.all()
    session.close()

    # Возвращаем только необходимые поля
    return [(name, count if sort_by_visits else total_points) for name, count, total_points in results]

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
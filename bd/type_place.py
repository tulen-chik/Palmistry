from config import Session
from models.type_place import TypePlace

def add_type_place(name, mood_id=None):
    """Добавляет новый тип места в базу данных."""
    session = Session()
    new_type_place = TypePlace(name=name, mood_id=mood_id)
    session.add(new_type_place)
    session.commit()
    session.close()

def get_type_place(type_place_id):
    """Получает тип места по его идентификатору."""
    session = Session()
    type_place = session.query(TypePlace).filter_by(id=type_place_id).first()
    session.close()
    return type_place

def get_all_type_places(name=None):
    """Получает все типы мест, с возможностью фильтрации по имени."""
    session = Session()
    if name:
        type_places = session.query(TypePlace).filter(TypePlace.name.ilike(f'%{name}%')).all()  # Фильтрация по имени
    else:
        type_places = session.query(TypePlace).all()  # Получаем все записи, если имя не передано
    session.close()
    return type_places

def update_type_place(type_place_id, name=None, mood_id=None):
    """Обновляет существующий тип места."""
    session = Session()
    type_place = session.query(TypePlace).filter_by(id=type_place_id).first()
    if type_place:
        if name is not None:
            type_place.name = name
        if mood_id is not None:
            type_place.mood_id = mood_id
        session.commit()
    session.close()

def delete_type_place(type_place_id):
    """Удаляет тип места по его идентификатору."""
    session = Session()
    type_place = session.query(TypePlace).filter_by(id=type_place_id).first()
    if type_place:
        session.delete(type_place)
        session.commit()
    session.close()
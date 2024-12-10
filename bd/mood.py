from config import Session
from models.mood import Mood

def add_mood(name):
    """Добавляет новую запись о настроении в базу данных."""
    session = Session()
    new_mood = Mood(name=name)
    session.add(new_mood)
    session.commit()
    session.close()


def get_mood(mood_id=None, name=None):
    """Получает настроение по его идентификатору или имени."""
    session = Session()
    try:
        if mood_id is not None:
            mood = session.query(Mood).filter_by(id=mood_id).first()
        elif name is not None:
            mood = session.query(Mood).filter_by(name=name).first()
        else:
            mood = None  # Если ни id, ни name не переданы
    finally:
        session.close()

    return mood

def get_all_moods():
    """Получает все записи о настроениях."""
    session = Session()
    moods = session.query(Mood).all()
    session.close()
    return moods

def update_mood(mood_id, name=None):
    """Обновляет существующую запись о настроении."""
    session = Session()
    mood = session.query(Mood).filter_by(id=mood_id).first()
    if mood and name is not None:
        mood.name = name
        session.commit()
    session.close()

def delete_mood(mood_id):
    """Удаляет настроение по его идентификатору."""
    session = Session()
    mood = session.query(Mood).filter_by(id=mood_id).first()
    if mood:
        session.delete(mood)
        session.commit()
    session.close()
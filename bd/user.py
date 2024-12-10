from config import Session
from models.users import Users

def add_user(id_telegram, mood_id=None):
    """Добавляет нового пользователя в базу данных с опциональным настроением."""
    session = Session()
    new_user = Users(id_telegram=id_telegram, mood_id=mood_id)
    session.add(new_user)
    session.commit()
    session.close()

def get_user(id_telegram):
    """Получает пользователя по его идентификатору."""
    session = Session()
    user = session.query(Users).filter_by(id_telegram=id_telegram).first()
    session.close()
    return user

def update_user(id_telegram, new_mood_id=None):
    """Обновляет существующего пользователя."""
    session = Session()
    user = session.query(Users).filter_by(id_telegram=id_telegram).first()
    if user:
        if new_mood_id is not None:
            user.mood_id = new_mood_id
        session.commit()
    session.close()

def delete_user(id_telegram):
    """Удаляет пользователя по его идентификатору."""
    session = Session()
    user = session.query(Users).filter_by(id_telegram=id_telegram).first()
    if user:
        session.delete(user)
        session.commit()
    session.close()
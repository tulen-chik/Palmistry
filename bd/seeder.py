from config import Session
from models.type_place import TypePlace
from models.mood import Mood  # Импортируем модель Mood

# Определяем массивы
ambiverts = [
    'lodging', 'restaurant', 'food', 'point_of_interest', 'establishment',
    'finance', 'store', 'health', 'cafe', 'gym', 'hospital', 'bank', 'pharmacy',
    'supermarket', 'shopping_mall', 'pet_store', 'laundry', 'car_repair', 'gas_station'
]

introverts = [
    'locality', 'political', 'tourist_attraction',
    'school', 'local_government_office', 'library', 'museum', 'art_gallery',
    'university', 'church', 'cemetery', 'aquarium', 'zoo'
]

extraverts = [
    'casino', 'bar', 'night_club',
    'electronics_store', 'jewelry_store', 'amusement_park', 'bowling_alley',
    'movie_theater', 'stadium'
]


def seed_moods():
    """Добавляет записи о настроениях в базу данных."""
    session = Session()

    # Добавляем записи о настроениях
    moods = ['ambivert', 'introvert', 'extravert']
    for mood_name in moods:
        mood = Mood(name=mood_name)
        session.add(mood)

    session.commit()  # Сохраняем изменения
    session.close()  # Закрываем сессию


def seed_type_places():
    session = Session()

    # Получаем идентификаторы настроений
    ambivert_mood = session.query(Mood).filter_by(name='ambivert').first()
    introvert_mood = session.query(Mood).filter_by(name='introvert').first()
    extravert_mood = session.query(Mood).filter_by(name='extravert').first()

    # Добавляем ambiverts
    for name in ambiverts:
        type_place = TypePlace(name=name, mood_id=ambivert_mood.id)
        session.add(type_place)

    # Добавляем introverts
    for name in introverts:
        type_place = TypePlace(name=name, mood_id=introvert_mood.id)
        session.add(type_place)

    # Добавляем extraverts
    for name in extraverts:
        type_place = TypePlace(name=name, mood_id=extravert_mood.id)
        session.add(type_place)

    session.commit()  # Сохраняем изменения
    session.close()  # Закрываем сессию
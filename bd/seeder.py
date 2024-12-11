from config import Session
from models.type_place import TypePlace
from models.mood import Mood

# Определяем массивы
mood_places = {
    'Интроверт': [
        'locality', 'political', 'tourist_attraction',
        'school', 'local_government_office', 'library', 'museum', 'art_gallery',
        'university', 'church', 'cemetery', 'aquarium', 'zoo'
    ],
    'Амбиверт': [
        'lodging', 'restaurant', 'food', 'point_of_interest', 'establishment',
        'finance', 'store', 'health', 'cafe', 'gym', 'hospital', 'bank', 'pharmacy',
        'supermarket', 'shopping_mall', 'pet_store', 'laundry', 'car_repair', 'gas_station'
    ],
    'Экстраверт': [
        'casino', 'bar', 'night_club',
        'electronics_store', 'jewelry_store', 'amusement_park', 'bowling_alley',
        'movie_theater', 'stadium'
    ]
}

def seed_moods():
    """Добавляет записи о настроениях в базу данных."""
    with Session() as session:
        moods = ['Интроверт', 'Амбиверт', 'Экстраверт']
        for mood_name in moods:
            if not session.query(Mood).filter_by(name=mood_name).first():  # Проверяем, существует ли уже
                mood = Mood(name=mood_name)
                session.add(mood)
        session.commit()  # Сохраняем изменения

def seed_type_places():
    """Добавляет типы мест в базу данных в зависимости от настроений."""
    with Session() as session:
        for mood_name, places in mood_places.items():
            mood = session.query(Mood).filter_by(name=mood_name).first()
            if mood:  # Проверяем, существует ли настроение
                for place_name in places:
                    # Проверяем, существует ли тип места с таким именем
                    if not session.query(TypePlace).filter_by(name=place_name).first():
                        type_place = TypePlace(name=place_name, mood_id=mood.id)
                        session.add(type_place)
        session.commit()  # Сохраняем изменения
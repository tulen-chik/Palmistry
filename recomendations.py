from geopy.distance import geodesic
import bd.mood
import bd.place
import bd.type_place
import bd.user
from models.placeDataClass import Place_dataclass
from models.userDataClass import User_dataclass
from models.moodDataClass import mood, Mood_dataclass
from typing import List, Generic
from AI import AI
import services 
import bd
import services.google_service
from config import user_profiles
from config import Base, engine, bot, user_profiles
from bd.seeder import seed_moods, seed_type_places
from handlers.profile_handler import register_profile_handlers 
import logging

category_resolving_map = {
    'locality': 'Парки',
    'political': 'Туристические агентства',
    'tourist_attraction': 'Парки',
    'school': 'Квест-комнаты',
    'local_government_office': "Библиотека",
    'library': "Библиотека",
    'museum': 'Музеи',
    'art_gallery': 'Пикниковые зоны',
    'university': "Киберспортивные арены",
    'church': "Квест-комнаты",
    'cemetery': "Книжные клубы",
    'aquarium': 'Спортивные клубы',
    'zoo': 'Ночные клубы',
    'lodging': "Пикниковые зоны",
    'restaurant': "Кафе",
    'food': 'Кафе',
    "point_of_interest": "Мастер-классы",
    'establishment': 'Игровые кафе',
    'finance': "Студии йоги",
    'store': 'Книжные магазины',
    'health': "Киберспортивные арены",
    'cafe': "Кафе",
    'gym': "Спортивные клубы",
    'hospital': "Киберспортивные турниры",
    'bank': "Волонтерские организации",
    'pharmacy': "Танцевальные студии",
    'supermarket': "Киберспортивные турниры",
    'shopping_mall': "Мастерские",
    'pet_store': "Мастер-классы",
    'laundry': "Концертные залы",
    'car_repair': "Киберспортивные турниры",
    'gas_station': "Волонтерские организации",
    "casino": "Ночные клубы",
    "bar": "Ночные клубы",
    'night_club': "Ночные клубы",
    "electronics_store": "Книжные клубы",
    'jewelry_store': "Танцевальные студии",
    "amusement_park": "Парк",
    'bowling_alley': "Игровые кафе",
    'movie_theater': "Киберспортивные арены",
    'stadium': "Спортивные клубы"
}

label_map = {
    "Ночные клубы": 0,
    "Спортивные клубы": 1,
    "Киберспортивные арены": 2,
    "Кафе": 3,
    "Танцевальные студии": 4,
    "Туристические агентства": 5,
    "Волонтерские организации": 6,
    "Библиотеки": 7,
    "Книжные магазины": 8,
    "Игровые кафе": 9,
    "Мастерские": 10,
    "Парки": 11,
    "Студии йоги": 12,
    "Музеи": 13,
    "Квест-комнаты": 14,
    "Книжные клубы": 15,
    "Концертные залы": 16,
    "Киберспортивные турниры": 17,
    "Пикниковые зоны": 18,
    "Мастер-классы": 19
}

# Пример данных о местах
#places = pd.DataFrame({
#    'name': ['Place A', 'Place B', 'Place C'],
#    'latitude': [53.9, 53.91, 53.92],
#    'longitude': [27.56, 27.57, 27.58],
#    'category': ['Ночные клубы', 'Спортивные клубы', 'Киберспортивные арены',
#                'Кафе', 'Танцевальные студии', 'Туристические агентства',
#                'Волонтерские организации', 'Библиотеки', 'Книжные магазины','Игровые кафе',
#                'Мастерские', 'Парки', 'Студии йоги', 'Музеи',
#                'Квест-комнаты', 'Спортивные клубы', 'Книжные клубы',
#                'Концертные залы', 'Киберспортивные турниры', 'Пикниковые зоны', 'Мастер-классы'],
#    'points': [4.5, 4.0, 3.5]  # Популярность места (например, рейтинг)
#})

# places = [Place_dataclass(id = 0, id_user = 0, name = "Place A" ,avatar = "Null", points = 4.5, review = "Yamal",
#     latitude= 53.9, longitude = 27.56, category="Ночные клубы"),
#     Place_dataclass(id = 0, id_user = 0, name = "Place B" ,avatar = "Null", points = 4.0, review = "Yamal",
#     latitude= 53.91, longitude = 27.57, category="Библиотеки"),
#     Place_dataclass(id = 0, id_user = 0, name = "Place C" ,avatar = "Null", points = 3.5, review = "Yamal",
#     latitude= 53.92, longitude = 27.58, category="Танцевальные студии")
#     ]

# Пример профиля пользователя
user_profile = User_dataclass(id = 0, id_telegram="SHpakelvka", mood_id=mood.INTRO,latitude=53.9,longitude=27.56)

def converterUser(id_telegram: int, lat: int, lon: int):
    user = bd.user.get_user(id_telegram)
    user_coverted = User_dataclass(id = user.id, id_telegram=user.id_telegram, mood_id=user.mood_id,latitude=lat,longitude=lon)
    return user_coverted

# Функция для расчета расстояния между пользователем и местом
def calculate_distance(user_location, place_location):
    return geodesic(user_location, place_location).kilometers

# Функция для расчета баллов
def calculate_score(distance, popularity, category_match,payed, mood_match):
    score = 0
    if mood:
        score += 50
    if payed:
        score +=50
    if category_match:
        score += 50  # Баллы за соответствие категории
    score += (5 - distance) * 10  # Баллы за близость (чем ближе, тем больше баллов)
    score += popularity * 10  # Баллы за популярность
    return score

# Функция для рекомендации мест
def recommend_places(user: User_dataclass, places, interested_categories: List[str]):
    user_location = (user.latitude, user.longitude)
    #users_mood = user.mood_id TODO добавить потдержку mood
    recommendations = []

    for place in places:
        place_location = (place['координаты']['lat'], place['координаты']['lat'])
        distance = calculate_distance(user_location, place_location)
        category_match = place['категория'] in interested_categories
        #mood_match = place.mood_id == users_mood
        score = calculate_score(distance, int(place['оценка']), category_match, False, False)
        recommendations.append((place, score))
    
    # Сортировка рекомендаций по баллам
    recommendations.sort(key=lambda x: x[1], reverse=True)
    return recommendations

# Example of usage
# if __name__ =="__main__":
#     # Получение рекомендаций
#     user = converterUser("511012132")
#     answer =  [AI.generateCategory("Хочу танцевать")]
#     recommendations = recommend_places(user_profile, places, answer)
#     for name, score in recommendations:
#         print(f"Place: {name}, Score: {score:.2f}")
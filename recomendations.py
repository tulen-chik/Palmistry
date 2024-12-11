import pandas as pd
from geopy.distance import geodesic
from models.placeDataClass import Place_dataclass
from models.userDataClass import User_dataclass
from models.moodDataClass import mood, Mood_dataclass
from typing import List, Generic
from AI import AI

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

places = [Place_dataclass(id = 0, id_user = 0, name = "Place A" ,avatar = "Null", points = 4.5, review = "Yamal",
    latitude= 53.9, longitude = 27.56, category="Ночные клубы"),
    Place_dataclass(id = 0, id_user = 0, name = "Place B" ,avatar = "Null", points = 4.0, review = "Yamal",
    latitude= 53.91, longitude = 27.57, category="Библиотеки"),
    Place_dataclass(id = 0, id_user = 0, name = "Place C" ,avatar = "Null", points = 3.5, review = "Yamal",
    latitude= 53.92, longitude = 27.58, category="Танцевальные студии")
    ]

# Пример профиля пользователя
user_profile = User_dataclass(id = 0, id_telegram="SHpakelvka", mood_id=mood.INTRO,latitude=53.9,longitude=27.56)

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
def recommend_places(user: User_dataclass, places: List[Place_dataclass], interested_categories: List[str]):
    user_location = (user.latitude, user.longitude)
    #users_mood = user.mood_id TODO добавить потдержку mood
    recommendations = []

    for place in places:
        place_location = (place.latitude, place.longitude)
        distance = calculate_distance(user_location, place_location)
        category_match = place.category in interested_categories
        #mood_match = place.mood_id == users_mood
        score = calculate_score(distance, place.points, category_match, False, False) # TODO category and mood check
        
        recommendations.append((place.name, score))
    
    # Сортировка рекомендаций по баллам
    recommendations.sort(key=lambda x: x[1], reverse=True)
    return recommendations

# Example of usage
if __name__ =="__main__":
    # Получение рекомендаций
    AI.initAI()
    answer =  [AI.generateCategory("Хочу танцевать")]
    recommendations = recommend_places(user_profile, places, answer)
    for name, score in recommendations:
        print(f"Place: {name}, Score: {score:.2f}")
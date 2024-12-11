import pandas as pd
from geopy.distance import geodesic

# Пример данных о местах
places = pd.DataFrame({
    'name': ['Place A', 'Place B', 'Place C'],
    'latitude': [53.9, 53.91, 53.92],
    'longitude': [27.56, 27.57, 27.58],
    'category': ['Ночные клубы', 'Спортивные клубы', 'Киберспортивные арены',
                'Кафе', 'Танцевальные студии', 'Туристические агентства',
                'Волонтерские организации', 'Библиотеки', 'Книжные магазины','Игровые кафе',
                'Мастерские', 'Парки', 'Студии йоги', 'Музеи',
                'Квест-комнаты', 'Спортивные клубы', 'Книжные клубы',
                'Концертные залы', 'Киберспортивные турниры', 'Пикниковые зоны', 'Мастер-классы'],
    'points': [4.5, 4.0, 3.5]  # Популярность места (например, рейтинг)
})

# Пример профиля пользователя
user_profile = {
    'latitude': 53.9,
    'longitude': 27.56,
    'preferred_categories': ['restaurant', 'cafe']
}

# Функция для расчета расстояния между пользователем и местом
def calculate_distance(user_location, place_location):
    return geodesic(user_location, place_location).kilometers

# Функция для расчета баллов
def calculate_score(distance, popularity, category_match,payed, mood):
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
def recommend_places(user_profile, places):
    user_location = (user_profile['latitude'], user_profile['longitude'])
    recommendations = []

    for _, place in places.iterrows():
        place_location = (place['latitude'], place['longitude'])
        distance = calculate_distance(user_location, place_location)
        category_match = place['category'] in user_profile['preferred_categories']
        score = calculate_score(distance, place['points'], category_match, False)
        
        recommendations.append((place['name'], score))
    
    # Сортировка рекомендаций по баллам
    recommendations.sort(key=lambda x: x[1], reverse=True)
    return recommendations

# Получение рекомендаций
recommendations = recommend_places(user_profile, places)
for name, score in recommendations:
    print(f"Place: {name}, Score: {score:.2f}")
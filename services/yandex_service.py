import requests
from config import YANDEX_API_KEY

def find_nearby_places(latitude, longitude, places_query):
    # Формируем URL для запроса к API Яндекс.Карт
    url = f"https://search-maps.yandex.ru/v1/?text={places_query}&ll={longitude},{latitude}&spn=0.1,0.1&results=5&apikey={YANDEX_API_KEY}"

    # Отправляем GET-запрос
    response = requests.get(url)

    # Проверяем статус ответа
    if response.status_code == 200:
        data = response.json()
        places = []

        # Обрабатываем полученные данные
        for feature in data.get('features', []):
            name = feature['properties']['name']
            description = feature['properties'].get('description', 'Нет описания')
            url = feature['properties'].get('url', 'Нет ссылки')
            rating = feature['properties'].get('rating', 'Нет оценок')
            places.append({
                'name': name,
                'description': description,
                'url': url,
                'rating': rating
            })
        return places
    else:
        return []  # Возвращаем пустой список в случае ошибки
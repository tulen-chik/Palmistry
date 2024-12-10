import requests
import os
import json
from config import engine

def find_nearby_places(latitude, longitude, places_query):
    # Формируем URL для запроса к API Google Places
    url = f"https://maps.googleapis.com/maps/api/place/nearbysearch/json?location={latitude},{longitude}&type={places_query}&radius=5000&key={os.environ['GOOGLE_MAPS_KEY']}"

    # Отправляем GET-запрос
    response = requests.get(url)

    # Проверяем статус ответа
    if response.status_code == 200:
        data = response.json()
        places = []

        # Обрабатываем полученные данные
        for result in data.get('results', []):
            name = result['name']
            vicinity = result.get('vicinity', 'Нет описания')
            rating = result.get('rating', 'Нет оценок')
            avatar = json.loads(result.get('photos', 'Нет аватара')[0]).get('photo_reference')

            places.append({
                'название': name,
                'местонахождение': vicinity,
                'оценка': rating,
                'аватар': avatar,
            })

        return places
    else:
        return []# Возвращаем пустой список в случае ошибки

def get_place_image(place_name):
    return requests.get(f"https://maps.googleapis.com/maps/api/place/photo?maxwidth=800&photoreference={place_name}&key={os.environ['GOOGLE_MAPS_KEY']}")
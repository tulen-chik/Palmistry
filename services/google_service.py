import requests
import os
import json
from config import engine
import logging

def find_nearby_places(latitude, longitude, places_query, radius=5000):
    # Формируем URL для запроса к API Google Places
    url = f"https://maps.googleapis.com/maps/api/place/nearbysearch/json?location={latitude},{longitude}&language=ru-RU&type={places_query}&radius={radius}&key={os.environ['GOOGLE_MAPS_KEY']}"

    # Отправляем GET-запрос
    response = requests.get(url)

    # Проверяем статус ответа
    if response.status_code == 200:
        data = response.json()
        places = []

        # Обрабатываем полученные данные
        for result in data.get('results', [])[1:6]:
            logging.warning(result)
            name = result['name']
            vicinity = result.get('vicinity', 'Нет описания')
            rating = result.get('rating', 0)
            coordinates = result.get('geometry').get('location')
            category = result.get('types')
            if 'photos' in result and len(result['photos']) > 0:
                photo_reference = result['photos'][0].get('photo_reference', 'Нет photo_reference')
            else:
                photo_reference = 'Нет фото'
            places.append({
                'название': name,
                'местонахождение': vicinity,
                'оценка': rating,
                'аватар': photo_reference,
                'координаты': coordinates,
                'категория': category,
            })

        return places
    else:
        return []# Возвращаем пустой список в случае ошибки

def get_place_image(place_name):
    return requests.get(f"https://maps.googleapis.com/maps/api/place/photo?maxwidth=800&photoreference={place_name}&key={os.environ['GOOGLE_MAPS_KEY']}")
from handlers.place_handler import get_places, send_places
from config import user_profiles

def handle_location(message):
    user_id = message.chat.id
    # Извлечение координат из сообщения
    coordinates = message.location  # Используем message.location для получения координат

    # Обновление user_profiles с новыми координатами
    user_profiles[user_id]['coordinates'] = {
        'lat': coordinates.latitude,
        'lon': coordinates.longitude
    }

    # Получение мест на основе обновленных координат
    places = get_places(user_id, coordinates.latitude, coordinates.longitude)
    send_places(user_id, places)
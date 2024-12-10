from config import user_profiles, API_TOKEN, places_by_personality
from services.yandex_service import find_nearby_places
from services.user_service import update_favorite_places
import telebot

bot = telebot.TeleBot(API_TOKEN)


def get_places(user_id, latitude, longitude):
    personality = user_profiles[user_id]['personality']
    preferred_places = places_by_personality[personality]
    places_query = '|'.join(preferred_places)

    places = find_nearby_places(latitude, longitude, places_query)

    return places

def send_places(user_id, places):
    if places:
        for place in places:
            bot.send_message(user_id, f"Название: {place['name']}\n"
                                      f"Описание: {place['description']}\n"
                                      f"Ссылка: {place['url']}\n"
                                      f"Количество оценок: {place['rating']}")
            # Обновляем любимые места
            update_favorite_places(user_id, place['name'])
    else:
        bot.send_message(user_id, "К сожалению, я не нашел увеселительных заведений рядом.")
from config import user_profiles
from bd.type_place import get_all_type_places
from services.google_service import find_nearby_places
from services.user_service import update_favorite_places
import telebot

bot = telebot.TeleBot(API_TOKEN)


def get_places(user_id, latitude, longitude):
    personality = user_profiles[user_id]['personality']
    preferred_places = get_all_type_places(personality)
    places_query = '|'.join(preferred_places)

    places = find_nearby_places(latitude, longitude, places_query)

    return places

def send_places(user_id, places):
    if places:
        for place in places:
            bot.send_message(user_id, f"Название: {place['название']}\n"
                                      f"Количество оценок: {place['оценка']}\n"
                                      f"Местонахождение: {place['местонахождение']}")
            # Обновляем любимые места
            update_favorite_places(user_id, place['name'])
    else:
        bot.send_message(user_id, "К сожалению, я не нашел увеселительных заведений рядом.")
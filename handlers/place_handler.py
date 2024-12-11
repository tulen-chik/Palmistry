from config import user_profiles, bot
from bd.type_place import get_all_type_places
from services.google_service import find_nearby_places
from services.user_service import update_favorite_places
from telebot import types
from telebot.types import KeyboardButton, ReplyKeyboardMarkup
import telebot
import os
import logging
import recomendations
from models.userDataClass import User_dataclass



def get_places(user_id, latitude, longitude):
    personality = user_profiles[user_id]['personality']
    preferred_places = get_all_type_places(personality)
    places_query = '|'.join(preferred_places)

    places = find_nearby_places(latitude, longitude, places_query)
    logging.warning(places)
    # Сохраняем найденные места в состоянии пользователя
    user_profiles[user_id] = {'places': places, 'awaiting_rating': False}
    places = recomendations.recommend_places(User_dataclass(id=0,id_telegram=user_id,mood_id=3,latitude=latitude,longitude=longitude),
                                             places,[""])
    logging.warning(user_profiles)
    places_refactor = []
    for place in places:
        places_refactor.append(place[1])
    return places[::-1]


current_place_index = 0


def send_places(user_id, places):
    global current_place_index  # Используем глобальную переменную для отслеживания индекса

    if places:
        # Проверяем, есть ли еще места для отправки
        if current_place_index < len(places):
            place = places[current_place_index]

            # Создаем клавиатуру с кнопками "Лайк" и "Дизлайк"
            keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
            like_button = types.KeyboardButton("👍")
            dislike_button = types.KeyboardButton("👎")
            keyboard.add(like_button, dislike_button)

            # Отправляем сообщение с изображением и клавиатурой
            message = bot.send_photo(user_id,
                                     photo=f"https://maps.googleapis.com/maps/api/place/photo?maxwidth=400&photoreference={place['аватар']}&key={os.environ['GOOGLE_MAPS_KEY']}",
                                     caption=f"Название: {place['название']}\n"
                                             f"Количество оценок: {place.get('оценка', 'Нет оценок')}\n"
                                             f"Местонахождение: {place['местонахождение']}",
                                     reply_markup=keyboard)

            # Обновляем любимые места
            update_favorite_places(user_id, place['название'])

            # Ждем ответа от пользователя и удаляем предыдущее сообщение
            bot.register_next_step_handler(message, lambda msg, m=message: handle_rating(msg, m, places))
        else:
            bot.send_message(user_id, "Спасибо, что помогли настроить рекомендации в вашем аккаунте😘")
    else:
        bot.send_message(user_id, "К сожалению, я не нашел увеселительных заведений рядом.")


def handle_rating(message, previous_message, places):
    user_id = message.from_user.id
    global current_place_index  # Используем глобальную переменную для отслеживания индекса

    bot.delete_message(user_id, message.message_id)

    if message.text == "👍 Лайк":
        bot.send_message(user_id, "Спасибо за оценку! 👍")
    elif message.text == "👎 Дизлайк":
        bot.send_message(user_id, "Спасибо за оценку! 👎")

    # Удаляем предыдущее сообщение
    bot.delete_message(user_id, previous_message.message_id)

    # Увеличиваем индекс текущего места
    current_place_index += 1

    # Отправляем следующее место
    send_places(user_id, places)
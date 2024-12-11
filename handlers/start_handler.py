from config import user_profiles, bot
from bd.user import get_user, add_user, update_user
from bd.mood import get_mood
from utils.keyboard import generate_personality_keyboard, generate_main_menu_keyboard, generate_location_keyboard
import recomendations
import logging
from telebot import types
from models.userDataClass import User_dataclass
from services.google_service import find_nearby_places

def start_handler(message):
    user_id = message.from_user.id  # Получаем ID пользователя Telegram

    # Проверяем, существует ли пользователь в базе данных
    user = get_user(user_id)
    if user is None:
        add_user(user_id)  # Добавляем пользователя, если его нет
        bot.send_message(user_id, "🌟 Выбери один из вариантов: 🌈\n\n1. Интроверт\n2. Амбиверт\n3. Экстраверт",
                         reply_markup=generate_personality_keyboard())
    else:
        main_menu(message)

def choose_personality(message):
    user_id = message.chat.id
    personality_choice = message.text
    update_user(user_id, get_mood(name=personality_choice).id)

    if user_id not in user_profiles:
        user_profiles[user_id] = {
            'personality': personality_choice,
            'preferences': {
                'places_rated': 0,
                'favorite_places': [],
                'past_choices': []
            }
        }
    else:
        user_profiles[user_id]['personality'] = personality_choice

    user_profiles[user_id]['preferences']['past_choices'].append(personality_choice)

    bot.send_message(user_id, "Отправьте мне ваше местоположение 🌍", reply_markup=generate_location_keyboard())

def main_menu(message):
    user_id = message.chat.id
    bot.send_message(user_id, "Выберите действие: 🍽️🌳📸🛍️🏛️", reply_markup=generate_main_menu_keyboard())

def start_location_request(message):
    user_id = message.from_user.id
    # Запрашиваем у пользователя его местоположение
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    location_button = types.KeyboardButton("📍 Отправить мое местоположение", request_location=True)
    keyboard.add(location_button)

    bot.send_message(user_id, "Пожалуйста, отправьте свое местоположение.", reply_markup=keyboard)

def start_location_response(message):
    user_id = message.from_user.id
    latitude = message.location.latitude
    longitude = message.location.longitude

    # Здесь вызываем функцию для поиска мест
    places = find_nearby_places(latitude, longitude, places_query='')
    logging.warning(places)
    # Сохраняем найденные места в состоянии пользователя
    user_profiles[user_id] = {'places': places, 'awaiting_rating': False}
    places = recomendations.recommend_places(User_dataclass(id=0,id_telegram=user_id,mood_id=3,latitude=latitude,longitude=longitude),
                                             places,[""])
    logging.warning(user_profiles)
    suggest_places(user_id, places)

def suggest_places(user_id, places):
    if places:
        keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)

        # Добавляем названия мест в клавиатуру
        for place in places[:5]:  # Берем только первые 5 мест
            keyboard.add(types.KeyboardButton(place[0]['название']))

        bot.send_message(user_id, "Выберите заведение из списка, в котором вы находитесь:", reply_markup=keyboard)
        user_profiles[user_id]['awaiting_rating'] = True  # Устанавливаем флаг ожидания оценки
    else:
        bot.send_message(user_id, "К сожалению, я не нашел увеселительных заведений рядом.")

from config import bot, user_profiles
from services.google_service import find_nearby_places
from telebot import types
from bd.place import add_place
import os
from telebot.types import KeyboardButton, ReplyKeyboardMarkup
from services.images import edit_image

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

    # Сохраняем найденные места в состоянии пользователя
    user_profiles[user_id] = {'places': places, 'awaiting_rating': False}
    suggest_places(user_id, places)

def suggest_places(user_id, places):
    if places:
        keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)

        # Добавляем названия мест в клавиатуру
        for place in places[:5]:  # Берем только первые 5 мест
            keyboard.add(types.KeyboardButton(place['название']))

        bot.send_message(user_id, "Выберите заведение из списка, в котором вы находитесь:", reply_markup=keyboard)
        user_profiles[user_id]['awaiting_rating'] = True  # Устанавливаем флаг ожидания оценки
    else:
        bot.send_message(user_id, "К сожалению, я не нашел увеселительных заведений рядом.")

def place_selection_request(message):
    user_id = message.from_user.id
    selected_place_name = message.text
    places = user_profiles[user_id]['places']

    # Находим выбранное место
    selected_place = next((place for place in places if place['название'] == selected_place_name), None)

    if selected_place:
        # Сохраняем выбранное место в состоянии пользователя
        user_profiles[user_id]['selected_place'] = selected_place

        # Создаем клавиатуру с кнопками "Лайк" и "Дизлайк"
        keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
        like_button = types.KeyboardButton("👍 Лайк")
        dislike_button = types.KeyboardButton("👎 Дизлайк")
        keyboard.add(like_button, dislike_button)

        # Отправляем информацию о выбранном месте
        bot.send_photo(user_id,
                       photo=f"https://maps.googleapis.com/maps/api/place/photo?maxwidth=400&photoreference={selected_place['аватар']}&key={os.environ['GOOGLE_MAPS_KEY']}",
                       caption=f"Вы выбрали: {selected_place['название']}\n"
                               f"Оценка: {selected_place.get('оценка', 'Нет оценок')}\n"
                               f"Местонахождение: {selected_place['местонахождение']}",
                       reply_markup=keyboard)

        # Устанавливаем флаг ожидания оценки
        user_profiles[user_id]['awaiting_rating'] = False  # Сбрасываем флаг ожидания

        # Ждем оценки
        bot.register_next_step_handler(message, lambda msg: handle_rating(msg, selected_place_name))


def handle_rating(message, selected_place_name):
    user_id = message.from_user.id

    # Получаем выбранное место из состояния пользователя
    selected_place = user_profiles[user_id].get('selected_place')

    if selected_place:
        avatar_image_url = f"https://maps.googleapis.com/maps/api/place/photo?maxwidth=400&photoreference={selected_place['аватар']}&key={os.environ['GOOGLE_MAPS_KEY']}"
        bg_image_path = 'public/bg.png'
        output_image_path = 'public/edited_bg.png'

        # Редактируем изображение с аватаром и названием
        edit_image(bg_image_path, avatar_image_url, selected_place_name, output_image_path)

        # Отправляем измененное изображение пользователю
        with open(output_image_path, 'rb') as photo:
            bot.send_photo(user_id, photo)

        # После отправки изображения, добавляем место в базу данных
        user_rating = message.text  # Получаем оценку пользователя (👍 или 👎)
        points = 1000 if user_rating == "👍 Лайк" else 1000  # Присваиваем баллы на основе оценки
        add_place(user_id, selected_place_name, avatar=selected_place['аватар'], points=points, review=(user_rating == "👍 Лайк"))

    else:
        bot.send_message(user_id, "Не удалось найти информацию о выбранном месте.")
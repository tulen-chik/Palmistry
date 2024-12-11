from config import user_profiles, bot
from bd.type_place import get_all_type_places
from services.google_service import find_nearby_places
from services.user_service import update_favorite_places
from telebot import types
from bd.place import get_all_places
from telebot.types import KeyboardButton, ReplyKeyboardMarkup
import telebot
from services.images import edit_image_p
import os

@bot.callback_query_handler(func=lambda call: True)
def handle_callback_query(call):
    user_id = call.from_user.id
    if call.data == 'top_visits':
        response_profile(user_id, 'top_visits')
    elif call.data == 'top_points':
        response_profile(user_id, 'top_points')


def response_profile(user_id, top_type):
    if top_type == 'top_visits':
        top_places = get_all_places(sort_by_visits=True)[:3]
        place_names = [place[0].avatar for place in top_places]
        avatar_image_urls = [
            f"https://maps.googleapis.com/maps/api/place/photo?maxwidth=400&photoreference={place[1]}&key={os.environ['GOOGLE_MAPS_KEY']}"
            for place in top_places
        ]
        output_image_path = 'public/top_visits_image.png'
        response_text = "🏆 **Топ 3 самых посещаемых мест:**\n" + "\n".join([f"- {name}" for name in place_names])
    elif top_type == 'top_points':
        top_places = get_all_places(sort_by_points=True)[:3]
        place_names = [place[0] for place in top_places]
        avatar_image_urls = [
            f"https://maps.googleapis.com/maps/api/place/photo?maxwidth=400&photoreference={place[1]}&key={os.environ['GOOGLE_MAPS_KEY']}"
            for place in top_places
        ]
        output_image_path = 'public/top_points_image.png'
        response_text = "🌟 **Топ 3 мест с наибольшими очками:**\n" + "\n".join([f"- {name}" for name in place_names])
    else:
        bot.send_message(user_id, "Некорректный тип запроса.")
        return

    # Отправляем текстовый список мест пользователю
    bot.send_message(user_id, response_text, parse_mode='Markdown')

    # Редактируем изображение с аватарами и названиями мест
    edit_image_p(avatar_image_urls=avatar_image_urls, place_names=place_names, output_image_path=output_image_path)

    # Отправляем измененное изображение пользователю
    with open(output_image_path, 'rb') as photo:
        bot.send_photo(user_id, photo)
from config import user_profiles, bot
from bd.type_place import get_all_type_places
from services.google_service import find_nearby_places
from services.user_service import update_favorite_places
from telebot import types
from bd.place import get_all_places
from telebot.types import KeyboardButton, ReplyKeyboardMarkup
import telebot
import os

def response_profile(message):
    # Получение топ-3 самых посещаемых мест
    top_visits = get_all_places(sort_by_visits=True)[:3]

    # Получение топ-3 мест с наибольшими очками
    top_points = get_all_places(sort_by_points=True)[:3]

    response = "🏆 **Топ 3 самых посещаемых мест:**\n"
    for place, visit_count in top_visits:
        response += f"- {place.name}: {visit_count} визитов\n"

    response += "\n🌟 **Топ 3 мест с наибольшими очками:**\n"
    for place, _ in top_points:
        response += f"- {place.name}: {place.points} очков\n"

    # Отправка ответа пользователю
    bot.send_message(message.chat.id, response, parse_mode='Markdown')

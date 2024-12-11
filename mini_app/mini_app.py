import os
from aiogram import Bot, Dispatcher, types
from aiogram.types.web_app_info import WebAppInfo
from bd.type_place import get_all_type_places
from bd.mood import get_all_moods
import telebot

from config import bot
@bot.message_handler(commands=['game'])
def game(message):
    user_id = message.from_user.id
    type_places = get_all_type_places()  # Получение данных из таблицы TypePlace
    moods = get_all_moods()  # Получение данных из таблицы Mood

    type_places_str = ','.join([place.name for place in type_places])
    moods_str = ','.join([mood.name for mood in moods])

    game_url = f'https://shpack.monster?type_places={type_places_str}&moods={moods_str}'

    markup = telebot.types.ReplyKeyboardMarkup()
    markup.add(telebot.types.KeyboardButton('Пройти квест', web_app=telebot.types.WebAppInfo(url=game_url)))

    bot.send_message(message.chat.id, 'мяу', reply_markup=markup)
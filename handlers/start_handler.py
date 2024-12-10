from config import API_TOKEN,user_profiles
from utils.keyboard import generate_personality_keyboard, generate_main_menu_keyboard, generate_location_keyboard
import telebot

bot = telebot.TeleBot(API_TOKEN)

def start_handler(message):
    user_id = message.chat.id
    if user_id not in user_profiles:
        bot.send_message(user_id, "Привет! 🌟 Выбери один из вариантов: 🌈\n\n1. Интроверт\n2. Амбиверт\n3. Экстраверт",
                         reply_markup=generate_personality_keyboard())
    else:
        main_menu(message)

def choose_personality(message):
    user_id = message.chat.id
    personality_choice = message.text

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
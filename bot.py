import telebot
from config import API_TOKEN
from handlers.start_handler import start_handler, choose_personality
from handlers.location_handler import handle_location
from handlers.profile_handler import show_profile
from handlers.filter_handler import filter_places
from utils.keyboard import generate_main_menu_keyboard

bot = telebot.TeleBot(API_TOKEN)

@bot.message_handler(commands=['start'])
def start_command(message):
    start_handler(message)

@bot.message_handler(func=lambda message: message.text in ["Интроверт", "Амбиверт", "Экстраверт"])
def personality_command(message):
    choose_personality(message)

@bot.message_handler(content_types=['location'])
def location_command(message):
    handle_location(message)

@bot.message_handler(commands=['profile'])
def profile_command(message):
    show_profile(message)

@bot.message_handler(commands=['filter'])
def filter_command(message):
    filter_places(message)

def main_menu(message):
    user_id = message.chat.id
    bot.send_message(user_id, "Выберите действие: 🍽️🌳📸🛍️🏛️", reply_markup=generate_main_menu_keyboard())

# Основной цикл
bot.polling(none_stop=True)
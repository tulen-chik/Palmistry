from telebot import types
from telebot.types import KeyboardButton, ReplyKeyboardMarkup

def generate_personality_keyboard():
    markup = ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add(
        KeyboardButton("Интроверт"),
        KeyboardButton("Амбиверт"),
        KeyboardButton("Экстраверт")
    )
    return markup

def generate_location_keyboard():
    markup = ReplyKeyboardMarkup(resize_keyboard=True)
    button = KeyboardButton("Отправить моё местоположение", request_location=True)
    markup.add(button)
    return markup

def create_profile_menu_keyboard():
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.add(types.KeyboardButton('/show_profile'))
    keyboard.add(types.KeyboardButton('/update_username'))
    keyboard.add(types.KeyboardButton('/update_personality'))
    keyboard.add(types.KeyboardButton('Вернуться на главное меню'))
    return keyboard

def generate_main_menu_keyboard():
    markup = ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add(
        KeyboardButton("🍽️ Рестораны"),
        KeyboardButton("🌳 Парки"),
        KeyboardButton("📸 Фотографические места"),
        KeyboardButton("🛍️ Магазины"),
        KeyboardButton("🏛️ Музеи")
    )
    return markup
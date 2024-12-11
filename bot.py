import telebot
from config import Base, engine, bot, user_profiles
from bd.seeder import seed_moods, seed_type_places
from handlers.start_handler import start_handler, choose_personality
from handlers.location_handler import handle_location
from handlers.portfolio_handler import response_profile  # Import the registration function
from handlers.filter_handler import filter_places
from handlers.coupon_handler import place_selection_request
from handlers.start_handler import start_location_request, start_location_response, start_location_response_categorized
from utils.keyboard import generate_main_menu_keyboard
from handlers.location_handler import send_places
# from mini_app.mini_app import game
from telebot import types
from AI import AI
import logging

@bot.message_handler(commands=['start'])
def start_command(message):
    start_handler(message)

@bot.message_handler(commands=['profile'])
def handler_profile(message):
    # Create inline keyboard for user selection
    keyboard = types.InlineKeyboardMarkup()
    keyboard.add(types.InlineKeyboardButton("Топ 3 самых посещаемых мест", callback_data='top_visits'))
    keyboard.add(types.InlineKeyboardButton("Топ 3 мест с наибольшими очками", callback_data='top_points'))

    # Send message with keyboard
    bot.send_message(message.chat.id, "Выберите, что вы хотите увидеть:", reply_markup=keyboard)
@bot.message_handler(func=lambda message: message.text in ["Интроверт", "Амбиверт", "Экстраверт"])
def personality_command(message):
    choose_personality(message)



@bot.callback_query_handler(func=lambda call: True)
def callback_handler(call):
    user_id = call.from_user.id
    if call.data == 'like':
        bot.answer_callback_query(call.id, "Спасибо за оценку! 👍")
    elif call.data == 'dislike':
        bot.answer_callback_query(call.id, "Спасибо за оценку! 👎")

    # Обновляем следующее место
    send_places(user_id, places)

@bot.message_handler(content_types=['location'])
def location_command(message):
    handle_location(message)

@bot.message_handler(commands=['filter'])
def filter_command(message):
    filter_places(message)

@bot.message_handler(commands=['me'])
def request_location(message):
    user_profiles[message.from_user.id]['awaiting_location'] = True
    start_location_request(message)

@bot.message_handler(func=lambda message: user_profiles.get(message.from_user.id, {}).get('awaiting_rating', False) and
                                          message.text in [place['название'] for place in
                                                           user_profiles[message.from_user.id]['places']])
def handle_place_selection(message):
    user_profiles[message.from_user.id]['awaiting_rating'] = False
    place_selection_request(message)


@bot.message_handler(content_types=["location"])
def handle_location(message):
    if user_profiles.get(message.from_user.id, {}).get('awaiting_location', False):
        user_profiles[message.from_user.id]['awaiting_location'] = False
        start_location_response(message)
    else:
        handle_location(message)

@bot.message_handler(content_types=["game"])
def game_start(message):
    game(message)

@bot.message_handler(func=lambda message: True)
def handle_message(message):
    if message.chat.id in user_profiles and user_profiles[message.chat.id] == "main_menu":
        if message.text == "🍽️ Рестораны":
            start_location_response_categorized(message,"Кафе")
        elif message.text == "🌳 Парки":
            start_location_response_categorized(message,"Парк")
        elif message.text == "📸 Фотографические места":
            start_location_response_categorized(message,"Библиотека")
        elif message.text == "🛍️ Магазины":
            start_location_response_categorized(message,"Игровые кафе")
        elif message.text == "🏛️ Музеи":
            start_location_response_categorized(message,"Музеи")
        else:
            bot.send_message(message.chat.id, "Пожалуйста, выберите действие из меню.")

def main():
    Base.metadata.create_all(engine)
    seed_moods()
    seed_type_places()
    AI.initAI()
    logging.warning("sosi") # Register profile handlers
    bot.polling(none_stop=True)

if __name__ == "__main__":
    main()
import telebot
from config import Base, engine, bot, user_profiles
from bd.seeder import seed_moods, seed_type_places
from handlers.start_handler import start_handler, choose_personality
from handlers.location_handler import handle_location# Import the registration function
from handlers.filter_handler import filter_places
from bd.place import get_all_places
from handlers.coupon_handler import place_selection_request
from handlers.start_handler import start_location_request, start_location_response
from utils.keyboard import generate_main_menu_keyboard
from handlers.location_handler import send_places
# from mini_app.mini_app import game
from AI import AI
import logging


@bot.message_handler(commands=['profile'])
def handle_profile(message):
    # Получение топ-3 мест по количеству
    top_places = get_all_places(sort_by_visits=True)[:3]

    # Получение топ-3 мест по очкам
    top_points = get_all_places(sort_by_points=True)[:3]

    response = "🏆 **Топ 3 мест по количеству:**\n"
    for name, count, _ in top_places:
        response += f"- {name}: {count} мест\n"

    response += "\n🌟 **Топ 3 мест по очкам:**\n"
    for name, _, total_points in top_points:
        response += f"- {name}: {total_points} очков\n"

    bot.send_message(message.chat.id, response, parse_mode='Markdown')

@bot.message_handler(commands=['start'])
def start_command(message):
    start_handler(message)

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
    start_location_request(message)

@bot.message_handler(func=lambda message: user_profiles.get(message.from_user.id, {}).get('awaiting_rating', False) and
                                          message.text in [place['название'] for place in
                                                           user_profiles[message.from_user.id]['places']])
def handle_place_selection(message):
    place_selection_request(message)


@bot.message_handler(content_types=["location"])
def handle_location(message):
    start_location_response(message)


@bot.message_handler(content_types=["game"])
def game_start(message):
    game(message)


def main():
    Base.metadata.create_all(engine)
    seed_moods()
    seed_type_places()
    AI.initAI()  # Register profile handlers
    bot.polling(none_stop=True)

if __name__ == "__main__":
    main()
import telebot
from config import Base, engine, bot, user_profiles
from bd.seeder import seed_moods, seed_type_places
from handlers.start_handler import start_handler, choose_personality
from handlers.location_handler import handle_location
from handlers.profile_handler import register_profile_handlers  # Import the registration function
from handlers.filter_handler import filter_places
from handlers.coupon_handler import start_location_request, start_location_response, place_selection_request
from utils.keyboard import generate_main_menu_keyboard
from handlers.location_handler import send_places
from mini_app.mini_app import game
# from AI import AI
from handlers.portfolio_handler import response_profile

@bot.message_handler(content_types=["game"])
def game_start(message):
    game(message)

@bot.message_handler(commands=['profile'])
def profile_handler(message):
    response_profile(message)

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


def main():
    Base.metadata.create_all(engine)
    seed_moods()
    seed_type_places()
    # AI.initAI()
    register_profile_handlers(bot)  # Register profile handlers
    bot.polling(none_stop=True)

if __name__ == "__main__":
    main()
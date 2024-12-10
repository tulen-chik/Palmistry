import telebot
from config import Base, engine
from bd.seeder import seed_moods, seed_type_places
from handlers.start_handler import start_handler, choose_personality
from handlers.location_handler import handle_location
from handlers.profile_handler import register_profile_handlers  # Import the registration function
from handlers.filter_handler import filter_places
from utils.keyboard import generate_main_menu_keyboard

bot = telebot.TeleBot(os.environ['TELEGRAM_BOT_TOKEN'])

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
    bot.send_message(message.chat.id, "Загрузка профиля...", reply_markup=generate_main_menu_keyboard())

@bot.message_handler(commands=['filter'])
def filter_command(message):
    filter_places(message)

def main():
    Base.metadata.create_all(engine)
    seed_moods()
    seed_type_places()
    register_profile_handlers(bot)  # Register profile handlers
    bot.polling(none_stop=True)

if __name__ == "__main__":
    main()
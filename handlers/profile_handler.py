from config import user_profiles
from telebot import types
from utils.keyboard import create_profile_menu_keyboard

user_states = {}

def create_main_menu_keyboard():
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.add(types.KeyboardButton('/show_profile'))
    keyboard.add(types.KeyboardButton('/update_username'))
    keyboard.add(types.KeyboardButton('/update_personality'))
    keyboard.add(types.KeyboardButton('Вернуться на главное меню'))
    return keyboard

# Function to show user profile
def show_profile(message, bot):
    user_id = message.chat.id
    if user_id not in user_profiles:
        user_profiles[user_id] = {
            'username': message.from_user.username or message.from_user.first_name,
            'photo': None,
            'personality': None,
            'preferences': {
                'places_rated': 0,
                'favorite_places': [],
                'past_choices': []
            }
        }
        bot.send_message(user_id, "Ваш профиль был автоматически создан. Пожалуйста, выберите тип личности.", reply_markup=create_main_menu_keyboard())
        return

    profile = user_profiles[user_id]
    response = (
        f"Ваш профиль:\n"
        f"Имя: {profile['username']}\n"
        f"Фотография: {'Есть' if profile['photo'] else 'Нет'}\n"
        f"Тип личности: {profile['personality'] or 'Не задан'}\n"
        f"Оцененные места: {profile['preferences']['places_rated']}\n"
        f"Любимые места: {', '.join(profile['preferences']['favorite_places']) if profile['preferences']['favorite_places'] else 'Нет'}\n"
        f"Прошлые выборы: {', '.join(profile['preferences']['past_choices']) or 'Нет'}"
    )
    bot.send_message(user_id, response, reply_markup=create_main_menu_keyboard())

# Function to handle username updates
def update_username(message, bot):
    user_id = message.chat.id
    new_username = message.text

    if user_id in user_profiles:
        user_profiles[user_id]['username'] = new_username
        bot.send_message(user_id, "Имя пользователя обновлено.", reply_markup=create_main_menu_keyboard())
    else:
        bot.send_message(user_id, "Профиль не найден.", reply_markup=create_main_menu_keyboard())

# Function to handle personality updates
def update_personality(message, bot):
    user_id = message.chat.id
    new_personality = message.text

    if user_id in user_profiles:
        user_profiles[user_id]['personality'] = new_personality
        bot.send_message(user_id, "Тип личности обновлён.", reply_markup=create_main_menu_keyboard())
    else:
        bot.send_message(user_id, "Профиль не найден.", reply_markup=create_main_menu_keyboard())

# Function to handle photo updates
def update_photo(message, bot):
    user_id = message.chat.id

    if user_id in user_profiles and message.photo:
        user_profiles[user_id]['photo'] = message.photo[-1].file_id
        bot.send_message(user_id, "Фотография обновлена.", reply_markup=create_main_menu_keyboard())
    else:
        bot.send_message(user_id, "Ошибка: фотография не найдена.", reply_markup=create_main_menu_keyboard())

# Function to register profile handlers
def register_profile_handlers(bot):
    @bot.message_handler(commands=['show_profile'])
    def handle_show_profile(message):
        show_profile(message, bot)

    @bot.message_handler(commands=['update_username'])
    def handle_update_username(message):
        bot.send_message(message.chat.id, "Введите новое имя пользователя:")
        user_states[message.chat.id] = 'updating_username'  # Set state
        bot.register_next_step_handler(message, update_username, bot)

    @bot.message_handler(commands=['update_personality'])
    def handle_update_personality(message):
        bot.send_message(message.chat.id, "Введите новый тип личности:")
        user_states[message.chat.id] = 'updating_personality'  # Set state
        bot.register_next_step_handler(message, update_personality, bot)

    @bot.message_handler(content_types=['photo'])
    def handle_photo(message):
        update_photo(message, bot)

    @bot.message_handler(func=lambda message: message.text == 'Вернуться на главное меню')
    def handle_return_to_main_menu(message):
        bot.send_message(message.chat.id, "Выберите действие:", reply_markup=create_main_menu_keyboard())
        user_states.pop(message.chat.id, None)
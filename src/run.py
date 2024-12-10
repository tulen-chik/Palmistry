import os
import telebot
import requests

bot = telebot.TeleBot(os.environ['TELEGRAM_BOT_TOKEN'])
API_URL = os.environ['API_SERVER_URL']  # Your API URL should be set in the environment variable

@bot.message_handler(commands=['start'])
def send_welcome(message):
    user_id = message.from_user.id  # Get the Telegram user ID
    id_telegram = str(user_id)  # Use it as id_telegram (or replace with your logic)

    # Send POST request to capture id_telegram
    post_data = {'id_telegram': id_telegram}
    try:
        print(post_data)
        response = requests.post(API_URL + '/capture_id', json=post_data)
        response.raise_for_status()  # Raise an error for HTTP errors
    except requests.exceptions.RequestException as e:
        bot.reply_to(message, f"Ошибка при отправке ID: {str(e)}")
        return

    # Create the link for the GET request
    get_link = f"{os.environ['API_URL']}/capture_ip?id_telegram={id_telegram}"
    bot.reply_to(message, f"Для получения IP, перейдите по следующей ссылке: {get_link}\n{id_telegram}")

bot.polling()
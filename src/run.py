import os

import telebot

bot = telebot.TeleBot(os.environ['TELEGRAM_BOT_TOKEN'])

@bot.message_handler(commands=['start'])
def send_welcome(message):

    bot.reply_to(message, "выберите тег, который вас интересует")

bot.polling()
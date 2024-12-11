import os
from aiogram import Bot, Dispatcher, types
from dotenv import load_dotenv
from aiogram.types.web_app_info import WebAppInfo

load_dotenv()

TELEGRAM_BOT_TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')

bot = Bot(token=TELEGRAM_BOT_TOKEN)
dp = Dispatcher()

@dp.message_handler(commands=['game'])
async def game(message: types.Message):
    markup = types.ReplyKeyboardMarkup()
    markup.add(types.KeyboardButton('Пройти квест', web_app=WebAppInfo(url='https://github.com/KQnok/mini')))
    await message.answer('мяу', reply_markup=markup)
from aiogram import Bot, Dispatcher, types
from config import API_TOKEN
from aiogram.types.web_app_info import WebAppInfo

bot = Bot(token=API_TOKEN)
dp = Dispatcher()

@dp.message_handler(commands=['game'])
async def game(message: types.Message):
    markup = types.ReplyKeyboardMarkup()
    markup.add(types.KeyboardButton('Пройти квест', web_app=WebAppInfo(url='https://github.com/KQnok/mini')))
    await message.answer('мяу', reply_markup=markup)
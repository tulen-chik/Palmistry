from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import telebot
import os

# Настройки подключения к базе данных
engine = create_engine(os.environ.get('DATABASE_URL'))
Base = declarative_base()
Session = sessionmaker(bind=engine)

bot = telebot.TeleBot(os.environ['TELEGRAM_BOT_TOKEN'])
user_profiles = {}

places_by_personality = {
    "Экстраверт": ["Ночные клубы", "Спортивные клубы", "Киберспортивные арены", "Кафе", "Танцевальные студии", "Туристические агентства", "Волонтерские организации"],
    "Интроверт": ["Библиотеки", "Книжные магазины", "Игровые кафе", "Мастерские", "Парки", "Студии йоги", "Музеи"],
    "Амбиверт": ["Квест-комнаты", "Спортивные клубы", "Книжные клубы", "Концертные залы", "Киберспортивные турниры", "Пикниковые зоны", "Мастер-классы"]
}
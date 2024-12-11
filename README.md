# 📚 Руководство по запуску проекта

## 📦 Ссылка на бота
[Запустить бота](https://t.me/@placeadvicer_bot) (во время разработки может быть временно недоступен)

## 🚀 Запуск проекта

Для запуска проекта выполните следующие шаги:

1. Откройте консоль.
2. Перейдите в корневой каталог проекта.
3. Введите команду:
   ```bash
   docker compose up --build
   ```

## 📄 Настройка .env файла

Поместите файл `.env` в корневой каталог проекта. Пример содержимого файла:

```env
DATABASE_URL=postgresql://your_username:your_password@db:5432/your_database_name

TELEGRAM_BOT_TOKEN=67610vrtecfdx65gxrecyhtrvecwjhytrvecdsyuhtvd

POSTGRES_DB=your_database_name

POSTGRES_USER=your_username

POSTGRES_PASSWORD=your_password

API_URL=http://localhost

BOT_TAG=groupes_cool_bot

GOOGLE_MAPS_KEY=AIzaSy2Bn7LzN3Dr3d3242we334MirJtwdewf30dj3f34fj3bh34fQ
```

### 🔑 Обязательные переменные

Все переменные в файле `.env` являются обязательными для корректной работы проекта.

## 📌 Примечания

- Убедитесь, что вы заменили все значения в `.env` на свои собственные.
- Если у вас возникнут вопросы, обратитесь к документации или задайте их в сообществе разработчиков.

---

Теперь вы готовы запустить и использовать проект! 🎉

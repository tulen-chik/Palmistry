для запуска проекта надо в консоли, находясь в корневом каталоге проекта ввести docker compose up --build

поместите .env файл в корневой каталог поекта, пример файла:
DATABASE_URL=postgres://your_username:your_password@db:5432/your_database_name
TELEGRAM_BOT_TOKEN=кпдц059320пекмкпмкпt3IphHjasUagnz8ArxkQA7pLb-9345а
POSTGRES_DB=your_database_name
POSTGRES_USER=your_username
POSTGRES_PASSWORD=your_password

все переменные обязательны

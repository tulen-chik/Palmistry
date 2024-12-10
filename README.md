для запуска проекта надо в консоли, находясь в корневом каталоге проекта ввести docker compose up --build

поместите .env файл в корневой каталог поекта, пример файла:
DATABASE_URL=postgres://your_username:your_password@db:5432/your_database_name
TELEGRAM_BOT_TOKEN=кпдц059320пекмкпмкпt3IphHjasUagnz8ArxkQA7pLb-9345а
POSTGRES_DB=your_database_name
POSTGRES_USER=your_username
POSTGRES_PASSWORD=your_password
API_URL=http://localhost
API_SERVER_URL=http://api_server:5000
BOT_TAG=groupes_cool_bot
GOOGLE_MAPS_KEY=AIafkyBsnE7LofvI-zNsfsgsfDgsggld2TsdsMirJ-0dj_Q
YANDEX_MAPS_KEY=db6ecadsasdgasf-f1ds-g4cfsdd-a6da-dsd64gfsgss00sd9s4

все переменные обязательны

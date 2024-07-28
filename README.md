
# CTFbot

CTFbot — это Telegram-бот для проведения CTF  соревнований (Capture The Flag) с использованием библиотек aiogram и SQLAlchemy.

## Установка

1. Клонируйте репозиторий:

git clone https://github.com/kernel-paniccc/CTFbot.git


2. Установите зависимости:

pip install -r requirements.txt


3. Создайте файл .env и добавьте необходимые переменные окружения:

TOKEN='BOT_API_TOKEN'

URL='SQLALHIMY_URL'

FLAGS='['Flag1', 'Flag2', '...']' (json)

## Использование

1. Запустите бота:

python3 run.py

## Функции

- Регистрация участников.
- Просмотр профиля.
- Отслеживание результатов и набранных очков участников в скорборде.
- Сдача флагов

## Структура проекта

- app/hendlels.py: Файл с логикой бота и описанием роутеров.
- app/database/models.py: Модели SQLAlchemy для работы с базой данных.
- app/database/requests.py: Функции реквеста в БД.
- run.py: запуск и инициализация бота.

---

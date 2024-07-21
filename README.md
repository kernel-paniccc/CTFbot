
# CTFbot

CTFbot — это Telegram-бот для проведения соревнований по захвату флагов (Capture The Flag) с использованием библиотек aiogram и SQLAlchemy.

## Установка

1. Клонируйте репозиторий:

git clone https://github.com/kernel-paniccc/CTFbot.git


2. Установите зависимости:

pip install -r requirements.txt


3. Создайте файл .env и добавьте необходимые настройки:

TOKEN='BOT_API_TOKEN'
URL='SQLALHIMY_URL'
FLAGS='['Flag1', 'Flag2', '...']' (json)


## Использование

1. Запустите бота:

python run.py

## Функциональности

- Регистрация участников.
- Просмотр профиля.
- Отслеживание результатов и набранных очков участников в скорборде.
- Сдача флагов

## Структура проекта

- app/hendlels.py: Файл с логикой бота и описанием роутеров.
- app/database/models.py: Модели SQLAlchemy для работы с базой данных.
- app/database/requests.py: Функции реквеста в БД.
- run.py: запуск и инициализация бота.

## Авторы

-  Ручкин Иван ([kernrl_paniccc](https://t.me/Kernel_Paniccc))

## Лицензия

Этот проект лицензирован по лицензии [Apache-2.0 license](LICENSE).

---

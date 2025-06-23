**Telegram GPT Bot**
Цей Telegram бот написаний на Python із використанням бібліотеки python-telegram-bot та OpenRouter API (сумісний з OpenAI) для генерації тексту та коду.

Функціональність
Команда /code активує режим генерації коду.

Якщо повідомлення починається з "Напиши код для ...", бот надсилає запит до OpenRouter і повертає відповідь.

Передбачено обробку помилок для стабільної роботи.

Як отримати необхідні ключі
1. Отримання Telegram токена
Відкрийте BotFather у Telegram.

Використайте команду /newbot, задайте ім’я та юзернейм для бота.

Отримайте API токен (наприклад: 1234567890:ABCdefGHIjklMNOpqrSTUvwxYZ).

2. Отримання OpenRouter API ключа
Перейдіть на сайт: https://openrouter.ai/

Зареєструйтесь або увійдіть.

Відкрийте розділ API Keys: https://openrouter.ai/keys

Згенеруйте новий ключ (виглядає приблизно як openrouter-...).

Встановлення
1. Клонування репозиторію:
bash
Копіювати
Редагувати
git clone https://github.com/yourusername/telegram-gpt-bot.git
cd telegram-gpt-bot
2. Встановлення залежностей:
bash
Копіювати
Редагувати
pip install -r requirements.txt
Вміст requirements.txt:

Копіювати
Редагувати
python-telegram-bot==20.3
requests
tk
Налаштування ключів
Створіть файл config.py у корені проєкту з наступним вмістом:

python
Копіювати
Редагувати
TELEGRAM_BOT_TOKEN = "ваш_токен_від_BotFather"
OPENROUTER_API_KEY = "ваш_API_ключ_від_OpenRouter"
Альтернативно можна використовувати .env файл із бібліотекою python-dotenv.

Запуск
bash
Копіювати
Редагувати
python bot.py
Логіка роботи
Бот слухає вхідні повідомлення у Telegram.

Команда /code активує режим генерації коду.

Якщо повідомлення користувача починається з фрази "Напиши код для ...", воно надсилається до OpenRouter.

Відповідь GPT надсилається користувачу у Telegram.

**Обробка помилок**
Усі винятки при запитах до API або Telegram обробляються і виводяться в консоль.

Якщо OpenRouter API недоступний — бот повідомляє про це користувачу.

У разі неправильного токена — бот завершить роботу з поясненням у логах.

Можливі подальші покращення
Кешування відповідей GPT.

Збереження історії сесій у базі даних (наприклад, SQLite).

Підтримка кількох моделей (GPT-3.5, GPT-4).

Обробка зображень та файлів.

Команди /help, /clear, /image, тощо.

Адмін-панель або логування у файл.

Приклад використання
Користувач:

Копіювати
Редагувати
Напиши код для бота, який надсилає погоду у Telegram.
Бот:
(відповідь GPT через OpenRouter)

python
Копіювати
Редагувати
import requests
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

async def weather(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # код для отримання погоди
    await update.message.reply_text("Погода: сонячно, 25°C")

app = ApplicationBuilder().token("YOUR_TOKEN").build()
app.add_handler(CommandHandler("weather", weather))
app.run_polling()

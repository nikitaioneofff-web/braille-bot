import os
import logging
import threading
from flask import Flask
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import Updater, CommandHandler, CallbackContext

# ===== НАСТРОЙКИ ИЗ ПЕРЕМЕННЫХ СРЕДЫ =====
TOKEN = os.environ.get('BOT_TOKEN')
SITE_URL = os.environ.get('SITE_URL')

# Проверка, что переменные загрузились
if not TOKEN:
    print("ОШИБКА: BOT_TOKEN не найден в переменных окружения!")
if not SITE_URL:
    print("ОШИБКА: SITE_URL не найден в переменных окружения!")

# ===== НАСТРОЙКА ЛОГИРОВАНИЯ =====
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# ===== КОМАНДЫ БОТА =====
def start(update: Update, context: CallbackContext):
    """Отправляет приветствие с кнопкой"""
    keyboard = [[InlineKeyboardButton("🎨 Открыть конвертер", url=SITE_URL)]]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    message = (
        "👋 *Привет!*\n\n"
        "Я помогу превратить твои фото в рисунки из символов Брайля.\n\n"
        "📸 *Как это работает:*\n"
        "1️⃣ Нажми кнопку ниже\n"
        "2️⃣ Загрузи фото на сайте\n"
        "3️⃣ Скопируй результат\n"
        "4️⃣ Вставь в любой чат\n\n"
        "✨ *22 символа в ширину — идеально для телефона!*"
    )
    
    update.message.reply_text(
        message,
        parse_mode='Markdown',
        reply_markup=reply_markup,
        disable_web_page_preview=True
    )

def help_command(update: Update, context: CallbackContext):
    """Отправляет помощь"""
    keyboard = [[InlineKeyboardButton("🎨 Открыть конвертер", url=SITE_URL)]]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    help_text = (
        "❓ *Помощь*\n\n"
        "1. Нажми кнопку *«Открыть конвертер»*\n"
        "2. Выбери фото на сайте\n"
        "3. Нажми *«Конвертировать»*\n"
        "4. Скопируй результат\n"
        "5. Вставь в Telegram"
    )
    
    update.message.reply_text(
        help_text,
        parse_mode='Markdown',
        reply_markup=reply_markup
    )

# ===== ПРОСТОЙ ВЕБ-СЕРВЕР ДЛЯ RENDER =====
app = Flask(__name__)

@app.route('/')
def home():
    return "Бот работает! ✅"

def run_http_server():
    """Запускает Flask-сервер на порту 10000."""
    app.run(host='0.0.0.0', port=10000, debug=False, use_reloader=False)

# ===== ЗАПУСК БОТА =====
def main():
    # Запускаем HTTP-сервер в отдельном потоке (для Render)
    threading.Thread(target=run_http_server, daemon=True).start()
    logger.info("🌐 HTTP-сервер запущен на порту 10000")

    # Запускаем бота
    updater = Updater(TOKEN, use_context=True)
    dp = updater.dispatcher
    
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("help", help_command))
    
    updater.start_polling()
    logger.info("✅ Бот запущен на Render 24/7!")
    updater.idle()

if __name__ == '__main__':
    main()

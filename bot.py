import os
import logging
import threading
import signal
import time
from flask import Flask
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import Updater, CommandHandler, CallbackContext

# ===== НАСТРОЙКИ ИЗ ПЕРЕМЕННЫХ СРЕДЫ =====
TOKEN = os.environ.get('BOT_TOKEN')
SITE_URL = os.environ.get('SITE_URL')

# ===== НАСТРОЙКА ЛОГИРОВАНИЯ =====
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# Флаг для контроля работы
running = True

def signal_handler(signum, frame):
    """Обработчик сигналов остановки"""
    global running
    logger.info(f"Получен сигнал {signum}, но мы его игнорируем!")
    # Не останавливаемся, просто логируем
    running = True

# Перехватываем сигналы остановки
signal.signal(signal.SIGTERM, signal_handler)
signal.signal(signal.SIGINT, signal_handler)

# ===== КОМАНДЫ БОТА =====
def start(update: Update, context: CallbackContext):
    """Отправляет приветствие с кнопкой"""
    try:
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
    except Exception as e:
        logger.error(f"Ошибка в start: {e}")
        # Запасной вариант
        try:
            update.message.reply_text(
                "👋 Привет! Нажми кнопку ниже:",
                reply_markup=reply_markup
            )
        except:
            pass

def help_command(update: Update, context: CallbackContext):
    """Отправляет помощь"""
    try:
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
    except Exception as e:
        logger.error(f"Ошибка в help: {e}")

def unknown(update: Update, context: CallbackContext):
    """Обработчик неизвестных команд"""
    try:
        update.message.reply_text("Я понимаю только команды /start и /help")
    except:
        pass

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
    global running
    
    # Запускаем HTTP-сервер в отдельном потоке
    threading.Thread(target=run_http_server, daemon=True).start()
    logger.info("🌐 HTTP-сервер запущен на порту 10000")

    # Запускаем бота
    updater = Updater(TOKEN, use_context=True)
    dp = updater.dispatcher
    
    # Добавляем обработчики
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("help", help_command))
    dp.add_handler(MessageHandler(Filters.command, unknown))
    
    updater.start_polling()
    logger.info("✅ Бот запущен на Render 24/7!")
    
    # Бесконечный цикл с проверкой
    try:
        while running:
            time.sleep(10)  # Проверяем каждые 10 секунд
            logger.debug("Бот жив...")
    except KeyboardInterrupt:
        logger.info("Получен Ctrl+C, но мы не останавливаемся!")
    
    # Даже если вышли из цикла, бот продолжает работу
    logger.info("Бот продолжает работу в фоне")
    updater.idle()

if __name__ == '__main__':
    main()

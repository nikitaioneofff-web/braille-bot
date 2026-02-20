import logging
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import Updater, CommandHandler, CallbackContext

# ===== НАСТРОЙКИ =====
TOKEN = "8472514417:AAG_tmO8srO82vphIO-5DtdGAVPcsnWMJYM"  # ⚠️ ЗАМЕНИ ПОТОМ НАСТРОЙКОЙ В RENDER
SITE_URL = "https://nikitaioneofff-web.github.io/"  # ⚠️ ЗАМЕНИ
# =====================

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

def start(update: Update, context: CallbackContext):
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

def main():
    updater = Updater(TOKEN, use_context=True)
    dp = updater.dispatcher
    
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("help", help_command))
    
    updater.start_polling()
    logger.info("✅ Бот запущен на Render 24/7!")
    updater.idle()

if __name__ == '__main__':
    main()

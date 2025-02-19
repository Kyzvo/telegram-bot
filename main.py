from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Updater, CommandHandler, CallbackContext

# Команда /start
def start(update: Update, context: CallbackContext):
    # Создаем кнопку
    keyboard = [[InlineKeyboardButton("Open Mini App", web_app={"url": "https://telegram-bot-1-i7hd.onrender.com"})]]
    reply_markup = InlineKeyboardMarkup(keyboard)

    # Отправляем сообщение с кнопкой
    update.message.reply_text("Добро пожаловать! Нажмите кнопку ниже, чтобы открыть мини-приложение.", reply_markup=reply_markup)

# Основная функция
def main():
    # Вставьте сюда токен вашего бота
    updater = Updater("7943667357:AAHAWLqXTdpkfXjjlbgNmeNUSnJGUSVXbVI")
    dispatcher = updater.dispatcher

    dispatcher.add_handler(CommandHandler("start", start))

    updater.start_polling()
    updater.idle()

if __name__ == "__main__":
    main()

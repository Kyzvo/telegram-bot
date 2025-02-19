from telegram import Update
from telegram.ext import Updater, CommandHandler, CallbackContext
import datetime

# База данных (пока что в памяти)
users = {}

# Команда /start
def start(update: Update, context: CallbackContext):
    user_id = update.message.from_user.id
    if user_id not in users:
        users[user_id] = {"points": 0, "last_daily": None}
        update.message.reply_text("Добро пожаловать! Вы зарегистрированы.")
    else:
        update.message.reply_text("Вы уже зарегистрированы.")

# Команда /daily
def daily(update: Update, context: CallbackContext):
    user_id = update.message.from_user.id
    if user_id not in users:
        update.message.reply_text("Сначала зарегистрируйтесь с помощью /start.")
        return

    today = datetime.date.today()
    if users[user_id]["last_daily"] != today:
        users[user_id]["points"] += 10
        users[user_id]["last_daily"] = today
        update.message.reply_text(f"Вам начислено 10 поинтов! Теперь у вас {users[user_id]['points']} поинтов.")
    else:
        update.message.reply_text("Вы уже получали поинты сегодня.")

# Запуск бота
def main():
    # Вставьте сюда токен вашего бота
    updater = Updater("7723248117:AAGPFMPIkUkF3tE4EdR7cl9m1IG0f6fmPEs")
    dispatcher = updater.dispatcher

    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(CommandHandler("daily", daily))

    updater.start_polling()
    updater.idle()

if __name__ == "__main__":
    main()

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
    updater = Updater("7723248117:AAGPFMPIkUkF3tE4EdR7cl9m1IG0f6fmPEs")
    dispatcher = updater.dispatcher

    dispatcher.add_handler(CommandHandler("start", start))

    updater.start_polling()
    updater.idle()

if __name__ == "__main__":
    main()

from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Updater, CommandHandler, CallbackContext
import sqlite3
import logging
from flask import Flask, request

# Настройка логирования
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# Инициализация базы данных
def init_db():
    conn = sqlite3.connect('bot.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            user_id INTEGER PRIMARY KEY,
            username TEXT,
            referrer_id INTEGER,
            points INTEGER DEFAULT 0
        )
    ''')
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS referrals (
            referral_id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            referred_user_id INTEGER,
            level INTEGER
        )
    ''')
    conn.commit()
    conn.close()

# Сохранение реферала и начисление поинтов
def save_referral(user_id, username, referrer_id):
    conn = sqlite3.connect('bot.db')
    cursor = conn.cursor()

    # Сохраняем пользователя
    cursor.execute('INSERT OR IGNORE INTO users (user_id, username) VALUES (?, ?)', (user_id, username))
    cursor.execute('UPDATE users SET referrer_id = ? WHERE user_id = ?', (referrer_id, user_id))

    # Находим рефереров 1-го, 2-го и 3-го уровней
    level_1 = referrer_id
    cursor.execute('SELECT referrer_id FROM users WHERE user_id = ?', (level_1,))
    level_2 = cursor.fetchone()[0] if cursor.fetchone() else None
    cursor.execute('SELECT referrer_id FROM users WHERE user_id = ?', (level_2,))
    level_3 = cursor.fetchone()[0] if cursor.fetchone() else None

    # Начисляем поинты
    if level_1:
        cursor.execute('INSERT INTO referrals (user_id, referred_user_id, level) VALUES (?, ?, 1)', (level_1, user_id))
        cursor.execute('UPDATE users SET points = points + 5000 WHERE user_id = ?', (level_1,))
    if level_2:
        cursor.execute('INSERT INTO referrals (user_id, referred_user_id, level) VALUES (?, ?, 2)', (level_2, user_id))
        cursor.execute('UPDATE users SET points = points + 2500 WHERE user_id = ?', (level_2,))
    if level_3:
        cursor.execute('INSERT INTO referrals (user_id, referred_user_id, level) VALUES (?, ?, 3)', (level_3, user_id))
        cursor.execute('UPDATE users SET points = points + 1500 WHERE user_id = ?', (level_3,))

    conn.commit()
    conn.close()

# Команда /start
def start(update: Update, context: CallbackContext):
    user_id = update.message.from_user.id
    username = update.message.from_user.username

    logger.info(f"Новый пользователь: ID={user_id}, username={username}")

    # Проверяем, есть ли реферер
    if context.args and context.args[0].startswith("ref"):
        referrer_id = int(context.args[0][3:])  # Извлекаем ID реферера
        logger.info(f"Реферер найден: ID={referrer_id}")
        save_referral(user_id, username, referrer_id)  # Сохраняем реферала
        update.message.reply_text(f"Вы были приглашены пользователем {referrer_id}!")

    # Создаем кнопку для открытия мини-приложения
    keyboard = [
        [InlineKeyboardButton("Открыть мини-приложение", web_app={"url": "https://telegram-bot-ypez.onrender.com"})]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    # Отправляем сообщение с кнопкой
    update.message.reply_text("Нажмите кнопку ниже, чтобы открыть мини-приложение:", reply_markup=reply_markup)

# Команда /points
def points(update: Update, context: CallbackContext):
    user_id = update.message.from_user.id
    conn = sqlite3.connect('bot.db')
    cursor = conn.cursor()
    cursor.execute('SELECT points FROM users WHERE user_id = ?', (user_id,))
    result = cursor.fetchone()
    conn.close()

    if result:
        points = result[0]
        update.message.reply_text(f"Ваши поинты: {points}")
    else:
        update.message.reply_text("Вы еще не зарегистрированы.")

# Команда /referrals
def referrals(update: Update, context: CallbackContext):
    user_id = update.message.from_user.id
    conn = sqlite3.connect('bot.db')
    cursor = conn.cursor()
    cursor.execute('SELECT referred_user_id, level FROM referrals WHERE user_id = ?', (user_id,))
    referrals_list = cursor.fetchall()
    conn.close()

    if referrals_list:
        message = "Ваши рефералы:\n"
        for ref in referrals_list:
            message += f"- Пользователь {ref[0]} (Уровень {ref[1]})\n"
        update.message.reply_text(message)
    else:
        update.message.reply_text("У вас пока нет рефералов.")

# Создаем Flask-приложение
app = Flask(__name__)

@app.route('/webhook', methods=['POST'])
def webhook():
    # Проверяем IP-адрес запроса
    client_ip = request.remote_addr
    allowed_ips = {"100.20.92.101", "44.225.181.72", "44.227.217.144"}

    if client_ip not in allowed_ips:
        logger.warning(f"Доступ запрещен для IP: {client_ip}")
        return 'Forbidden', 403

    try:
        update = Update.de_json(request.get_json(force=True), updater.bot)
        dispatcher.process_update(update)
        return 'ok'
    except Exception as e:
        logger.error(f"Ошибка при обработке обновления: {e}")
        return 'error', 500

# Основная функция
def main():
    global updater, dispatcher

    try:
        # Инициализация базы данных
        init_db()

        # Укажите ваш токен бота
        updater = Updater("7943667357:AAHAWLqXTdpkfXjjlbgNmeNUSnJGUSVXbVI", use_context=True)
        dispatcher = updater.dispatcher

        # Регистрация обработчиков команд
        dispatcher.add_handler(CommandHandler("start", start))
        dispatcher.add_handler(CommandHandler("points", points))
        dispatcher.add_handler(CommandHandler("referrals", referrals))

        # Установка вебхука
        updater.start_webhook(listen="100.20.92.101", port=443, url_path="7943667357:AAHAWLqXTdpkfXjjlbgNmeNUSnJGUSVXbVI")
        updater.bot.set_webhook("https://telegram-bot-ypez.onrender.com/webhook")

        # Запуск Flask-приложения
        app.run(host='0.0.0.0', port=443)
    except Exception as e:
        logger.critical(f"Критическая ошибка: {e}")

if __name__ == "__main__":
    main()

import sqlite3

def init_db():
    conn = sqlite3.connect('bot.db')  # Создаем файл базы данных
    cursor = conn.cursor()

    # Создаем таблицу users
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            user_id INTEGER PRIMARY KEY,
            username TEXT,
            referrer_id INTEGER,
            points INTEGER DEFAULT 0
        )
    ''')

    # Создаем таблицу referrals
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS referrals (
            referral_id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            referred_user_id INTEGER,
            level INTEGER
        )
    ''')

    conn.commit()  # Сохраняем изменения
    conn.close()  # Закрываем соединение

# Запускаем создание базы данных
init_db()

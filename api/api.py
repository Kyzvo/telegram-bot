from flask import Flask, jsonify, request
import sqlite3

app = Flask(__name__)

# Функция для получения данных пользователя
def get_user_data(user_id):
    conn = sqlite3.connect('bot.db')
    cursor = conn.cursor()

    # Получаем данные пользователя
    cursor.execute('SELECT points, referrer_id FROM users WHERE user_id = ?', (user_id,))
    user_data = cursor.fetchone()

    if not user_data:
        conn.close()
        return None

    points, referrer_id = user_data

    # Получаем рефералов
    cursor.execute('SELECT referred_user_id, level FROM referrals WHERE user_id = ?', (user_id,))
    referrals = cursor.fetchall()

    conn.close()

    return {
        'points': points,
        'referral_link': f"https://t.me/your_bot?start=ref{user_id}",
        'referrals': [{'user_id': ref[0], 'level': ref[1]} for ref in referrals]
    }

# Маршрут для получения данных пользователя
@app.route('/api/user', methods=['GET'])
def user():
    user_id = request.args.get('user_id')  # Получаем user_id из запроса
    if not user_id:
        return jsonify({'error': 'user_id is required'}), 400

    user_data = get_user_data(int(user_id))
    if not user_data:
        return jsonify({'error': 'User not found'}), 404

    return jsonify(user_data)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
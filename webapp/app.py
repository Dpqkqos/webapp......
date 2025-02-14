from flask import Flask, render_template, request, jsonify
import sqlite3
from datetime import datetime

app = Flask(__name__)

# Подключение к базе данных SQLite
def get_db_connection():
    conn = sqlite3.connect('database.db')
    conn.row_factory = sqlite3.Row
    return conn

# Инициализация базы данных
def init_db():
    conn = get_db_connection()
    conn.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id TEXT UNIQUE,
            role TEXT
        )
    ''')
    conn.execute('''
        CREATE TABLE IF NOT EXISTS states (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id TEXT,
            date TEXT,
            state TEXT,
            recommendation TEXT,
            FOREIGN KEY (user_id) REFERENCES users (user_id)
        )
    ''')
    conn.commit()
    conn.close()

init_db()

@app.route('/client/<user_id>', methods=['GET', 'POST'])
def client(user_id):
    if request.method == 'POST':
        state = request.form.get('state')
        date = datetime.now().strftime('%Y-%m-%d')
        conn = get_db_connection()
        conn.execute('INSERT INTO states (user_id, date, state) VALUES (?, ?, ?)', (user_id, date, state))
        conn.commit()
        conn.close()
        return jsonify({'status': 'success'})
    
    conn = get_db_connection()
    user_state = conn.execute('SELECT * FROM states WHERE user_id = ? ORDER BY id DESC LIMIT 1', (user_id,)).fetchone()
    conn.close()
    return render_template('index.html', user_state=user_state)

@app.route('/advisor/<advisor_id>', methods=['GET'])
def advisor(advisor_id):
    conn = get_db_connection()
    clients = conn.execute('SELECT user_id FROM users WHERE role = "client"').fetchall()
    states = []
    for client in clients:
        client_state = conn.execute('SELECT * FROM states WHERE user_id = ? ORDER BY id DESC LIMIT 1', (client['user_id'],)).fetchone()
        if client_state:
            states.append(client_state)
    conn.close()
    return render_template('advisor.html', states=states)

@app.route('/update_recommendation', methods=['POST'])
def update_recommendation():
    user_id = request.form.get('user_id')
    recommendation = request.form.get('recommendation')
    conn = get_db_connection()
    conn.execute('UPDATE states SET recommendation = ? WHERE user_id = ? AND recommendation IS NULL', (recommendation, user_id))
    conn.commit()
    conn.close()
    return jsonify({'status': 'success'})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
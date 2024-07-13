from flask import Flask, request, jsonify, g, render_template, redirect, url_for
import sqlite3
import os

app = Flask(__name__)
DATABASE = 'tasks.db'

def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(DATABASE)
    return db

@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/register', methods=['POST'])
def register():
    data = request.form
    email = data['email']
    password = data['password']
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute('INSERT INTO usuarios (email, senha) VALUES (?, ?)', (email, password))
    conn.commit()
    return redirect(url_for('index'))

@app.route('/login', methods=['POST'])
def login():
    data = request.form
    email = data['email']
    password = data['password']
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM usuarios WHERE email = ? AND senha = ?', (email, password))
    user = cursor.fetchone()
    if user:
        return redirect(url_for('tasks', user_id=user[0]))
    else:
        return "Invalid credentials!", 401

@app.route('/tasks/<int:user_id>', methods=['GET', 'POST'])
def tasks(user_id):
    if request.method == 'POST':
        data = request.form
        task = data['task']
        due_date = data['due_date']
        conn = get_db()
        cursor = conn.cursor()
        cursor.execute('INSERT INTO tarefas (userId, tarefa, dataVencimento, concluida) VALUES (?, ?, ?, ?)', (user_id, task, due_date, False))
        conn.commit()
        return redirect(url_for('tasks', user_id=user_id))
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM tarefas WHERE userId = ?', (user_id,))
    tasks = cursor.fetchall()
    return render_template('tasks.html', tasks=tasks, user_id=user_id)

@app.route('/task/<int:task_id>/<int:user_id>', methods=['POST'])
def update_task(task_id, user_id):
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute('UPDATE tarefas SET concluida = 1 WHERE id = ?', (task_id,))
    conn.commit()
    return redirect(url_for('tasks', user_id=user_id))

@app.route('/task/delete/<int:task_id>/<int:user_id>', methods=['POST'])
def delete_task(task_id, user_id):
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute('DELETE FROM tarefas WHERE id = ?', (task_id,))
    conn.commit()
    return redirect(url_for('tasks', user_id=user_id))

if __name__ == '__main__':
    app.run(debug=True)

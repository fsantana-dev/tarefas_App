import sqlite3

def init_db():
    conn = sqlite3.connect('tasks.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS usuarios (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            email TEXT NOT NULL UNIQUE,
            senha TEXT NOT NULL
        )
    ''')
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS tarefas (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            userId INTEGER,
            tarefa TEXT NOT NULL,
            dataVencimento TEXT NOT NULL,
            concluida BOOLEAN NOT NULL,
            FOREIGN KEY (userId) REFERENCES usuarios (id)
        )
    ''')
    conn.commit()
    conn.close()

if __name__ == '__main__':
    init_db()
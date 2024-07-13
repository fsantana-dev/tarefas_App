import sqlite3

conn = sqlite3.connect('tasks.db')
cursor = conn.cursor()

cursor.execute('''
CREATE TABLE IF NOT EXISTS usuarios (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    email TEXT NOT NULL,
    senha TEXT NOT NULL
)
''')

cursor.execute('''
CREATE TABLE IF NOT EXISTS tarefas (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    userId INTEGER NOT NULL,
    tarefa TEXT NOT NULL,
    dataVencimento TEXT NOT NULL,
    concluida BOOLEAN NOT NULL DEFAULT 0,
    FOREIGN KEY (userId) REFERENCES usuarios(id)
)
''')

conn.commit()
conn.close()

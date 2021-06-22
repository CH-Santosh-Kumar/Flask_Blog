import sqlite3

connection = sqlite3.connect('database.db')

with open('schema.sql') as f:
    connection.executescript(f.read())

cur = connection.cursor()

cur.execute("INSERT INTO posts (title, content) VALUES (?, ?)",
            ('First Post','We are trying to create website.')
            )

cur.execute("INSERT INTO posts (title,content) VALUES (?, ?)",
            ('Second Post','We are using Flask, SQLite and Jinja for this.')
            )

connection.commit()
connection.close()
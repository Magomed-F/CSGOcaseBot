import sqlite3


def create_table():
    with sqlite3.connect('core/db/database.db') as db:
        cursor = db.cursor()
        cursor.execute('''CREATE TABLE IF NOT EXISTS support(
                       ID INTEGER,
                       message TEXT,
                       message_id INTEGER)''')
        db.commit()


def add_message(id, message, message_id):
    with sqlite3.connect('core/db/database.db') as db:
        cursor = db.cursor()
        cursor.execute('''INSERT INTO support (ID, message, message_id) VALUES (?, ?, ?)''',
                       (id, message, message_id))
        db.commit()


def get_message() -> list:
    with sqlite3.connect('core/db/database.db') as db:
        cursor = db.cursor()
        cursor.execute('''SELECT * FROM support''')
        data = cursor.fetchall()
        return data


def del_message(message_id):
    with sqlite3.connect('core/db/database.db') as db:
        cursor = db.cursor()
        cursor.execute('''DELETE FROM support WHERE message_id = (?)''',
                       (message_id, ))
        db.commit()


create_table()
import sqlite3


def create_table() -> None:
    with sqlite3.connect('core/db/database.db') as db:
        cursor = db.cursor()
        cursor.execute('''CREATE TABLE IF NOT EXISTS prices(
                       skin TEXT,
                       price FLOAT)''')
        db.commit()


def add_price(name, price):
    with sqlite3.connect('core/db/database.db') as db:
        cursor = db.cursor()
        cursor.execute('''INSERT INTO prices (skin, price) VALUES (?, ?)''',
                       (name, price))
        db.commit()





create_table()
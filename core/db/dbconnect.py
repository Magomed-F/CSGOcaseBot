import sqlite3


def create_table() -> None:
    with sqlite3.connect('core/db/database.db') as db:
        cursor = db.cursor()
        cursor.execute('''CREATE TABLE IF NOT EXISTS users(
                       ID INTEGER,
                       Рефералов INTEGER,
                       Баланс FLOAT)''')
        db.commit()


def new_user_add_func(id) -> None:
    with sqlite3.connect('core/db/database.db') as db:
        cursor = db.cursor()
        cursor.execute('''INSERT INTO users (ID, "Рефералов", "Баланс") VALUES (?, ?, ?)''',
                       (id, 0, 0))
        db.commit()


def get_user_data_func(id) -> list:
    with sqlite3.connect('core/db/database.db') as db:
        cursor = db.cursor()
        cursor.execute('''SELECT * FROM users WHERE ID = (?)''',
                       (id, ))
        data = cursor.fetchall()
        user_data = []
        for dt in data[0]:
            user_data.append(dt)

        return user_data
    

def get_all_id() -> list:
    with sqlite3.connect('core/db/database.db') as db:
        cursor = db.cursor()
        cursor.execute('''SELECT ID FROM users''')
        tuples = cursor.fetchall()
        ids = []
        for id in tuples:
            ids.append(id[0])

        return ids
    

def balance_down(user_id, amount):
    with sqlite3.connect('core/db/database.db') as db:
        cursor = db.cursor()
        cursor.execute('''UPDATE users SET "Баланс" = "Баланс" - (?) WHERE ID = (?)''',
                       (amount, user_id))
        db.commit()
    

def referals_up_func(id) -> None:
    with sqlite3.connect('core/db/database.db') as db:
        cursor = db.cursor()
        cursor.execute('''UPDATE users SET "Рефералов" = "Рефералов" + 1, "Баланс" = "Баланс" + 2.5 WHERE id = (?)''',
                       (id, ))
        db.commit()




create_table()
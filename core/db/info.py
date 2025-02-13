import sqlite3 


def create_table() -> None:
    with sqlite3.connect('core/db/database.db') as db:
        cursor = db.cursor()
        cursor.execute('''CREATE TABLE IF NOT EXISTS info(
                       users INTEGER DEFAULT 0,
                       withdraws INTEGER DEFAULT 0)''')
        db.commit()


def add_user() -> None:
    with sqlite3.connect('core/db/database.db') as db:
        cursor = db.cursor()
        cursor.execute('''UPDATE info SET users = users + 1''')
        db.commit()


def get_data() -> list:
    with sqlite3.connect('core/db/database.db') as db:
        cursor = db.cursor()
        cursor.execute('''SELECT * FROM info''')
        data_list = cursor.fetchall()
        info = []
        for data in data_list[0]:
            info.append(data)
        return info


def add_withdraw(amount) -> None:
    with sqlite3.connect('core/db/database.db') as db:
        cursor = db.cursor()
        cursor.execute('''UPDATE info SET withdraws = withdraws + (?)''',
                       (amount,))
        db.commit()

    
create_table()
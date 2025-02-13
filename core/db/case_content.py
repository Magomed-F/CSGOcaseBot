import sqlite3 


def create_case(case_name) -> None:
    with sqlite3.connect('core/db/database.db') as db:
        cursor = db.cursor()
        cursor.execute(f'''CREATE TABLE IF NOT EXISTS {case_name}(
                       skin TEXT,
                       chance TEXT,
                       skin_price TEXT,
                       ID INTEGER PRIMARY KEY AUTOINCREMENT)''')
        db.commit()


def add_case_content(name, skin, chance, price):
    with sqlite3.connect('core/db/database.db') as db:
        cursor = db.cursor()
        cursor.execute(f'INSERT INTO {name} (skin, chance, skin_price) VALUES (?, ?, ?)',
                       (skin, chance, price))
        db.commit()


def get_case_content(case_name) -> list:
    with sqlite3.connect('core/db/database.db') as db:
        cursor = db.cursor()
        cursor.execute(f'''SELECT * FROM {case_name}''')
        data = cursor.fetchall()
        return data
    

def get_total_chance(case_name) -> float:
    with sqlite3.connect('core/db/database.db') as db:
        cursor = db.cursor()
        cursor.execute(f'''SELECT (chance) FROM {case_name}''')
        total_chance = 0
        lst = cursor.fetchall()

        for chance in lst:
            total_chance += float(chance[0])

        return total_chance


def del_all_content(case_name):
    with sqlite3.connect('core/db/database.db') as db:
        cursor = db.cursor()
        cursor.execute(f'''DELETE FROM {case_name} WHERE 1=1''')
        db.commit()


def del_case_content(case_name, skin):
    with sqlite3.connect('core/db/database.db') as db:
        cursor = db.cursor()
        cursor.execute(f'''DELETE FROM {case_name} WHERE ID = (?)''',
                       (skin,))
        db.commit()



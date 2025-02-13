import sqlite3


def create_table() -> None:
    with sqlite3.connect('core/db/database.db') as db:
        cursor = db.cursor()
        cursor.execute('''CREATE TABLE IF NOT EXISTS cases_data(
                       case_name TEXT,
                       price INTEGER)''')
        db.commit()


def add_case(case_name, price):
    with sqlite3.connect('core/db/database.db') as db:
        cursor = db.cursor()
        cursor.execute('''INSERT INTO cases_data (case_name, price) VALUES (?, ?)''',
                       (case_name, price))
        db.commit()


def get_cases() -> list:
    with sqlite3.connect('core/db/database.db') as db:
        cursor = db.cursor()
        cursor.execute('''SELECT * FROM cases_data''')
        list_of_tuples = cursor.fetchall()
        cases = []
        for case in list_of_tuples:
            cases.append(case)
        db.commit()
        return cases
    

def get_case_price(case_name):
    with sqlite3.connect('core/db/database.db') as db:

        cursor = db.cursor()
        cursor.execute('''SELECT * FROM cases_data WHERE case_name = (?)''',
                       (case_name, ))
        
        lst = cursor.fetchall()
        price = 0

        for data in lst:
            price = float(data[1])
        
        return price
    

def del_case(case_name):
    with sqlite3.connect('core/db/database.db') as db:
        cursor = db.cursor()
        cursor.execute('''DELETE FROM cases_data WHERE case_name = (?)''',
                       (case_name,))
        cursor.execute(f'''DROP TABLE IF EXISTS [{case_name}]''')
        db.commit()


create_table()
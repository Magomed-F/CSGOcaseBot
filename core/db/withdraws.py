import sqlite3 


def create_table() -> None:
    with sqlite3.connect('core/db/database.db') as db:
        cursor = db.cursor()
        cursor.execute('''CREATE TABLE IF NOT EXISTS withdraws(
                       ID INTEGER,
                       name TEXT)''')
        db.commit()



def get_withdraws() -> list:
    with sqlite3.connect('core/db/database.db') as db:
        cursor = db.cursor()
        cursor.execute('''SELECT * FROM withdraws''')
        list_of_tuples = cursor.fetchall()
        withdraws = []
        for withdraw in list_of_tuples:
            withdraws.append(withdraw)

        db.commit()
        return withdraws
        


create_table()
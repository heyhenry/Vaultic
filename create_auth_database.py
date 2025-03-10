import sqlite3

connection = sqlite3.connect("db/auth.db")
cursor = connection.cursor()

create_table_statement = '''
CREATE TABLE IF NOT EXISTS authentication (
    desc TEXT,
    hash TEXT
);
'''

cursor.execute(create_table_statement)

connection.close()
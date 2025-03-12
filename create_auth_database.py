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

# insert default info for desc with an empty value for hash upon initial creation
default_details_statement = "INSERT INTO authentication (desc, hash) values ('master_password', '')"

cursor.execute(default_details_statement)

connection.commit()

connection.close()
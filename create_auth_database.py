import sqlite3

# open auth.db else create auth.db if it doesn't exist
connection = sqlite3.connect("db/auth.db")
cursor = connection.cursor()

# create the auth table
create_table_statement = '''
CREATE TABLE IF NOT EXISTS authentication (
    desc TEXT,
    hash TEXT,
    salt TEXT
);
'''
# execute above statement
cursor.execute(create_table_statement)

# insert default info for desc with an empty value for hash upon initial creation
default_details_statement = "INSERT INTO authentication (desc, hash, salt) values ('master_password', '', '')"

# execute above statement
cursor.execute(default_details_statement)

connection.commit()

connection.close()
import sqlite3

def create_passwords_database():
    # establish a connection to an existing database, or create database
    connection = sqlite3.connect("db/pw_manager.db")
    # create a pointer reference to invoke methods (i.e. queries, statements incl. fetching data)
    cursor = connection.cursor()

    # create an 'accounts' table if it doesn't already exists
    create_table_statement = '''
    CREATE TABLE IF NOT EXISTS accounts (
        account_name TEXT,
        username TEXT,
        password TEXT
    );
    '''

    # execute statement to create an 'accounts' table
    cursor.execute(create_table_statement)

    # not needed if this file is solely to create a database
    # forces sqlite to forcefully update the changes
    sync_changes_statement = "PRAGMA synchronous = FULL;"
    connection.execute(sync_changes_statement)


    # close database connection
    connection.close()
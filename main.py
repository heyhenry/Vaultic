import argon2
import sqlite3
from authmanager import AuthManager
from create_password_database import create_passwords_database
from create_auth_database import create_auth_database
import os
import pandas as pd

PASSWORD_DATABASE_FILENAME = "db/pw_manager.db"
DUMP_FILENAME = "db/password_db.sql"
ENCRYPTED_DUMP_FILENAME = "db/enc_password_db.sql"

def main():

    # create both a 'db' directory and the auth database if auth database doesn't exist
    if not os.path.exists("db/auth.db"):
        if not os.path.exists("db"):
            os.mkdir("db")
        create_auth_database()

    # create the auth object instance
    auth = AuthManager()

    # welcome message
    print("[[[ Welcome to Valutic ]]]")

    # if a valid hash is found in the auth.db, proceed to ask for the password and verify
    if auth.get_stored_hash():
        try:
            # prompt user password
            input_password = input("Enter your Master Password: ")
            
            # verify the entered password
            if auth.verify_master_password(input_password):

                # process to check each level of db manipulation is working accordingly
                print("[Welcome to Vaultic]")

                # create connection to the pw_manager.db
                connection = sqlite3.connect("db/pw_manager.db")

                # decrypt the enc_dump and recreate the database for use
                if os.path.exists(ENCRYPTED_DUMP_FILENAME):
                    auth.decrypt_dump()

                # pretty display of database contents
                print(pd.read_sql_query("SELECT * FROM accounts", connection))

                # press any key to complete program usage
                input("\nPress 'any' button to exit program.")

                # must close the connection, so the encrypt function can run properly, as it opens its own connection to the pw_manager.db
                connection.close()
        except KeyboardInterrupt:
            connection.close()
            auth.encrypt_dump()

    # if a valid hash is not found in the auth.db, proceed to ask user for a new master password and store in auth.db
    else:
        # prompt user to create a master password
        master_password = input("Enter a New Master Password: ")

        # setup and store the master password and salt in auth.db
        auth.set_master_password(master_password)

        # create the initial pw_manager.db
        create_passwords_database()

        # create dump file of pw_manager.db and encrypt it
        auth.encrypt_dump()

        # process to check each level of db manipulation is working accordingly
        print("Accessing pw database?")
        print("1. Yes")
        print("2. No")
        choice = int(input("Enter choice: "))

        # decrpy the data and create pw_manager.db if user wants to access the database
        if choice == 1:
            auth.decrypt_dump()
            input("Press 'any' button to exit program")

    # always re-encrypt file before program closes if dump file is not encrypted
    if not os.path.exists(ENCRYPTED_DUMP_FILENAME):
        auth.encrypt_dump()

    # close the database after usage
    auth.close_database()

if __name__ == "__main__":
    main()
    # try:
    #     main()
    # except KeyboardInterrupt:
    #     auth = AuthManager()
    #     auth.encrypt_dump()
import argon2
import sqlite3
from authmanager import AuthManager
from create_password_database import create_passwords_database
from create_auth_database import create_auth_database
import os

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
    # prompt user password
    input_password = input("Enter your Master Password: ")
    # verify the entered password
    auth.verify_master_password(input_password)

# if a valid hash is not found in the auth.db, proceed to ask user for a new master password and store in auth.db
else:
    master_password = input("Enter a New Master Password: ")
    auth.set_master_password(master_password)
    create_passwords_database()
    auth.create_dump()

# close the database after usage
auth.close_database()
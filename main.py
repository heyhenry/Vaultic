import argon2
import sqlite3
from authmanager import AuthManager

# create the auth object instance
auth = AuthManager()

# welcome message
print("[[[ Welcome to Valutic ]]]")

# if a valid hash is found in the auth.db, proceed to ask for the password and verify
if auth.get_stored_hash():
    input_password = input("Enter your Master Password: ")
    auth.verify_master_password(input_password)
# if a valid hash is not found in the auth.db, proceed to ask user for a new master password and store in auth.db
else:
    master_password = input("Enter a New Master Password: ")
    auth.set_master_password(master_password)

# close the database after usage
auth.close_database()
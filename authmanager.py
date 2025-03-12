import sqlite3
import argon2

class AuthManager:
    def __init__(self):
        # store db filepath
        self.db_path = "db/auth.db"
        # create argon2 object instance
        self.ph = argon2.PasswordHasher()
        # connect to the database and create object intance for sqlite3.connection
        self.connection = sqlite3.connect(self.db_path)
        # create cursor object instance for sqlite3.cursor
        self.cursor = self.connection.cursor()
        
    def get_stored_hash(self):
        # get the value for the hash from auth.db
        get_master_password_query = "SELECT hash FROM authentication WHERE rowid = 1"
        self.cursor.execute(get_master_password_query)
        result = self.cursor.fetchone()
        # return boolean result based on whether a valid hash exists
        if result[0] == '':
            return False
        return True

    def set_master_password(self, master_password):
        # hash the new master password
        hashed_master_password = self.ph.hash(master_password)

        # update the value for hash in the auth.db
        insert_new_master_password = "UPDATE authentication SET hash = ? WHERE rowid = 1"
        self.cursor.execute(insert_new_master_password, (hashed_master_password,))
        # save changes
        self.connection.commit()

    def verify_master_password(self, input_password):
        # get the hashed string for the master password
        get_hashed_master_password = "SELECT hash FROM authentication WHERE rowid = 1"
        self.cursor.execute(get_hashed_master_password)
        result = self.cursor.fetchone()
        hashed_master_password = result[0]

        # check if the passwords match against each other
        try:
            self.ph.verify(hashed_master_password, input_password)
            print("Successfully accessed your vault!")
        except argon2.exceptions.VerifyMismatchError:
            print("Unsuccessful accessing your vault.")

    # close the database connection
    def close_database(self):
        self.connection.close()
import sqlite3
import argon2
import os
from cryptography.fernet import Fernet
from base64 import urlsafe_b64encode

PASSWORD_DATABASE_FILENAME = "db/pw_manager.db"
DUMP_FILENAME = "db/password_db.sql"
ENCRYPTED_DUMP_FILENAME = "db/enc_password_db.sql"

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
        self.enc_key = None
        
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
        self.generate_salt()
        self.generate_encryption_key(self.kdf(master_password))

    def generate_salt(self):
        # create a new salt
        generate_salt = "UPDATE authentication SET salt = ? WHERE rowid = 1"
        # generate randomised string size of 16 bytes
        self.cursor.execute(generate_salt, (os.urandom(16),))
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
            # generate encryption key with kdf as basis
            self.generate_encryption_key(self.kdf(input_password))
            return True
            
        except argon2.exceptions.VerifyMismatchError:
            print("Unsuccessful accessing your vault.")
            return False

    def kdf(self, password):
        # get the stored salt value
        get_salt = "SELECT salt FROM authentication WHERE rowid = 1"
        self.cursor.execute(get_salt)
        salt = self.cursor.fetchone()
        salt = salt[0]
        # ensure password has been converted to bytes aka binary
        password = password.encode()
        
        # create the kdf
        kdf = argon2.low_level.hash_secret_raw(
            secret=password,
            salt=salt,
            time_cost=3,
            memory_cost=65536,
            parallelism=1,
            hash_len=32,
            type=argon2.Type.ID
        )
        return kdf
    
    def generate_encryption_key(self, kdf):
        # encode to url safe base64 as per requirement for fernot keys
        encoded_kdf = urlsafe_b64encode(kdf)
        # create and set the encryption key
        self.enc_key = Fernet(encoded_kdf)

    def delete_dump(self, filename):
        if os.path.exists(filename):
            os.remove(filename)

    def delete_database(self):
        if os.path.exists(PASSWORD_DATABASE_FILENAME):
            os.remove(PASSWORD_DATABASE_FILENAME)

    def create_dump(self):
        if os.path.exists(PASSWORD_DATABASE_FILENAME):
            pw_connection = sqlite3.connect(PASSWORD_DATABASE_FILENAME)
        with open(DUMP_FILENAME, 'w') as outfile:
            for line in pw_connection.iterdump():
                outfile.write(f"{line}\n")
        pw_connection.close()
        self.delete_database()

    def encrypt_dump(self):
        self.create_dump()
        with open(DUMP_FILENAME, 'rb') as file:
            data = file.read()
            encrypted_data = self.enc_key.encrypt(data)
            with open(ENCRYPTED_DUMP_FILENAME, 'wb') as outfile:
                outfile.write(encrypted_data)
        os.remove(DUMP_FILENAME)

    def decrypt_dump(self):
        if os.path.exists(ENCRYPTED_DUMP_FILENAME):
            with open (ENCRYPTED_DUMP_FILENAME, 'rb') as file:
                enc_data = file.read()
                decrypted_data = self.enc_key.decrypt(enc_data)
                with open(DUMP_FILENAME, 'wb') as outfile:
                    outfile.write(decrypted_data)
        os.remove(ENCRYPTED_DUMP_FILENAME)
        self.recreate_database()

    def recreate_database(self):
        with open(DUMP_FILENAME, 'r') as file:
            sql_script = file.read()
        self.delete_dump(DUMP_FILENAME)
        pw_connection = sqlite3.connect(PASSWORD_DATABASE_FILENAME)
        pw_connection.executescript(sql_script)
        pw_connection.commit()
        pw_connection.close()

    # close the database connection
    def close_database(self):
        self.connection.close()
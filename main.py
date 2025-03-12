import argon2
import sqlite3

connection = sqlite3.connect("db/auth.db")
cursor = connection.cursor()

# check database to see if a master password has been set
get_password_query = "SELECT hash FROM authentication"
cursor.execute(get_password_query)
result = cursor.fetchone()
password_found = False
if result[0] != '':
    password_found = True

if password_found:
    print("Enter your master password: ")
else:
    # prompt user to enter a new master password
    master_password = input("Enter new master password: ")
    print(f"master password: {master_password}")

    # hash the new master password
    ph = argon2.PasswordHasher()
    hashed_master_password = ph.hash(master_password)
    print(f"hashed master password: {hashed_master_password}")
    
    # insert the new master password into the authentication database
    insert_new_password = "UPDATE authentication SET hash = ? WHERE rowid = 1"
    cursor.execute(insert_new_password, (hashed_master_password,))
    connection.commit()

connection.close()

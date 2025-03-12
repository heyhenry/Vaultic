import argon2
import sqlite3

# currently stored hash is for the string literal pw: Peekaboo (verificaiton is case sensitive!)

connection = sqlite3.connect("db/auth.db")
cursor = connection.cursor()

ph = argon2.PasswordHasher()

# check database to see if a master password has been set
get_password_query = "SELECT hash FROM authentication"
cursor.execute(get_password_query)
result = cursor.fetchone()
password_found = False
if result[0] != '':
    password_found = True

if password_found:
    input_password = input("Enter your master password: ")

    # retrieve the master password's hash
    get_hashed_master_password = "SELECT hash FROM authentication WHERE rowid = 1"
    cursor.execute(get_hashed_master_password)
    result = cursor.fetchone()
    result_master_password = result[0]
    # print(result_master_password)

    # verify password against stored hash to see if password is correct
    try:
        ph.verify(result_master_password, input_password)
        print("CONGRATLATIONS!! YOU'VE ENTERED YOUR VAULT SUCCESSFULLY!!!!!")
    except argon2.exceptions.VerifyMismatchError:
        print("Your input password does not match the given master password!")
else:
    # prompt user to enter a new master password
    master_password = input("Enter new master password: ")
    print(f"master password: {master_password}")

    # hash the new master password
    hashed_master_password = ph.hash(master_password)
    print(f"hashed master password: {hashed_master_password}")
    
    # insert the new master password into the authentication database
    insert_new_password = "UPDATE authentication SET hash = ? WHERE rowid = 1" # safer than f"" which is susceptible to sql injection attacks
    cursor.execute(insert_new_password, (hashed_master_password,))
    connection.commit()

connection.close()

import argon2
import sqlite3

connection = sqlite3.connect("db/auth.db")
cursor = connection.cursor()

# first git commit 
# check database to see if a master password has been set
get_password_query = "SELECT hash FROM authentication"
cursor.execute(get_password_query)
result = cursor.fetchone()
password_found = False
if result[0] != '':
    password_found = True

connection.close()

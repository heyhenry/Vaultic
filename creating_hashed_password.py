# credit: https://github.com/python-code-camp/Hashing-Python-for-Password-Security/blob/main/main.py

import argon2

# sample password
password = "MySecurePassword"

# Create a PasswordHasher object
ph = argon2.PasswordHasher()

# Hash the password using Argon2
hashed_password = ph.hash(password)
print("Hashed Password:", hashed_password)

# Authenticate the password
input_password = "MySecurePassword"


# the try-except block is required, since an incorrect password input will come up with an exceptions error, namely: MismatchError
try: 
    ph.verify(hashed_password, input_password)
    print("Password verified successfully!")
except argon2.exceptions.VerifyMismatchError:
    print("Password verification failed.")
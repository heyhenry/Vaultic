# Key Derivation Function to generate encryption key for the database
# credits: https://argon2-cffi.readthedocs.io/en/stable/api.html#argon2.low_level.Type, 
import argon2
import os

# we are using the raw string password as the secret
sample_password = b"MySecurePassword"
salt = os.urandom(16)

kdf = argon2.low_level.hash_secret_raw(
    secret=sample_password,
    salt=salt,
    # higher the iteration, the securer it is so brute force attacks, standard is 3-5, increase time taken for brute force attack
    time_cost=3, 
    # 8kb is too weak, 64MB (65536) provides more security and is the standard and reduces hash computation speed
    memory_cost=65536,
    parallelism=1,
    # hash_len of 32 bytes to equate for 256bit key requirement
    hash_len=32,
    type=argon2.Type.ID
)

# check byte length of the kdf key
print(len(kdf))

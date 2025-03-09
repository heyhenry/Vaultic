# Brainstorming ideas and implementation suggestions/features for Vaultic

# Features to Add:
- Strong Password Generator
- Security (Encryption)
    - Potentially during transit
    - Passwords
    - Storage Files of Passwords
    - Usage of fernet symmetric encryption/decryption recipe (fernet has aes components)
- Password Protected App (potentially also a username/email)
- Saved Data:
    - Account Name
    - Username/Email
    - Password
- Add Acction Option
- Delete Account Option
- Re/Generate Password Option
- Recovery Option? (Beyond Current Scope)
- 2FA Login Option? (Beyond Current Scope)
- Cloud Storage (i.e. SQLite Cloud) (Beyond Current Scope)
- Database storage (SQLite)

# Password Requirements
- User generated passwords must be at least 8 characters long, auto-generated passwords must be at least 6 characters log. (NIST 2023 guidelines)
- Maxiumum password length of 64 characterse (NIST 2023 guidelines)
- Passwords should include special characters, and avoid banned characters (i.e. emojis and spaces) (NIST 2023 guidelines)
- No password complexity recommended, just use ASCII characters (NIST 2023 guidelines)

# Password Security Design
- Using Argon2 for Master Password Hashing 
    - Because its slow, so it will make brute force attacks even slower amongst other attacks
    - Because it has won the password hashing competition, making it a known and publicly reputable hashing algorithm
    - Because it provides better resistance than its previous hashing algorithm comrades, like Bcrypt
- Using Fernot's Symmetric Encryption
    - Because it is a widely used, accepted and reputable encryption technique
    - Because it is a standard encryption option used globally
    - Because it is easy to understand and implement (especially for a first timer)
    - Because it is enough for this kind of project, other options such as Asymmetric, Block and Stream Ciphers can be seen as being potentially overkill 

# Security process
1. Ask user for initial input for master password
    - Implement validation to ensure password is within certain range of characters and uses select characters
    - Implement validation to ensure password is valid (non-empty string or space only string)
2. Hash the given master password
    - Store the password hash in a sqlite.db file
3. Generate encryption key based on hashed password and salt, once password login was successful
4. use encryption key to decrypt the sqlite database
5. when application closes, encrypt the sqlite database again

6. Repeat steps 3-5 for every next interaction with the password manager
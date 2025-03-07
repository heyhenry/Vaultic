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
- 
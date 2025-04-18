# queries to the password manager database
PW_SELECT_ALL_ROWID_ACCOUNT_NAME_USERNAME = "SELECT rowid, account_name, username FROM accounts"
PW_SELECT_ALL_DETAILS = "SELECT * FROM accounts WHERE account_name=? AND username=?"
PW_UPDATE_PASSWORD = "UPDATE accounts SET password=? WHERE account_name=? AND username=?"
PW_REMOVE_ACCOUNT = "DELETE FROM accounts WHERE account_name=? AND username=?"
PW_ADD_ACCOUNT = "INSERT INTO accounts (account_name, username, password) VALUES (?, ?, ?)"
PW_UPDATE_ACCOUNT_DETAILS = "UPDATE accounts SET account_name=?,username=?,password=? WHERE account_name=? AND username=?"
PW_SELECT_ALL_ACCOUNT_NAMES = "SELECT account_name FROM accounts"

# queries to the authentication database
AUTH_GET_HASH = "SELECT hash FROM authentication WHERE rowid = 1"
AUTH_INSERT_NEW_MASTER_PASSWORD = "UPDATE authentication SET hash = ? WHERE rowid = 1"
AUTH_SET_SALT = "UPDATE authentication SET salt = ? WHERE rowid = 1"
AUTH_GET_SALT = "SELECT salt FROM authentication WHERE rowid = 1"
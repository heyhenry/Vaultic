# queries to the password database
PW_SELECT_ALL_ACCOUNT_NAME_USERNAME = "SELECT account_name, username FROM accounts"
PW_SELECT_ALL_DETAILS = "SELECT * FROM accounts WHERE account_name=? AND username=?"
PW_UPDATE_PASSWORD = "UPDATE accounts SET password=? WHERE account_name=? AND username=?"
PW_REMOVE_ACCOUNT = "DELETE FROM accounts WHERE account_name=? AND username=?"
PW_ADD_ACCOUNT = "INSERT INTO accounts (account_name, username, password) VALUES (?, ?, ?)"
PW_UPDATE_ACCOUNT_DETAILS = "UPDATE accounts SET account_name=?,username=?,password=? WHERE account_name=? AND username=?"
# To add to the vaultic app before publishing a new release.. 
### Changes occuring after receiving feedback from beta testers and further personal testing.

## Changes yet to implement 
- regarding 'generate new password' on the home page..  (contemplating on implementing or leaving as is, as toast notifications helps clear action statement)
    - potentially, settig up unique iid for each item in the treeview so app can reference and re-highlight the previous selected item (before the repopulation), so the app can also maintain the account-details section info instead of clearing it.

## Changes so far
- sql lookup variables have been set to str() type because when a treeview repopulates, the sqlite gives the information for data that are digits only as an integer type as it loses the parenthesis when inserted into the database? (lines 400 and 430 amended)
- clicking 'generate new password' on the home page also clears the details section
- Implemented toast notifications to important function actions (removing an account, updating an account, adding new account entry, generating new password for an account via homepage)
- Utilising the usage of the rowid for each item in the sqlite database.
    - Pull that rowid information and attach to the iid of each account item.
- On register page, ensure the 'remember this' text gets a colour change upon cursor hovering over it.
- Don't clear data fields for new_entry and update_entry on error.
    - Potentially reduce/reuse code where possible.
- Refactored show_error_message() to support optional callback execution after displaying the error.
- Adjusted one query and appended a new one in queries.py.
- Eliminated redundant checks for an active connection to the pw database and a valid cursor.
- Update all sql queries and validations where both account_name and username were used to verify, now can stick to just account_name as account_names are unique.
- Implement initial entry field focus in NewEntryPage and EditAccountInfoPage.
- Look for section in code where the username.get() may not be required as the account_name.get() is now a unique identifier.
    - Also just general usage of username and/or password where redundant.
- Include comments for code logic, where required
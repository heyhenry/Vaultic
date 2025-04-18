# To add to the vaultic app before publishing a new release..

## Changes so far
- sql lookup variables have been set to str() type because when a treeview repopulates, the sqlite gives the information for data that are digits only as an integer type as it loses the parenthesis when inserted into the database? (lines 400 and 430 amended)
- clicking 'generate new password' on the home page also clears the details section


## Changes yet to implement
- regarding 'generate new password' on the home page.. 
    - potentially, settig up unique iid for each item in the treeview so app can reference and re-highlight the previous selected item (before the repopulation), so the app can also maintain the account-details section info instead of clearing it.
- potentially adding lil notifications when account is deleted, update as occurred -> in the form of a toast notification
- BIG ONE: should create a unique id per entry (maybe auto-generated) because users should still be allowed to have duplicate account name and usernames if they wish.
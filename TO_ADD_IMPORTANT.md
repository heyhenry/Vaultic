# To add to the vaultic app before publishing a new release..

## Changes yet to implement 
- regarding 'generate new password' on the home page..  (contemplating on implementing or leaving as is, as toast notifications helps clear action statement)
    - potentially, settig up unique iid for each item in the treeview so app can reference and re-highlight the previous selected item (before the repopulation), so the app can also maintain the account-details section info instead of clearing it.
- Disallowing duplicate account_name naming -> reasons: improve UX, bad logic for bts code functionality.
- Update all sql queries and validations where both account_name and username were used to verify, now can stick to just account_name as account_names are unique.
- On register page, ensure the 'remember this' text gets a colour change upon cursor hovering over it
    - maybe also a tooltip saying: "Learn why!"

## Changes so far
- sql lookup variables have been set to str() type because when a treeview repopulates, the sqlite gives the information for data that are digits only as an integer type as it loses the parenthesis when inserted into the database? (lines 400 and 430 amended)
- clicking 'generate new password' on the home page also clears the details section
- Implemented toast notifications to important function actions (removing an account, updating an account, adding new account entry, generating new password for an account via homepage)
- Utilising the usage of the rowid for each item in the sqlite database.
    - Pull that rowid information and attach to the iid of each account item


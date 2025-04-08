# todo next

# priority read
- updated requirements.txt x
- tidy up and remove files that dont need to be apart of final product
- work on the readme (alot done, wip)
    - download section
- update the app's taskbar icon (done on creation of executable, add favicon line to it)
- create executable

# self notes to detail later in readme
- regarding passwords:
    - they allow unicode
    - they allow 64 characters
    - they allow spaces in the passwords (just not whitespacesalone)
    - users can go beyond even 64 characters if they wish for their passwords
    - a separte box is opened when editing an account to provide another layer of security, it is better than it all being shown on the homepage and also cuts the requirement to add unmasking feature within the accessed application.

# Done (START):
- clear the homepage's details section if logged out. 
- put sql queries into a constant block or another file and import into vaultic.py 
    - pw_manager queries 
    - auth queries 
- update the toast notification's default icon with app logo
- work on the readme (alot done, wip)
    - future implementation/roadmap section? i.e. add dark theme 
    - add links to the badges 
    - add final resource.md path link 
- add LICENSE 
- add hovering tooltips for different functions? i.e. logout, copy 
- create utils for common functions like toast 
- submain_logos fix up 
    - remove unused submain_logos  
    - rename used submain logos 
    - apply renamed submain_logos where code references them 
- create snapshots of the apps different pages and different states (errors, masked passwords) 
- create the markdown file that displays snapshots 
- Get more version of vaultic_logo_5 but like different poses for different pages 
    - editaccountpage  
- turn the 'remember this' on the register page to a clickable hyperlink to a webpage about the why you should remember your password and how master passwords work for password managers (i.e. if you forget it, gg) 
- Updated password generation algorithm to exclude the trickier punctuations 
- Maybe get more version of vaultic_logo_5 but like different poses for different pages
    - registerpage 
    - loginpage 
    - homepage 
    - newentrypage 
- get an logo for vaultic and apply 
- make sure all windows are uniformly placed so user doesnt have to travel around the screen with fingers and eyes so much.
- reduce the error display time for login atleast
- center windows
- disable ability to resize windows
- provide a logout and close option 
- potentially add a copy button next to passwords 
    - implement a toast notification when copied 
- implement toggleable password masking for login (with default state as masked) 
- increase fontsize in treeview and font style 
- Reconfigure the widget's sizes based on main branches untouched font code displaying the correct font size.
    - Setup customised font/size styles 
    - LoginPage 
    - RegisterPage 
    - HomePage 
    - EditAccountPage 
    - NewEntryPage 
- Look into ttkbootstrap for UI design usage x
- fix up treeview 
    - dont allow user to drag the heading 
    - update the font/size 
    - potentially update the size of the widget 
- Update to a good font (maybe back to helvetica or something else) 
- ensure everything is gucci with the transition to ttkbootstrap and then proceed to implement the new features 
- reduce/reorg code
    - remove lambda uses if possible 
    - renamed frame/frames to page/pages/current_page 
- trigger deselection behaviour if the cursor clicks anywhere outside of the treeview (buttons are dealt with already) 
- update functions where binds are used if possible 
- create strong password requirement for master password registration 
- potentially fix up homepage's call functions i.e. new_entry calls are all done from a single function rather than some done via binding and some via functions  
    - hint.. usage of event=None 
- find the limit of password length and what happens if so. (how to restrict at a certain point) 
- fix the checker when trying to click remove account and theres no details given ( was just a type on password_var not having the .get() func)  
- bug to fix: if account is selected, then edited, we need the account_details information to disappear when edit_account is clicked 
- bug to fix: make the 'edit account details' do nothing if no information is filled in account details section 
- bug to fix: create focus highlight or w/e when an item is selected in the accounts list 
    - remove the highlight when taken off the page or account list is updated 
        - if highlight is gone, so is the information in the account details section? 
- Implement logic to the details buttons 
    - Edit Account (Create a pop-up like new entry? or retain entry fields enablement) 
        - validation for edited entry attempt 
        - update the database in realtime 
        - update the homepage's accounts_list in realtime 
- Change clear_all() functions that clear entry widgets to re-setting the textvarialbes instead 
- create wireframe for edit entry 
- create wireframe for home_v2 
- create wireframe for latest home page 
- Re-Place the details widgets 
- Work on the get_selected_details via treeview and display it in the details section 
- Implement logic to the details buttons
    - Generate New Password (Immediately update the entry field for password and treeview display) 
    - Delete Entry (Immediate deletion thats reflected in the treeview display) 
- bug fix to do: when clicking on an item in the treeview and then creating a new entry, upon completing the creation of a new entry, IndexError: string index out of range occurs via the get_account_details() function. Namely the line underscored is 'account_name = self.accounts_list.item(selection)["values"][0]' 

# Done (END):

-------
- Create the listbox that'll host the different accounts in the password database on the homepage x
    - Ensure the listbox has scrollability x
- Create the details display section on the homepage
- Implement the ability to edit the information via the details display section
    - Ensure the user is able to highlight and copy without needing to go into edit mode   
    - Potentially have the data displayed inside a locked entry widget that will get unlocked in edit mode
    - Write the algorithm to update the information 
    - Maybe create the edit mode buttons similar to BetterLife Bio Section
    - Ability to update the password via the generate_password button without going into edit mode, but also in edit mode





# todo LATER
- Change the function name: show_frame to show_page? x
- incorporate proper password requirements for master password later x
- find a way to deal with ctrl+c and unexcepted crashes not being prompted to encrypt the database (LATER) ** UPDATE: NOT NEEDED COS TKINTER APPS WONT ALLOW USERS TO CTRL+C SINCE ITS GUI NOT CLI
- potentially dealing with curly braces display in the listbox for account_name values ** UPDATE: NOT RELEVANT ANYMORE SINCE IM USING TREEVIEW
    - this happens on tkinter's side.. 
        - characters that trigger the curly braces include: 
            - spaces
            - parenthesis
            - brackets
            - dollar signs
            - semicolons, quotes, backslashes
            - anything that might confuse tcl's command parser
    - solution is to replace the output during the listbox.insert() process
        - i.e. listbox.insert(tk.END, f'{item_name.replace("(", "").replace(")", "")}')
- Serious consideration of using Mixin Class to promote DRY, i.e. the clear_all and error_message which can be inherited alongside tk.Frame for the child classes.
- Potential for backup data dumps in the case of corrupted files?
- Potentially add an entirely different window that exclusively just has a static message when the app has some software error and to contact suppor team.
- Github actions ci/cd implementation? potentially makes me a strong candidate for devops.


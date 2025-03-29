import tkinter as tk
from tkinter import ttk
import sqlite3
from authmanager import AuthManager
from create_password_database import create_passwords_database
from create_auth_database import create_auth_database
import os
import pandas as pd
from password_generation import generate_password

class Windows(tk.Tk):
    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)

        # check for auth database's existence
        self.check_auth_exists()

        # create auth obj ref
        self.auth = AuthManager()

        # db connection vars
        self.pw_connection = None
        self.pw_cursor = None

        # creating a window's title
        self.wm_title = ("Test Applicaiton")
    
        # creating a  frame and assigning it to container
        container = tk.Frame(self, height=400, width=600)
        # specifying the region where the frame is packed in root
        container.pack(side="top", fill="both", expand=True)

        # configuring the location of the container using grid
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        # we will now create a dictionary of frames
        self.frames = {}
        # we'll create the frames themselves later but let's add the components to the dictionary
        for F in (LoginPage, RegisterPage, HomePage, NewEntryPage, EditAccountPage):
            frame = F(container, self)

            # the windows class acts as the root window for the frames
            self.frames[F] = frame
            frame.grid(row=0, column=0, sticky="nswe")

        # determine initial page display upon program startup
        if self.auth.get_stored_hash():
            self.show_frame(LoginPage)
            # self.show_frame(HomePage)
        else:
            self.show_frame(RegisterPage)

        self.protocol("WM_DELETE_WINDOW", self.on_close)

    # display selected page
    def show_frame(self, page):
        frame = self.frames[page]

        # withdraw to avoid flckering of previous page
        self.withdraw()
        self.geometry("480x340") # general defaulted window size for all pages (temporary)
        if page == RegisterPage or page == LoginPage:
            # self.geometry("480x340")
            if page == RegisterPage:
                self.after(100, lambda: frame.password_entry.focus())
            else:
                # timer added due to tkinter event processing isn't instantaenous(spelling?)
                self.after(100, lambda: frame.password_entry.focus())
        elif page == HomePage:
            self.geometry("800x700")
            frame.populate_accounts_list()

        # raises the current frame to the top
        frame.tkraise()
        # ensures immediate update
        self.update_idletasks()

        # deiconify to show only the updated window
        self.deiconify()

    # check if an authentication database exists 
    def check_auth_exists(self):
        if not os.path.exists("db/auth.db"):
            if not os.path.exists("db"):
                os.mkdir("db")
            create_auth_database()

    # re-encrypts the passwords database whenever app is closed
    def on_close(self):
        # temp log
        print('closing..')
        # check if the pw_manager database is exposed
        if os.path.exists('db/pw_manager.db'):
            # close current connection to the pw_manager database
            if self.pw_connection:
                self.pw_connection.close()
            # re-encrypt the pw_manager database
            self.auth.encrypt_dump()
        self.destroy()

class LoginPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        self.password_var = tk.StringVar()
        self.create_widgets()

    def create_widgets(self):
        app_title = tk.Label(self, text="Vaultic", font=("helvetica", 24))
        password_subtitle = tk.Label(self, text="Enter Password:", font=("helvetica", 18))
        self.password_entry = tk.Entry(self, font=("helvetica", 24), width=18, textvariable=self.password_var)
        self.error_message = tk.Label(self, foreground="red", font=("helvetica", 12))
        login_submission = tk.Button(self, text="Login", font=("helvetica", 18), command=self.process_password)

        app_title.place(x=200, y=30)
        password_subtitle.place(x=80, y=110)
        self.password_entry.place(x=80, y=150)
        self.error_message.place(x=150, y=190)
        login_submission.place(x=200, y=220)

        # detect 'Enter' keybind press
        self.password_entry.bind("<Return>", lambda event: self.process_password())

    def clear_all(self):
        self.password_entry.delete(0, "end")
        self.error_message.config(text="")

    def show_error_message(self):
        self.error_message.config(text="Invalid Password! Try again.")
        self.after(3000, self.clear_all)

    def process_password(self):
        if self.controller.auth.verify_master_password(self.password_var.get()):
            print('yessir')
            self.controller.auth.decrypt_dump()
            self.controller.pw_connection = sqlite3.connect("db/pw_manager.db")
            self.controller.pw_cursor = self.controller.pw_connection.cursor()
            self.controller.show_frame(HomePage)
        else:
            self.show_error_message()

class RegisterPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        self.password_var = tk.StringVar()
        self.confirm_password_var = tk.StringVar()
        self.error_type = None
        self.create_widgets()

    def create_widgets(self):
        app_title = tk.Label(self, text="Vaultic", font=("helvetica", 24))
        desc_subtitle = tk.Label(self, text="Create Your Master Password", font=("helvetica", 18))
        password_subtitle = tk.Label(self, text="Enter Password:", font=("helvetica", 14))
        self.password_entry = tk.Entry(self, font=("helvetica", 18), width=25, textvariable=self.password_var)
        confirm_password_subtitle = tk.Label(self, text='Confirm Password:', font=("helvetica", 14))
        self.confirm_password_entry = tk.Entry(self, font=("helvetica", 18), width=25, textvariable=self.confirm_password_var)
        self.error_message = tk.Label(self, foreground='red', font=("helvetica", 10))
        create_submission = tk.Button(self, text="Create", font=("helvetica", 18), command=self.process_password_creation)
        reminder_message = tk.Label(self, text="Remember This!", font=("helvetica", 12))

        app_title.place(x=200, y=10)
        desc_subtitle.place(x=80, y=50)
        password_subtitle.place(x=80, y=90)
        self.password_entry.place(x=80, y=120)
        confirm_password_subtitle.place(x=80, y=160)
        self.confirm_password_entry.place(x=80, y=190)
        self.error_message.place(x=130, y=220)
        create_submission.place(x=180, y=240)
        reminder_message.place(x=330, y=300)

        # detect 'enter' keybind regardless of which entry field has focus
        self.password_entry.bind("<Return>", lambda event: self.process_password_creation())
        self.confirm_password_entry.bind("<Return>", lambda event: self.process_password_creation())

    def validate_password_creation(self):
        if self.password_var.get() != self.confirm_password_var.get():
            self.error_type = "Password Mismatch"
            return False
        elif self.password_var.get().isspace():
            self.error_type = "Whitespaces Only"
            return False
        elif len(self.password_var.get()) == 0:
            self.error_type = "Empty Password"
            return False
        return True
    
    def clear_all(self):
        self.error_message.config(text="")
        self.password_entry.delete(0, "end")
        self.confirm_password_entry.delete(0, "end")

    def show_error_message(self):
        self.error_message.config(text=f"Invalid Password! {self.error_type}.")
        # timed error message and wipe in use, as this tasks should encourage the user to pay full attention due to its high security risk "WRITE THIS IN THE readme.md under design choice?"
        self.after(3000, self.clear_all)

    def process_password_creation(self):
        if self.validate_password_creation():
            # update the authentication database's information with new; pw, hashing, salt
            self.controller.auth.set_master_password(self.password_var.get())
            # create the initial pw_manager database
            create_passwords_database()
            self.controller.auth.encrypt_dump()
            self.controller.auth.decrypt_dump()
            # create a connection to the pw_manager database
            self.controller.pw_connection = sqlite3.connect("db/pw_manager.db")
            self.controller.pw_cursor = self.controller.pw_connection.cursor()
            self.controller.show_frame(HomePage)
        else:
            self.show_error_message()

class HomePage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        self.account_name_var = tk.StringVar()
        self.account_username_var = tk.StringVar()
        self.account_password_var = tk.StringVar()
        self.create_widgets()

    def create_widgets(self):
        title = tk.Label(self, text="Home", font=("Helvetica", 24))
        new_entry = tk.Button(self, text="New Account [+]", font=("Helvetica", 12), command=lambda: self.controller.show_frame(NewEntryPage))

        self.accounts_list = ttk.Treeview(self, columns=("account_name", "account_username"), show="headings", height=10, selectmode='browse')
        self.accounts_list.heading("account_name", text="Account Name")
        self.accounts_list.heading("account_username", text="Username")
        self.accounts_list.column("account_name", width=300)
        self.accounts_list.column("account_username", width=300)

        title.place(x=350, y=10)
        new_entry.place(x=600, y=10)

        self.accounts_list.place(x=100, y=80)

        # # right
        details_subtitle = tk.Label(self, text="Account Details:", font=("Helvetica", 24))
        account_name_subtitle = tk.Label(self, text="Name:", font=("Helvetica", 18))
        account_username_subtitle = tk.Label(self, text="Username:", font=("Helvetica", 18))
        account_password_subtitle = tk.Label(self, text="Password:", font=("Helvetica", 18))
        account_name_entry = tk.Entry(self, textvariable=self.account_name_var, state='readonly', font=("Helvetica", 18))
        account_username_entry = tk.Entry(self, textvariable=self.account_username_var, state='readonly', font=("Helvetica", 18))
        account_password_entry = tk.Entry(self, textvariable=self.account_password_var, state='readonly', font=("Helvetica", 18))
        remove_account_button = tk.Button(self, text="Remove Account", font=("Helvetica", 14), command=self.remove_account)
        edit_account_details_button = tk.Button(self, text="Edit Account Details", font=("Helvetica", 14), command=self.edit_account_info)
        generate_password_button = tk.Button(self, text="Generate New Password", font=("Helvetica", 14), command=self.generate_new_password)

        details_subtitle.place(x=275, y=325)
        account_name_subtitle.place(x=200, y=400)
        account_username_subtitle.place(x=200, y=450)
        account_password_subtitle.place(x=200, y=500)
        account_name_entry.place(x=400, y=400)
        account_username_entry.place(x=400, y=450)
        account_password_entry.place(x=400, y=500)
        remove_account_button.place(x=100, y=575)
        edit_account_details_button.place(x=290, y=575)
        generate_password_button.place(x=500, y=575)
        
        self.accounts_list.bind("<<TreeviewSelect>>", self.get_account_details)

    # fill the accounts list with stored account names
    def populate_accounts_list(self):
        # delete all items stored in the accounts_list
        self.accounts_list.delete(*self.accounts_list.get_children())
        # run query to the database to fetch all latest accounts and their information 
        # and store into the accounts list
        if self.controller.pw_connection:
            sql_query = "SELECT account_name, username FROM accounts"
            self.controller.pw_cursor.execute(sql_query)
            result = self.controller.pw_cursor.fetchall()
            if result:
                for account_info in result:
                    self.accounts_list.insert("", "end", values=account_info)

    def get_account_details(self, event):
        # select an account from the accounts_list
        selection = self.accounts_list.focus()
        # store the account's name and username respectively for future referencing
        account_name = self.accounts_list.item(selection)["values"][0]
        account_username = self.accounts_list.item(selection)["values"][1]
        # run query to fetch account information from the database
        sql_query = "SELECT account_name,username,password FROM accounts WHERE account_name=? AND username=?"
        self.controller.pw_cursor.execute(sql_query, (account_name, account_username))
        result = self.controller.pw_cursor.fetchall()
        # set the account variables for details display based on selected account
        self.account_name_var.set(result[0][0])
        self.account_username_var.set(result[0][1])
        self.account_password_var.set(result[0][2])
        # deselect the item after setting variables, to clear selection index
        self.accounts_list.selection_remove(selection)

    def generate_new_password(self):
        # only generate password if an account was selected
        if self.account_name_var.get() or self.account_username_var.get() or self.account_password_var.get():
            # create a new password
            new_password = generate_password()
            # run query to update the password value for the given account
            update_password_query = "UPDATE accounts SET password=? WHERE account_name=? AND username=?"
            self.controller.pw_cursor.execute(update_password_query, (new_password, self.account_name_var.get(), self.account_username_var.get()))
            self.controller.pw_connection.commit()
            # update display's password value in tkinter
            self.account_password_var.set(new_password)
            # update the accounts list
            self.populate_accounts_list()

    def remove_account(self):
        # only remove account if an account was selected
        if self.account_name_var.get() or self.account_username_var.get() or self.account_password_var():
            # get account unique identifiers
            selection = self.accounts_list.focus()
            account_name = self.accounts_list.item(selection)["values"][0]
            account_username = self.accounts_list.item(selection)["values"][1]
            # run sql query to delete the selected account from the database
            remove_account_query = "DELETE FROM accounts WHERE account_name=? AND username=?"
            self.controller.pw_cursor.execute(remove_account_query, (account_name, account_username))
            self.controller.pw_connection.commit()
            # reset all details related variables
            self.account_name_var.set("")
            self.account_username_var.set("")
            self.account_password_var.set("")
            # update the accounts list
            self.populate_accounts_list()

    def edit_account_info(self):
        # trigger a call for EditAccountPage's values to be update based on the selected account in HomePage
        self.controller.frames[EditAccountPage].get_account_info()
        # redirect to the EditAccountPage window
        self.controller.show_frame(EditAccountPage)

class NewEntryPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        self.account_name_var = tk.StringVar()
        self.username_var = tk.StringVar()
        self.password_var = tk.StringVar()
        self.create_widgets()

    def create_widgets(self):
        title = tk.Label(self, text="New Account Entry", font=("Helvetica", 18))
        account_name_subtitle = tk.Label(self, text="Account Name:", font=("Helvetica", 12))
        self.account_name_entry = tk.Entry(self, textvariable=self.account_name_var, font=("Helvetica", 12), width=20)
        username_subtitle = tk.Label(self, text="Username:", font=("Helvetica", 12))
        self.username_entry = tk.Entry(self, textvariable=self.username_var, font=("Helvetica", 12), width=20)
        password_subtitle = tk.Label(self, text="Password:", font=("Helvetica", 12))
        self.password_entry = tk.Entry(self, textvariable=self.password_var, font=("Helvetica", 12), width=20)
        generate_password_button = tk.Button(self, text="Generate", font=("Helvetica", 10), command=self.create_password)
        self.error_message = tk.Label(self, foreground="red", font=("Helvetica", 10))
        add_entry_button = tk.Button(self, text="Add", font=("Helvetica", 14), width=10, command=self.validate_new_entry)
        cancel_entry_button = tk.Button(self, text="Cancel", font=("Helvetica", 14), width=10, command=self.cancel_entry)

        title.place(x=150, y=30)    
        account_name_subtitle.place(x=80, y=100)
        self.account_name_entry.place(x=200, y=100)
        username_subtitle.place(x=80, y=150)
        self.username_entry.place(x=200, y=150)
        password_subtitle.place(x=80, y=200)
        self.password_entry.place(x=200, y=200)
        generate_password_button.place(x=400, y=197)
        self.error_message.place(x=120, y=225)
        add_entry_button.place(x=80, y=250)
        cancel_entry_button.place(x=250, y=250)
        
    # generate a randomised password if prompted
    def create_password(self):
        self.password_var.set(generate_password())
    
    # check if user has entered a valid account entry
    def validate_new_entry(self):
        # ensure all fields have data
        if len(self.account_name_var.get()) > 0 and len(self.username_var.get()) > 0 and len(self.password_var.get()) > 0:
            self.create_entry()
        else:
            self.show_error_message()

    # display the error message
    def show_error_message(self):
        self.error_message.config(text="Error: All fields must be filled.")
        self.after(3000, self.clear_all)

    # clear all entry fields and the error message
    def clear_all(self):
        self.error_message.config(text="")
        self.account_name_entry.delete(0, "end")
        self.username_entry.delete(0, "end")
        self.password_entry.delete(0, "end")

    # create a new account entry and store in the pw_manager database
    def create_entry(self):
        # sql query to add a new valid account entry
        sql_query = "INSERT INTO accounts (account_name, username, password) VALUES (?, ?, ?)"
        # checker to ensure that there is an active connection to the pw_manager database
        if self.controller.pw_cursor:
            self.controller.pw_cursor.execute(sql_query, (self.account_name_var.get(), self.username_var.get(), self.password_var.get()))
            # save changes to the pw_manager database
            self.controller.pw_connection.commit()
            # clean out data fields prior to page redirect
            self.clear_all()
            # return user to the homepage after entry is added
            self.controller.show_frame(HomePage)
        # hidden issue logger for dev
        # technically, should never be procced, as a database connection commences the moment the user is logged into the account.
        else:
            print("Trouble: 'pw_cursor' is None")

    # cancels the process of creating a new account entry
    def cancel_entry(self):
        # ensure all data fields are cleaned
        self.clear_all()
        # redirect to the homepage
        self.controller.show_frame(HomePage)

class EditAccountPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        self.account_name_var = tk.StringVar()
        self.username_var = tk.StringVar()
        self.password_var = tk.StringVar()
        self.current_account_name_var = tk.StringVar()
        self.current_username_var = tk.StringVar()
        self.create_widgets()

    def create_widgets(self):
        title = tk.Label(self, text="Edit Account Info", font=("Helvetica", 18))
        account_name_subtitle = tk.Label(self, text="Account Name:", font=("Helvetica", 12))
        self.account_name_entry = tk.Entry(self, textvariable=self.account_name_var, font=("Helvetica", 12), width=20)
        username_subtitle = tk.Label(self, text="Username:", font=("Helvetica", 12))
        self.username_entry = tk.Entry(self, textvariable=self.username_var, font=("Helvetica", 12), width=20)
        password_subtitle = tk.Label(self, text="Password:", font=("Helvetica", 12))
        self.password_entry = tk.Entry(self, textvariable=self.password_var, font=("Helvetica", 12), width=20)
        generate_password_button = tk.Button(self, text="Generate", font=("Helvetica", 10), command=self.create_password)
        self.error_message = tk.Label(self, foreground="red", font=("Helvetica", 10))
        add_entry_button = tk.Button(self, text="Add", font=("Helvetica", 14), width=10, command=self.validate_account_info)
        cancel_entry_button = tk.Button(self, text="Cancel", font=("Helvetica", 14), width=10, command=self.cancel_entry)

        title.place(x=150, y=30)    
        account_name_subtitle.place(x=80, y=100)
        self.account_name_entry.place(x=200, y=100)
        username_subtitle.place(x=80, y=150)
        self.username_entry.place(x=200, y=150)
        password_subtitle.place(x=80, y=200)
        self.password_entry.place(x=200, y=200)
        generate_password_button.place(x=400, y=197)
        self.error_message.place(x=120, y=225)
        add_entry_button.place(x=80, y=250)
        cancel_entry_button.place(x=250, y=250)

    def create_password(self):
        self.password_var.set(generate_password())
    
    def validate_account_info(self):
        if len(self.account_name_var.get()) > 0 and len(self.username_var.get()) > 0 and len(self.password_var.get()) > 0:
            self.update_entry()
        else:
            self.show_error_message()
    
    def show_error_message(self):
        self.error_message.config(text="Error: All fields must be filled.")
        self.after(3000, self.clear_all)
    
    def clear_all(self):
        self.error_message.config(text="")
        self.account_name_entry.delete(0, "end")
        self.username_entry.delete(0, "end")
        self.password_entry.delete(0, "end")

    def cancel_entry(self):
        self.clear_all()
        self.controller.show_frame(HomePage)     

    def update_entry(self):
        update_account_info_query = "UPDATE accounts SET account_name=?,username=?,password=? WHERE account_name=? AND username=?"
        self.controller.pw_cursor.execute(update_account_info_query, (self.account_name_var.get(), self.username_var.get(), self.password_var.get(), self.current_account_name_var.get(), self.current_username_var.get()))
        self.controller.pw_connection.commit()
        self.clear_all()
        self.controller.show_frame(HomePage)

    def get_account_info(self):
        # pull the values stored for respective variables from the HomePage variable instances
        self.account_name_var.set(self.controller.frames[HomePage].account_name_var.get())
        self.username_var.set(self.controller.frames[HomePage].account_username_var.get())
        self.password_var.set(self.controller.frames[HomePage].account_password_var.get())
        self.current_account_name_var.set(self.controller.frames[HomePage].account_name_var.get())
        self.current_username_var.set(self.controller.frames[HomePage].account_username_var.get())
        

if __name__ == "__main__":
    app = Windows()
    app.mainloop()
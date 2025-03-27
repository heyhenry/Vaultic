import tkinter as tk
from tkinter import ttk
import sqlite3
from authmanager import AuthManager
from create_password_database import create_passwords_database
from create_auth_database import create_auth_database
import os
import pandas as pd

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
        for F in (LoginPage, RegisterPage, HomePage, NewEntryPage):
            frame = F(container, self)

            # the windows class acts as the root window for the frames
            self.frames[F] = frame
            frame.grid(row=0, column=0, sticky="nswe")

        # determine initial page display upon program startup
        if self.auth.get_stored_hash():
            self.show_frame(LoginPage)
            # self.show_frame(NewEntryPage)
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
            frame.refresh_homepage()

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
        self.create_widgets()

    def create_widgets(self):
        title = tk.Label(self, text="HOME PAGE IS HERE")
        new_entry = tk.Button(self, text="New Account [+]", command=lambda: self.controller.show_frame(NewEntryPage))
        self.display_summary = tk.Label(self)
        

        title.place(x=200, y=10)
        new_entry.place(x=350, y=10)
        self.display_summary.place(x=200, y=50)

    # update the homepage with data from database
    def refresh_homepage(self):
        sql_query = "SELECT * FROM accounts"
        self.controller.pw_cursor.execute(sql_query)
        result = self.controller.pw_cursor.fetchall()
        self.display_summary.config(text=result if result else "No records found")

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
        add_entry_button = tk.Button(self, text="Add", font=("Helvetica", 14), width=10, command=self.create_entry)
        cancel_entry_button = tk.Button(self, text="Cancel", font=("Helvetica", 14), width=10)

        title.place(x=150, y=30)    
        account_name_subtitle.place(x=80, y=100)
        self.account_name_entry.place(x=200, y=100)
        username_subtitle.place(x=80, y=150)
        self.username_entry.place(x=200, y=150)
        password_subtitle.place(x=80, y=200)
        self.password_entry.place(x=200, y=200)
        add_entry_button.place(x=80, y=250)
        cancel_entry_button.place(x=250, y=250)
        
    # create a new account entry and store in the pw_manager database
    def create_entry(self):
        # sql query to add a new valid account entry
        sql_query = "INSERT INTO accounts (account_name, username, password) VALUES (?, ?, ?)"
        # checker to ensure that there is an active connection to the pw_manager database
        if self.controller.pw_cursor:
            self.controller.pw_cursor.execute(sql_query, (self.account_name_var.get(), self.username_var.get(), self.password_var.get()))
            # save changes to the pw_manager database
            self.controller.pw_connection.commit()
            # return user to the homepage after entry is added
            self.controller.show_frame(HomePage)
        # hidden issue logger for dev
        else:
            print("Trouble: 'pw_cursor' is None")

if __name__ == "__main__":
    app = Windows()
    app.mainloop()
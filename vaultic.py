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
        for F in (LoginPage, RegisterPage, HomePage):
            frame = F(container, self)

            # the windows class acts as the root window for the frames
            self.frames[F] = frame
            frame.grid(row=0, column=0, sticky="nswe")

        # determine initial page display upon program startup
        if self.auth.get_stored_hash():
            self.show_frame(LoginPage)
        else:
            self.show_frame(RegisterPage)

        self.protocol("WM_DELETE_WINDOW", self.on_close)

    # display selected page
    def show_frame(self, page):
        frame = self.frames[page]

        # withdraw to avoid flckering of previous page
        self.withdraw()
        
        if page == RegisterPage or page == LoginPage:
            self.geometry("480x340")
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
        self.controler = controller
        self.create_widgets()

    def create_widgets(self):
        app_title = tk.Label(self, text="Vaultic", font=("helvetica", 24))
        password_subtitle = tk.Label(self, text="Enter Password:", font=("helvetica", 18))
        password_entry = tk.Entry(self, font=("helvetica", 24), width=18)
        login_submission = tk.Button(self, text="Login", font=("helvetica", 18))

        app_title.place(x=200, y=30)
        password_subtitle.place(x=80, y=110)
        password_entry.place(x=80, y=150)
        login_submission.place(x=200, y=220)

class RegisterPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        self.password_var = tk.StringVar()
        self.confirm_password_var = tk.StringVar()
        self.create_widgets()

    def create_widgets(self):
        app_title = tk.Label(self, text="Vaultic", font=("helvetica", 24))
        desc_subtitle = tk.Label(self, text="Create Your Master Password", font=("helvetica", 18))
        password_subtitle = tk.Label(self, text="Enter Password:", font=("helvetica", 14))
        password_entry = tk.Entry(self, font=("helvetica", 18), width=25)
        confirm_password_subtitle = tk.Label(self, text='Confirm Password:', font=("helvetica", 14))
        confirm_password_entry = tk.Entry(self, font=("helvetica", 18), width=25)
        create_submission = tk.Button(self, text="Create", font=("helvetica", 18), command=self.process_password_creation)
        reminder_message = tk.Label(self, text="Remember This!", font=("helvetica", 12))

        app_title.place(x=200, y=10)
        desc_subtitle.place(x=80, y=50)
        password_subtitle.place(x=80, y=90)
        password_entry.place(x=80, y=120)
        confirm_password_subtitle.place(x=80, y=160)
        confirm_password_entry.place(x=80, y=190)
        create_submission.place(x=180, y=240)
        reminder_message.place(x=330, y=300)

    def validate_password_creation(self):
        if self.password_var.get() == self.confirm_password_var.get():
            return True
        return False

    def process_password_creation(self):
        if self.validate_password_creation():
            self.controller.auth.set_master_password(self.password_var.get())
            create_passwords_database()
            self.controller.auth.encrypt_dump()
            self.controller.auth.decrypt_dump()
            self.controller.pw_connection = sqlite3.connect("db/pw_manager.db")
            self.controller.pw_cursor = self.controller.pw_connection.cursor()
            
            self.controller.show_frame(HomePage)
        else:
            pass
            # display error message and clear fields for retry

class HomePage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        self.create_widgets()

    def create_widgets(self):
        title = tk.Label(self, text="HOME PAGE IS HERE")
        title.pack()
        self.display_summary = tk.Label(self)
        self.display_summary.pack()

    # update the homepage with data from database
    def refresh_homepage(self):
        sql_query = "SELECT * FROM accounts"
        self.controller.pw_cursor.execute(sql_query)
        result = self.controller.pw_cursor.fetchall()
        self.display_summary.config(text=result if result else "No records found")

if __name__ == "__main__":
    app = Windows()
    app.mainloop()
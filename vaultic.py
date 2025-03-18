import tkinter as tk
from tkinter import ttk
import sqlite3
from authmanager import AuthManager
from create_password_database import create_passwords_database
from create_auth_database import create_auth_database
import os
import pandas as pd

class windows(tk.Tk):
    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)

        # check for auth database's existence
        self.check_auth_exists()

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

        self.show_frame(LoginPage)

    # display selected page
    def show_frame(self, page):
        frame = self.frames[page]

        # withdraw to avoid flckering of previous page
        self.withdraw()
        
        if page == RegisterPage or LoginPage:
            self.geometry("480x340")

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
        self.create_widgets()

    def create_widgets(self):
        app_title = tk.Label(self, text="Vaultic", font=("helvetica", 24))
        desc_subtitle = tk.Label(self, text="Create Your Master Password", font=("helvetica", 18))
        password_subtitle = tk.Label(self, text="Enter Password:", font=("helvetica", 14))
        password_entry = tk.Entry(self, font=("helvetica", 18), width=25)
        confirm_password_subtitle = tk.Label(self, text='Confirm Password:', font=("helvetica", 14))
        confirm_password_entry = tk.Entry(self, font=("helvetica", 18), width=25)
        create_submission = tk.Button(self, text="Create", font=("helvetica", 18))
        reminder_message = tk.Label(self, text="Remember This!", font=("helvetica", 12))

        app_title.place(x=200, y=10)
        desc_subtitle.place(x=80, y=50)
        password_subtitle.place(x=80, y=90)
        password_entry.place(x=80, y=120)
        confirm_password_subtitle.place(x=80, y=160)
        confirm_password_entry.place(x=80, y=190)
        create_submission.place(x=180, y=240)
        reminder_message.place(x=330, y=300)

class HomePage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        label = tk.Label(self, text="HomePage")
        label.pack(padx=10, pady=10)

        switch_window_button = tk.Button(
            self, 
            text="Go to the Register Page",
            command=lambda: controller.show_frame(RegisterPage)
        )
        switch_window_button.pack(side="bottom", fill=tk.X)

if __name__ == "__main__":
    app = windows()
    app.mainloop()
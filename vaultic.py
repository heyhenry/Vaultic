import sqlite3
from authmanager import AuthManager
from create_password_database import create_passwords_database
from create_auth_database import create_auth_database
import os
from password_generation import generate_password
import ttkbootstrap as bttk
from ttkbootstrap.constants import *
from PIL import Image, ImageTk
import tkinter as tk
import pyperclip
import random
import webbrowser
from vaultic_utils import show_toast, show_tooltip, print_out

class Windows(bttk.Window):
    def __init__(self, *args, **kwargs):
        bttk.Window.__init__(self, *args, **kwargs)

        # implementing font/sizes and other custom style decisions
        self.selected_font = "Helvetica"
        self.setup_styles()

        # only run toast notification after pending ui works finish loading to avoid top-level quirks
        self.after_idle(self.startup_notification)

        # check for auth database's existence
        self.check_auth_exists()

        # create auth obj ref
        self.auth = AuthManager()

        # db connection vars
        self.pw_connection = None
        self.pw_cursor = None

        # creating a window's title
        self.title("Vaultic")
    
        # creating a  frame and assigning it to container
        container = bttk.Frame(self, height=400, width=600)
        # specifying the region where the frame is packed in root
        container.pack(side="top", fill="both", expand=True)

        # configuring the location of the container using grid
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        # we will now create a dictionary of pages
        self.pages = {}
        # we'll create the pages themselves later but let's add the components to the dictionary
        for P in (LoginPage, RegisterPage, HomePage, NewEntryPage, EditAccountPage):
            page = P(container, self)

            # the windows class acts as the root window for the pages
            self.pages[P] = page
            page.grid(row=0, column=0, sticky="nswe")

        # determine initial page display upon program startup
        if self.auth.get_stored_hash():
            self.show_page(LoginPage)
        else:
            self.show_page(RegisterPage)

        self.protocol("WM_DELETE_WINDOW", self.on_close)

    # display selected page
    def show_page(self, current_page):
        page = self.pages[current_page]

        # withdraw to avoid flckering of previous page
        self.withdraw()

        # setting the titlebar's icon
        titlebar_icon = ImageTk.PhotoImage(Image.open("img/main_logo.png").resize((32, 32), Image.Resampling.LANCZOS))
        self.iconphoto(False, titlebar_icon)
        # default window size
        self.center_window(490, 340)
        self.resizable(False, False)

        if current_page == RegisterPage or current_page == LoginPage:
            # timer added due to tkinter event processing isn't instantaenous(spelling?)
            self.after(100, page.password_entry.focus)
        elif current_page == HomePage:
            self.center_window(800,700)
            # updates the accounts list to the latest version
            # also deselects any pre-existing item selection aka handles deselection logic as all deselections are intertwined with redirecting to the homepage
            page.populate_accounts_list()

        # raises the current frame to the top
        page.tkraise()
        # ensures immediate update
        self.update_idletasks()

        # deiconify to show only the updated window
        self.deiconify()

    # poisiton the window in the middle of the user's screen
    def center_window(self, win_width, win_height):
        x = (self.winfo_screenwidth() // 2) - (win_width // 2)
        y = (self.winfo_screenheight() // 2) - (win_height // 2)
        return self.geometry(f"{win_width}x{win_height}+{x}+{y}")

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

    def setup_styles(self):
        style = bttk.Style(theme="minty")

        # label
        style.configure("CustomF24.TLabel", font=(self.selected_font, 24))
        style.configure("CustomF18.TLabel", font=(self.selected_font, 18))
        style.configure("CustomF14.TLabel", font=(self.selected_font, 14))
        style.configure("CustomF12.TLabel", font=(self.selected_font, 12))
        style.configure("CustomF10.TLabel", font=(self.selected_font, 10))

        # button
        style.configure("CustomF18.TButton", font=(self.selected_font, 18))
        style.configure("CustomF14.TButton", font=(self.selected_font, 14))
        style.configure("CustomF12.TButton", font=(self.selected_font, 12))
        style.configure("CustomF10.TButton", font=(self.selected_font, 10))

        # altered global setting of button's takefocus option
        self.option_add("*TButton*takeFocus", False)

        # treeview
        style.configure("Treeview.Heading", font=(self.selected_font, 18))
        style.configure("Treeview", font=(self.selected_font, 12), rowheight=25)
       
    def startup_notification(self):
        cheeky_messages = [
            "Vaultic reporting for duty... with a smug grin.",
            "Don’t worry, I remember everything. *smiles*",
            "No keys? No problem. I *am* the key.",
            "Your secrets are safe... until you copy-paste them everywhere.",
            "Vaultic here — acting like I’m not judging your passwords.",
            "Ah, the daily dance of pretending we’re secure.",
            "I see you’re back. Hope you remembered *me*, at least.",
            "Loading secrets… don’t peek 👀",
            "Vaultic: Because sticky notes are a crime.",
            "Initializing... 100% sass, 0% breach.",
            "Your secrets are guarded like a Primarch’s gene-seed.",
            "Even the Inquisition couldn’t crack this vault.",
            "By the light of the Astronomican, Vaultic awakens.",
            "I might be a peasant app, but I guard like a royal knight!",
            "My power level? It's over 9000... bits of entropy.",
            "Training complete. Vaultic’s security is Ultra Instinct.",
            "I'm gonna be... the Vault King!",
            "Your secrets are more protected than the One Piece.",
            "You want the top? Then remember your damn password.",
            "Suzu-freakin-ran? Nah. Vaultic runs this school."
        ]
        show_toast("Vaultic is now running", random.choice(cheeky_messages), 5000)

class LoginPage(bttk.Frame):
    def __init__(self, parent, controller):
        bttk.Frame.__init__(self, parent)
        self.controller = controller
        self.password_var = bttk.StringVar()
        self.masked_img = ImageTk.PhotoImage(Image.open("img/pw_masked.png").resize((42, 42), Image.Resampling.LANCZOS))
        self.unmasked_img = ImageTk.PhotoImage(Image.open("img/pw_unmasked.png").resize((42, 42), Image.Resampling.LANCZOS)) 
        self.logo_img = ImageTk.PhotoImage(Image.open("img/main_logo.png").resize((84, 84), Image.Resampling.LANCZOS))
        self.create_widgets()
   
    def create_widgets(self):
        app_logo = bttk.Label(self, image=self.logo_img)
        app_title = bttk.Label(self, text='Vaultic', style="CustomF24.TLabel")
        self.password_entry = bttk.Entry(self, width=18, textvariable=self.password_var, show="*", font=(self.controller.selected_font, 24))
        self.toggle_mask = tk.Button(self, image=self.masked_img, command=self.toggle_masking)
        self.toggle_mask.config(activebackground="#F8F9FA", background="#F8F9FA")
        self.error_message = bttk.Label(self, foreground="red", style="CustomF12.TLabel")
        login_submission = bttk.Button(self, text="Login", command=self.process_password, style="CustomF18.TButton")

        app_logo.place(x=200, y=0)
        app_title.place(x=200, y=90)
        self.password_entry.place(x=80, y=150)
        self.toggle_mask.place(x=425, y=150)
        self.error_message.place(x=150, y=210)
        login_submission.place(x=200, y=240)

        # detect 'Enter' keybind press
        self.password_entry.bind("<Return>", self.process_password)

    def clear_all(self):
        self.error_message.config(text="")
        self.password_var.set("")

    def show_error_message(self):
        self.error_message.config(text="Invalid Password! Try again.")
        self.after(1000, self.clear_all)

    def process_password(self, event=None):
        if self.controller.auth.verify_master_password(self.password_var.get()):
            print('yessir')
            self.controller.auth.decrypt_dump()
            self.controller.pw_connection = sqlite3.connect("db/pw_manager.db")
            self.controller.pw_cursor = self.controller.pw_connection.cursor()
            self.controller.show_page(HomePage)
        else:
            self.show_error_message()

    def toggle_masking(self):
        if self.password_entry.cget("show") == "*":
            self.toggle_mask.config(image=self.unmasked_img)
            self.password_entry.config(show="")
        else:
            self.toggle_mask.config(image=self.masked_img)
            self.password_entry.config(show="*")

class RegisterPage(bttk.Frame):
    def __init__(self, parent, controller):
        bttk.Frame.__init__(self, parent)
        self.controller = controller
        self.password_var = bttk.StringVar()
        self.confirm_password_var = bttk.StringVar()
        self.error_type = None
        self.thumbsup_img = ImageTk.PhotoImage(Image.open("img/submain_logo_3.png").resize((84, 84), Image.Resampling.LANCZOS))
        self.create_widgets()

    def create_widgets(self):
        app_title = bttk.Label(self, text="Vaultic", style="CustomF24.TLabel")
        desc_subtitle = bttk.Label(self, text="Create Your Master Password", style="CustomF18.TLabel")
        password_subtitle = bttk.Label(self, text="Enter Password:", style="CustomF14.TLabel")
        self.password_entry = bttk.Entry(self, width=25, textvariable=self.password_var, font=(self.controller.selected_font, 18))
        confirm_password_subtitle = bttk.Label(self, text='Confirm Password:', style="CustomF14.TLabel")
        self.confirm_password_entry = bttk.Entry(self, width=25, textvariable=self.confirm_password_var, font=(self.controller.selected_font, 18))
        self.error_message = bttk.Label(self, foreground='red', style="CustomF10.TLabel")
        create_submission = bttk.Button(self, text="Create", command=self.process_password_creation, style="CustomF18.TButton")
        reminder_message = bttk.Label(self, text="Remember This!", style="CustomF12.TLabel")
        thumbsup_display = bttk.Label(self, image=self.thumbsup_img)

        app_title.place(x=200, y=10)
        desc_subtitle.place(x=80, y=50)
        password_subtitle.place(x=80, y=90)
        self.password_entry.place(x=80, y=120)
        confirm_password_subtitle.place(x=80, y=170)
        self.confirm_password_entry.place(x=80, y=200)
        self.error_message.place(x=130, y=245)
        create_submission.place(x=180, y=270)
        reminder_message.place(x=330, y=300)
        thumbsup_display.place(x=30, y=250)

        # detect 'enter' keybind regardless of which entry field has focus
        self.password_entry.bind("<Return>", self.process_password_creation)
        self.confirm_password_entry.bind("<Return>", self.process_password_creation)
        reminder_message.bind("<Button-1>", self.open_master_password_info)

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
        elif len(self.password_var.get()) < 8:
            self.error_type = "Minimum Length 8 Characters"
            return False
        return True
    
    def clear_all(self):
        self.error_message.config(text="")
        self.password_var.set("")
        self.confirm_password_var.set("")

    def show_error_message(self):
        self.error_message.config(text=f"Invalid Password! {self.error_type}.")
        # timed error message and wipe in use, as this tasks should encourage the user to pay full attention due to its high security risk "WRITE THIS IN THE readme.md under design choice?"
        self.after(1000, self.clear_all)

    def process_password_creation(self, event=None):
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
            self.controller.show_page(HomePage)
        else:
            self.show_error_message()

    def open_master_password_info(self, event):
        webbrowser.open("https://bitwarden.com/blog/picking-the-right-password-for-your-password-manager/")

class HomePage(bttk.Frame):
    def __init__(self, parent, controller):
        bttk.Frame.__init__(self, parent)
        self.controller = controller
        self.account_name_var = bttk.StringVar()
        self.account_username_var = bttk.StringVar()
        self.account_password_var = bttk.StringVar()
        self.copy_icon = ImageTk.PhotoImage(Image.open("img/copy.png").resize((32, 32), Image.Resampling.LANCZOS))
        self.logout_icon = ImageTk.PhotoImage(Image.open("img/logout.png").resize((48, 48), Image.Resampling.LANCZOS))
        self.logo_icon = ImageTk.PhotoImage(Image.open("img/submain_logo_2.png").resize((84, 84), Image.Resampling.LANCZOS))
        self.attack_img = ImageTk.PhotoImage(Image.open("img/submain_logo_1.png").resize((120, 120), Image.Resampling.LANCZOS))
        self.create_widgets()

    def create_widgets(self):
        title = bttk.Label(self, text="Home", style="CustomF24.TLabel")
        icon_display = bttk.Label(self, image=self.logo_icon)
        new_entry = bttk.Button(self, text="New Account [+]", command=self.new_entry_redirect, style="CustomF12.TButton")

        self.accounts_list = bttk.Treeview(self, columns=("account_name", "account_username"), show="headings", height=7, selectmode='browse')
        self.accounts_list.heading("account_name", text="Account Name", anchor='w')
        self.accounts_list.heading("account_username", text="Username", anchor='w')
        self.accounts_list.column("account_name", width=300, minwidth=300, stretch=False)
        self.accounts_list.column("account_username", width=300, minwidth=300, stretch=False)

        details_subtitle = bttk.Label(self, text="Account Details:", style="CustomF24.TLabel")
        account_name_subtitle = bttk.Label(self, text="Name:", style="CustomF18.TLabel")
        account_username_subtitle = bttk.Label(self, text="Username:", style="CustomF18.TLabel")
        account_password_subtitle = bttk.Label(self, text="Password:", style="CustomF18.TLabel")
        account_name_entry = bttk.Entry(self, textvariable=self.account_name_var, state='readonly', font=(self.controller.selected_font, 18))
        account_username_entry = bttk.Entry(self, textvariable=self.account_username_var, state='readonly', font=(self.controller.selected_font, 18))
        account_password_entry = bttk.Entry(self, textvariable=self.account_password_var, state='readonly', font=(self.controller.selected_font, 18))
        copy_username_button = tk.Button(self, image=self.copy_icon, command=lambda: self.copy_text("copy_username"))
        copy_username_button.config(background="#F8F9FA", activebackground="#F8F9FA")
        copy_password_button = tk.Button(self, image=self.copy_icon, command=lambda: self.copy_text("copy_password"))
        copy_password_button.config(background="#F8F9FA", activebackground="#F8F9FA")
        self.remove_account_button = bttk.Button(self, text="Remove Account", command=self.remove_account, style="CustomF14.TButton")
        self.edit_account_details_button = bttk.Button(self, text="Edit Account Details", command=self.edit_account_info, style="CustomF14.TButton")
        generate_password_button = bttk.Button(self, text="Generate New Password", command=self.generate_new_password, style="CustomF14.TButton")
        logout_button = tk.Button(self, image=self.logout_icon, command=self.logout)
        logout_button.config(background="#F8F9FA", activebackground="#F8F9FA")
        attack_display = bttk.Label(self, image=self.attack_img)

        title.place(x=350, y=10)
        icon_display.place(x=160, y=0)
        new_entry.place(x=550, y=15)

        self.accounts_list.place(x=100, y=80)

        details_subtitle.place(x=275, y=320)
        account_name_subtitle.place(x=200, y=390)
        account_username_subtitle.place(x=200, y=440)
        account_password_subtitle.place(x=200, y=490)
        account_name_entry.place(x=400, y=390)
        account_username_entry.place(x=400, y=440)
        account_password_entry.place(x=400, y=490)
        copy_username_button.place(x=680, y=445)
        copy_password_button.place(x=680, y=495)
        self.remove_account_button.place(x=100, y=585)
        self.edit_account_details_button.place(x=290, y=585)
        generate_password_button.place(x=500, y=585)
        logout_button.place(x=10, y=650)
        attack_display.place(x=30, y=380)
        
        self.accounts_list.bind("<<TreeviewSelect>>", self.get_account_details)
        self.bind("<Button-1>", self.deselect_account)
        copy_username_button.bind("<Enter>", lambda event: show_tooltip(copy_username_button, "Copy Username"))
        copy_password_button.bind("<Enter>", lambda event: show_tooltip(copy_password_button, "Copy Password"))
        logout_button.bind("<Enter>", lambda event: show_tooltip(logout_button, "Logout"))

    def new_entry_redirect(self):
        self.clear_details_section()
        self.controller.show_page(NewEntryPage)

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
        # get the details if there is an active selection
        if selection:
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
        if self.account_name_var.get():
            # get account unique identifiers
            selection = self.accounts_list.focus()
            account_name = self.accounts_list.item(selection)["values"][0]
            account_username = self.accounts_list.item(selection)["values"][1]
            # run sql query to delete the selected account from the database
            remove_account_query = "DELETE FROM accounts WHERE account_name=? AND username=?"
            self.controller.pw_cursor.execute(remove_account_query, (account_name, account_username))
            self.controller.pw_connection.commit()
            # reset all details related variables
            self.clear_details_section()
            # update the accounts list
            self.populate_accounts_list()

    def edit_account_info(self):
        if self.account_name_var.get():
            # trigger a call for EditAccountPage's values to be update based on the selected account in HomePage
            self.controller.pages[EditAccountPage].get_account_info()
            # redirect to the EditAccountPage window
            self.controller.show_page(EditAccountPage)
            # deselect the item when switching to account editing page, to clear selection index
            self.clear_details_section()

    def clear_details_section(self):
        # reset the local account info variables
        self.account_name_var.set("")
        self.account_username_var.set("")
        self.account_password_var.set("")

    def deselect_account(self, event):
        # find the selected item
        selection = self.accounts_list.focus()
        # unhighlight it
        self.accounts_list.selection_remove(selection)
        # deselect the item aka change the string value to an empty string value == nothing is selected
        # None is not viable due to tcl/tk only reading direct strings
        self.accounts_list.focus("")
        # clear existing details that are displayed in the details section
        self.clear_details_section()

    def copy_text(self, pressed_button):
        if pressed_button == "copy_username":
            show_toast("Copied!", "Username has been copied.", 3000)
            # copy the selected info to the user's device's clipboard
            pyperclip.copy(self.account_username_var.get())
        else:
            pyperclip.copy(self.account_password_var.get())
            show_toast("Copied!", "Password has been copied.", 3000)

    def logout(self):
        # temp log
        print('closing..')
        # check if the pw_manager database is exposed
        if os.path.exists('db/pw_manager.db'):
            # close current connection to the pw_manager database
            if self.controller.pw_connection:
                self.controller.pw_connection.close()
            # re-encrypt the pw_manager database
            self.controller.auth.encrypt_dump()
        self.controller.pages[LoginPage].password_var.set("")
        self.controller.show_page(LoginPage)

class NewEntryPage(bttk.Frame):
    def __init__(self, parent, controller):
        bttk.Frame.__init__(self, parent)
        self.controller = controller
        self.account_name_var = bttk.StringVar()
        self.username_var = bttk.StringVar()
        self.password_var = bttk.StringVar()
        self.thumbsup_img = ImageTk.PhotoImage(Image.open("img/submain_logo_4.png").resize((96, 96), Image.Resampling.LANCZOS))
        self.create_widgets()

    def create_widgets(self):
        thumbsup_display = bttk.Label(self, image=self.thumbsup_img)
        title = bttk.Label(self, text="New Account Entry", style="CustomF18.TLabel")
        account_name_subtitle = bttk.Label(self, text="Account Name:", style="CustomF12.TLabel")
        self.account_name_entry = bttk.Entry(self, textvariable=self.account_name_var, width=20, font=(self.controller.selected_font, 12))
        username_subtitle = bttk.Label(self, text="Username:", style="CustomF12.TLabel")
        self.username_entry = bttk.Entry(self, textvariable=self.username_var, width=20, font=(self.controller.selected_font, 12))
        password_subtitle = bttk.Label(self, text="Password:", style="CustomF12.TLabel")
        self.password_entry = bttk.Entry(self, textvariable=self.password_var, width=20, font=(self.controller.selected_font, 12))
        generate_password_button = bttk.Button(self, text="Generate", command=self.create_password, style="CustomF10.TButton")
        self.error_message = bttk.Label(self, foreground="red", style="CustomF10.TLabel")
        add_entry_button = bttk.Button(self, text="Add", width=10, command=self.validate_new_entry, style="CustomF14.TButton")
        cancel_entry_button = bttk.Button(self, text="Cancel", width=10, command=self.cancel_entry, style="CustomF14.TButton")

        thumbsup_display.place(x=30, y=0)
        title.place(x=150, y=30)    
        account_name_subtitle.place(x=80, y=100)
        self.account_name_entry.place(x=200, y=100)
        username_subtitle.place(x=80, y=150)
        self.username_entry.place(x=200, y=150)
        password_subtitle.place(x=80, y=200)
        self.password_entry.place(x=200, y=200)
        generate_password_button.place(x=400, y=200)
        self.error_message.place(x=160, y=235)
        add_entry_button.place(x=80, y=265)
        cancel_entry_button.place(x=250, y=265)
        
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
        self.after(1000, self.clear_all)

    # clear all entry fields and the error message
    def clear_all(self):
        self.error_message.config(text="")
        self.account_name_var.set("")
        self.username_var.set("")
        self.password_var.set("")

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
            self.controller.show_page(HomePage)
        # hidden issue logger for dev
        # technically, should never be procced, as a database connection commences the moment the user is logged into the account.
        else:
            print("Trouble: 'pw_cursor' is None")

    # cancels the process of creating a new account entry
    def cancel_entry(self):
        # ensure all data fields are cleaned
        self.clear_all()
        # redirect to the homepage
        self.controller.show_page(HomePage)

class EditAccountPage(bttk.Frame):
    def __init__(self, parent, controller):
        bttk.Frame.__init__(self, parent)
        self.controller = controller
        self.account_name_var = bttk.StringVar()
        self.username_var = bttk.StringVar()
        self.password_var = bttk.StringVar()
        # hold current values prior to change, for database reference
        self.current_account_name_var = bttk.StringVar()
        self.current_username_var = bttk.StringVar()
        self.lookover_img = ImageTk.PhotoImage(Image.open("img/submain_logo_5.png").resize((96, 96), Image.Resampling.LANCZOS))
        self.create_widgets()

    def create_widgets(self):
        lookover_display = bttk.Label(self, image=self.lookover_img)
        title = bttk.Label(self, text="Edit Account Info", style="CustomF18.TLabel")
        account_name_subtitle = bttk.Label(self, text="Account Name:", style="CustomF12.TLabel")
        self.account_name_entry = bttk.Entry(self, textvariable=self.account_name_var, width=20, font=(self.controller.selected_font, 12))
        username_subtitle = bttk.Label(self, text="Username:", style="CustomF12.TLabel")
        self.username_entry = bttk.Entry(self, textvariable=self.username_var, width=20, font=(self.controller.selected_font, 12))
        password_subtitle = bttk.Label(self, text="Password:", style="CustomF12.TLabel")
        self.password_entry = bttk.Entry(self, textvariable=self.password_var, width=20, font=(self.controller.selected_font, 12))
        generate_password_button = bttk.Button(self, text="Generate", command=self.create_password, style="CustomF10.TButton")
        self.error_message = bttk.Label(self, foreground="red", style="CustomF10.TLabel")
        update_entry_button = bttk.Button(self, text="Update", width=10, command=self.validate_account_info, style="CustomF14.TButton")
        cancel_entry_button = bttk.Button(self, text="Cancel", width=10, command=self.cancel_entry, style="CustomF14.TButton")

        lookover_display.place(x=30, y=0)
        title.place(x=150, y=30)    
        account_name_subtitle.place(x=80, y=100)
        self.account_name_entry.place(x=200, y=100)
        username_subtitle.place(x=80, y=150)
        self.username_entry.place(x=200, y=150)
        password_subtitle.place(x=80, y=200)
        self.password_entry.place(x=200, y=200)
        generate_password_button.place(x=400, y=200)
        self.error_message.place(x=160, y=235)
        update_entry_button.place(x=80, y=265)
        cancel_entry_button.place(x=250, y=265)

    def create_password(self):
        self.password_var.set(generate_password())
    
    def validate_account_info(self):
        if len(self.account_name_var.get()) > 0 and len(self.username_var.get()) > 0 and len(self.password_var.get()) > 0:
            self.update_entry()
        else:
            self.show_error_message()
    
    def show_error_message(self):
        self.error_message.config(text="Error: All fields must be filled.")
        self.after(1000, self.clear_all)
    
    def clear_all(self):
        self.error_message.config(text="")
        self.account_name_var.set("")
        self.username_var.set("")
        self.password_var.set("")

    def cancel_entry(self):
        self.clear_all()
        self.controller.show_page(HomePage)     

    def update_entry(self):
        # run query to update values for selected account
        update_account_info_query = "UPDATE accounts SET account_name=?,username=?,password=? WHERE account_name=? AND username=?"
        self.controller.pw_cursor.execute(update_account_info_query, (self.account_name_var.get(), self.username_var.get(), self.password_var.get(), self.current_account_name_var.get(), self.current_username_var.get()))
        self.controller.pw_connection.commit()
        # clear fields post process
        self.clear_all()
        # redirect to the HomePage
        self.controller.show_page(HomePage)

    def get_account_info(self):
        # pull the values stored for respective variables from the HomePage variable instances
        self.account_name_var.set(self.controller.pages[HomePage].account_name_var.get())
        self.username_var.set(self.controller.pages[HomePage].account_username_var.get())
        self.password_var.set(self.controller.pages[HomePage].account_password_var.get())
        self.current_account_name_var.set(self.controller.pages[HomePage].account_name_var.get())
        self.current_username_var.set(self.controller.pages[HomePage].account_username_var.get())
        
if __name__ == "__main__":
    app = Windows()
    app.mainloop()
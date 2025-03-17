import tkinter as tk
from tkinter import ttk

class windows(tk.Tk):
    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)
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

        self.show_frame(RegisterPage)

    def show_frame(self, page):
        frame = self.frames[page]

        # withdraw to avoid flckering of previous page
        self.withdraw()
        
        if page == RegisterPage:
            self.geometry("480x270")

        # raises the current frame to the top
        frame.tkraise()
        # ensures immediate update
        self.update_idletasks()

        # deiconify to show only the updated window
        self.deiconify()

class LoginPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        label = tk.Label(self, text="LoginPage")
        label.pack(padx=10, pady=10)

        # we use the switch_window_button in order to call the show_frame() method as a lambda function
        switch_window_button = tk.Button(
            self, 
            text="Go to the Home Page",
            command=lambda: controller.show_frame(HomePage)
        )
        switch_window_button.pack(side="bottom", fill=tk.X)

class RegisterPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        self.create_widgets()

    def create_widgets(self):
        app_title = tk.Label(self, text="Vaultic")
        desc_subtitle = tk.Label(self, text="Create Master Your Password")
        password_subtitle = tk.Label(self, text="Enter Password:")
        password_entry = tk.Entry(self)
        confirm_password_subtitle = tk.Label(self, text='Confirm Password:')
        confirm_password_entry = tk.Entry(self)
        create_submission = tk.Button(self)

        app_title.pack()
        desc_subtitle.pack()
        password_subtitle.pack()
        password_entry.pack()
        confirm_password_subtitle.pack()
        confirm_password_entry.pack()
        create_submission.pack()

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
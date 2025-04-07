from ttkbootstrap.constants import *
from ttkbootstrap.toast import ToastNotification
from ttkbootstrap.tooltip import ToolTip


def show_toast(title, message, duration):
    ToastNotification(
        title=title,
        message=message,
        duration=duration
    ).show_toast()

def show_tooltip(widget, text):
    ToolTip(widget=widget, text=text, bootstyle=INFO).show_tip()

def print_out(event=None):
    print("POOP!!")
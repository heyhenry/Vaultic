from ttkbootstrap.constants import *
from ttkbootstrap.toast import ToastNotification
from ttkbootstrap.tooltip import ToolTip

# separeted because it not dependent on any class's widgets
def show_toast(title, message, duration):
    ToastNotification(
        title=title,
        message=message,
        duration=duration
    ).show_toast()

def show_tooltip(widget, text):
    ToolTip(widget=widget, text=text, bootstyle=INFO).show_tip()
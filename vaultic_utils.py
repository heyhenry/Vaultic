from ttkbootstrap.toast import ToastNotification

def show_toast(title, message, duration):
    ToastNotification(
        title=title,
        message=message,
        duration=duration
    ).show_toast()
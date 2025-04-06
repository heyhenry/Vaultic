from ttkbootstrap.toast import ToastNotification

def create_toast(title, message, duration):
    return ToastNotification(
        title=title,
        message=message,
        duration=duration
    ).show_toast()
from tkinter import *

def dashboard():
    dashboard_window = Toplevel()
    dashboard_window.title("Desktop Inventory Management System")
    dashboard_window.geometry("1920x1080")
    dashboard_window.config(bg="#1E1E1E")

    heading = Label(dashboard_window, text="Dashboard", bg="#1E1E1E", fg="White", font=("Georgia",50,"bold")).place(x=750, y=10)

    content_frame = Frame(dashboard_window,bg="#E0E0E0")
    content_frame.place(x=50, y=100, width=1800, height=900)

    sub_heading = Label(content_frame, text="Welcome, Admin!", bg="#E0E0E0", fg="Black", font=("Arial",30,"bold")).place(x=20, y=10)



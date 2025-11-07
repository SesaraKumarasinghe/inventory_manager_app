from tkinter import *
from window2 import logged_in_window
from PIL import Image, ImageTk
import mysql.connector
from tkinter import messagebox

try:
    dbcon = mysql.connector.connect(
        host="localhost",
        user="root",
        password="root",
        database="inventory_manager_db"
    )

except mysql.connector.Error as err:
    messagebox.showerror("Database Error", str(err))
    exit()

window = Tk()
window.geometry("1920x1080")
window.title("Desktop Inventory Management System")
img = Image.open("C:\\Pythonprogrammes\\Inventory_management_app\\New folder\\screenshot3.png")
icon = ImageTk.PhotoImage(img)
window.iconphoto(True, icon)
window.config(bg="#1E1E1E")

login_frame = Frame(window, bg="#252526", bd=5, relief="flat")
login_frame.place(x=715, y=150, width=500, height=510)

photo = PhotoImage(file="C:\\Pythonprogrammes\\Inventory_management_app\\New folder\\screenshot3.png")
log_label = Label(window, text="DIM System", fg="#FFFFFF", bg="#252526", font=("Georgia", 50, "bold"),
                  image=photo, compound="top")
log_label.image = photo
log_label.place(x=750, y=200)

username_label = Label(window, text="Username :", fg="#CCCCCC", bg="#252526", font=("Georgia", 18))
username_label.place(x=760, y=420)
password_label = Label(window, text="Password  :", fg="#CCCCCC", bg="#252526", font=("Georgia", 18))
password_label.place(x=760, y=470)

user_entry = Entry(window, font=("Arial", 10, "bold"), width=35, fg="White", bg="#2D2D30")
user_entry.place(x=915, y=429)
password_entry = Entry(window, font=("Arial", 10, "bold"), width=35, fg="White", bg="#2D2D30", show="*")
password_entry.place(x=915, y=479)

def login():
    username = user_entry.get().strip()
    password = password_entry.get().strip()

    if not username or not password:
        messagebox.showwarning("No Input", "Please don't leave any spaces behind.", parent=window)
        return

    cursor = dbcon.cursor()
    cursor.execute("SELECT user_name, password FROM users WHERE user_name=%s AND password=%s", (username, password))
    result = cursor.fetchone()
    cursor.close()

    if result:
        messagebox.showinfo("Success", "Access granted!", parent=window)
        window.withdraw()
        logged_in_window()
    else:
        messagebox.showerror("Failed", "Access denied", parent=window)

def clear_fields():
    user_entry.delete(0, END)
    password_entry.delete(0, END)

login_but = Button(window, command=login, text="Login", font=("Georgia", 10, "bold"),
                   fg="White", bg="#3A3D41", relief="flat", width=15, height=2,
                   activebackground="#2D2D30", activeforeground="White")
login_but.place(x=770, y=550)

clear_but = Button(window, command=clear_fields, text="Clear", font=("Georgia", 10, "bold"),
                   fg="White", bg="#3A3D41", relief="flat", width=15, height=2,
                   activebackground="#2D2D30", activeforeground="White")
clear_but.place(x=1009, y=550)

window.protocol("WM_DELETE_WINDOW", lambda: (dbcon.close(), window.destroy()))

window.mainloop()

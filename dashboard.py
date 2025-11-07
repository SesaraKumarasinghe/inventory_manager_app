from tkinter import *
from tkinter import ttk
import mysql.connector
from tkinter import messagebox

class Dashboard:
            def __init__(self, root):
                self.dbcon = mysql.connector.connect(
                    host="localhost",
                    user="root",
                    password="root",
                    database="Inventory_manager_db"
                )

                self.root = root
                self.main_window()

            def main_window(self):
                dashboard_window = Toplevel()
                dashboard_window.title("Desktop Inventory Management System")
                dashboard_window.geometry("1920x1080")
                dashboard_window.config(bg="#1E1E1E")

                heading = Label(dashboard_window, text="Dashboard", bg="#1E1E1E", fg="White", font=("Georgia", 50, "bold"))
                heading.place(x=750, y=10)

                main_frame = Frame(dashboard_window, bg="#E0E0E0")
                main_frame.place(x=50, y=100, width=1800, height=900)

                sub_heading = Label(main_frame, text="Welcome, Admin!", bg="#E0E0E0", fg="Black", font=("Arial", 30, "bold"))
                sub_heading.place(x=20, y=10)

                underline = Frame(main_frame, bg="#1E1E1E", height=4, width=1800)
                underline.place(x=0, y=70)

                content_frame = Frame(main_frame, bg="White")
                content_frame.place(x=20, y=100,width=1750, height=780)



from tkinter import *
from tkinter import ttk
from tkinter import  messagebox
from tkinter.ttk import Combobox
import mysql.connector

class ReportsManager:
    def __init__(self,root):
        self.dbcon = mysql.connector.connect(
            host="localhost",
            user="root",
            password="root",
            database="Inventory_manager_db"
        )

        self.root = root
        self.main_window()
        self.treeview()

    def main_window(self):
        self.reports_win = Toplevel(self.root)
        self.reports_win.title("Desktop Inventory Management System")
        self.reports_win.geometry("1300x800")
        self.reports_win.config(bg="#1E1E1E")

        heading = Label(self.reports_win, text="Reports",
                        bg="#1E1E1E", fg="White",
                        font=("Georgia", 42, "bold"))
        heading.place(x=500, y=10)

        self.content_frame = Frame(self.reports_win, bg="#F1F0F0")
        self.content_frame.place(x=30, y=80, width=1240, height=670)

        sub_heading = Label(self.content_frame, text="Welcome, Admin!",
                            bg="#F1F0F0", fg="#1E1E1E",
                            font=("TkDefaultFont", 24, "bold"))
        sub_heading.place(x=20, y=10)

        underline = Frame(self.content_frame, bg="#1E1E1E", height=3, width=1240)
        underline.place(x=0, y=55)

        s_repo = Button(self.content_frame, text="Sales Report",
                         relief="flat",
                         bg="#3962A3", fg="White",
                         activebackground="#3962A3",
                         activeforeground="White",
                         font=("Arial", 9))
        s_repo.place(x=30, y=80)

        p_repo = Button(self.content_frame, text="Purchase Report",
                         relief="flat",
                         bg="#3962A3", fg="White",
                         activebackground="#3962A3",
                         activeforeground="White",
                         font=("Arial", 9))
        p_repo.place(x=130, y=80)

        u_actvty = Button(self.content_frame, text="User Activity",
                         relief="flat",
                         bg="#3962A3", fg="White",
                         activebackground="#3962A3",
                         activeforeground="White",
                         font=("Arial", 9))
        u_actvty.place(x=250, y=80)

        exp_csv = Button(self.content_frame, text="Print Report",
                         relief="flat",
                         bg="#3962A3", fg="White",
                         activebackground="#3962A3",
                         activeforeground="White",
                         font=("Arial", 9))
        exp_csv.place(x=1130, y=80)

        exp_pdf = Button(self.content_frame, text="Export CSV",
                         relief="flat",
                         bg="#3962A3", fg="White",
                         activebackground="#3962A3",
                         activeforeground="White",
                         font=("Arial", 9))
        exp_pdf.place(x=1035, y=80)

        exp_pdf = Button(self.content_frame, text="Export PDF",
                         relief="flat",
                         bg="#3962A3", fg="White",
                         activebackground="#3962A3",
                         activeforeground="White",
                         font=("Arial", 9))
        exp_pdf.place(x=940, y=80)

        fltr_lbl = Label(self.content_frame, text="Filter By :",
                           bg="#F1F0F0", fg="#1E1E1E",
                           font=("Arial", 11, "bold"))
        fltr_lbl.place(x=30, y=120)

        style = ttk.Style()
        style.theme_use("clam")
        style.configure("TCombobox",
                        fieldbackground="white",
                        background="white",
                        foreground="grey")

        def add_combobox_placeholder(combo,placeholder_txt):
            combo.set(placeholder_txt)
            combo.configure()

            def clear_placeholder(event):
                if combo.get() == placeholder_txt:
                    combo.set("")
                    combo.configure(foreground="Black")

            def restore_placeholder(event):
                if combo.get() == "":
                    combo.set(placeholder_txt)
                    combo.configure(foreground="Grey")

            combo.bind("<FocusIn>",clear_placeholder)
            combo.bind("<FocusOut>",restore_placeholder)

        combo_type = ttk.Combobox(self.content_frame, values=["Sale", "Purchase"], state="readonly", font=("Arial", 11))
        combo_type.place(x=110,y=120)

        combo_user = ttk.Combobox(self.content_frame, values=["Admin", "Staff"], state="readonly", font=("Arial", 11))
        combo_user.place(x=310,y=120)

        combo_date = ttk.Combobox(self.content_frame, values=["Today", "This week", "This month"], state="readonly", font=("Arial", 11))
        combo_date.place(x=510,y=120)

        add_combobox_placeholder(combo_type,"Select type...")
        add_combobox_placeholder(combo_user,"Select user...")
        add_combobox_placeholder(combo_date,"Select date...")

        filter_btn = Button(self.content_frame, text="Filter",
                relief="flat",
                bg="#3962A3", fg="White",
                activebackground="#3962A3",
                activeforeground="White",
                font=("Arial", 9),width=15)
        filter_btn.place(x=740, y=119)

    def treeview(self):
        style = ttk.Style()
        style.theme_use("default")
        style.configure("Treeview",
                        background="White",
                        foreground="Black",
                        fieldbackground="White",
                        rowheight=28)

        style.configure("Treeview.Heading",
                        background="#548DCF",
                        foreground="White",
                        font=("Arial", 11, "bold"))

        self.table = ttk.Treeview(self.content_frame,
                                  columns=("date","user","type","products_id","quantity","total_amount"),
                                  show="headings")

        self.table.heading("date",text="Date")
        self.table.column("date",width=120,anchor="center")

        self.table.heading("user",text="User")
        self.table.column("user",width=80,anchor="center")

        self.table.heading("type",text="Type")
        self.table.column("type",width=80,anchor="center")

        self.table.heading("products_id",text="Product")
        self.table.column("products_id",width=120,anchor="center")

        self.table.heading("quantity",text="Quantity")
        self.table.column("quantity",width=80,anchor="center")

        self.table.heading("total_amount",text="Total")
        self.table.column("total_amount",width=120,anchor="center")

        self.table.place(x=30,y=170, width=1180, height=280)


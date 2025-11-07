from tkinter import *
from tkinter import ttk
import mysql.connector
from tkinter import messagebox

# class Dashboard:
#             def __init__(self, root):
#                 self.dbcon = mysql.connector.connect(
#                     host="localhost",
#                     user="root",
#                     password="root",
#                     database="Inventory_manager_db"
#                 )
#
#                 self.root = root
#                 self.main_window()
#
#             def main_window(self):
#                 dashboard_window = Toplevel()
#                 dashboard_window.title("Desktop Inventory Management System")
#                 dashboard_window.geometry("1920x1080")
#                 dashboard_window.config(bg="#1E1E1E")
#
#                 heading = Label(dashboard_window, text="Dashboard", bg="#1E1E1E", fg="White", font=("Georgia", 50, "bold"))
#                 heading.place(x=750, y=10)
#
#                 main_frame = Frame(dashboard_window, bg="#252526")
#                 main_frame.place(x=50, y=100, width=1800, height=900)
#
#                 sub_heading = Label(main_frame, text="Welcome, Admin!", bg="#252526", fg="White", font=("Arial", 30, "bold"))
#                 sub_heading.place(x=20, y=10)
#
#                 underline = Frame(main_frame, bg="#1E1E1E", height=4, width=1800)
#                 underline.place(x=0, y=70)
#
#                 self.content_frame = Frame(main_frame, bg="White")
#                 self.content_frame.place(x=20, y=100,width=1750, height=780)
#
#                 add_prdct = Button(self.content_frame, text="Add Product", relief="flat",
#                                    bg="#3962A3", fg="White", activebackground="#3962A3", activeforeground="White",
#                                    font=("Arial", 10))
#                 add_prdct.place(x=30, y=30)
#
#                 add_tran = Button(self.content_frame, text="Add Transaction", relief="flat",
#                                   bg="#359E0B", fg="White",
#                                   activebackground="#359E0B", activeforeground="White", font=("Arial", 10))
#                 add_tran.place(x=140, y=30)
#
#                 view_rprts = Button(self.content_frame, text="View Reports",relief="flat",bg="#DBA919", fg="White",
#                                     activebackground="#DBA919",activeforeground="White",font=("Arial",10))
#                 view_rprts.place(x=270,y=30)
#
#                 users = Button(self.content_frame, text="Users",relief="flat",bg="#C07783", fg="White",
#                                     activebackground="#C07783",activeforeground="White",font=("Arial",10))
#                 users.place(x=386,y=30,width=70)
#
#                 search_lbl = Label(self.content_frame, text="Search", bg="white", fg="Black",
#                                    font=("Arial", 13, "bold"))
#                 search_lbl.place(x=500, y=32)
#
#                 self.entry = Entry(self.content_frame, width=25, font=("Arial", 13), bg="#FBF7EA",fg="Black")
#                 self.entry.place(x=580, y=33)
#
#                 refresh_btn = Button(self.content_frame, text="⟳ Refresh", bg="#2ECC71",
#                                      fg="white", relief="flat", activebackground="#48C9B0", font=("Arial", 10))
#                 refresh_btn.place(x=850, y=30)
#
#             def stats(self):
#                 frame = Frame(self.content_frame,bg="#E8E8E8")
#                 frame.place(x=30, y=100, height=490, width=440)
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
        self.stats()

    def main_window(self):
        dashboard_window = Toplevel()
        dashboard_window.title("Desktop Inventory Management System")
        dashboard_window.geometry("1200x700")
        dashboard_window.config(bg="#1E1E1E")

        heading = Label(
            dashboard_window,
            text="Dashboard",
            bg="#1E1E1E",
            fg="White",
            font=("Georgia", 40, "bold")
        )
        heading.place(x=450, y=10)

        main_frame = Frame(dashboard_window, bg="#252526")
        main_frame.place(x=30, y=100, width=1140, height=560)

        sub_heading = Label(
            main_frame,
            text="Welcome, Admin!",
            bg="#252526",
            fg="White",
            font=("Arial", 26, "bold")
        )
        sub_heading.place(x=20, y=10)

        underline = Frame(main_frame, bg="#1E1E1E", height=3, width=1140)
        underline.place(x=0, y=60)

        self.content_frame = Frame(main_frame, bg="White")
        self.content_frame.place(x=0, y=80, width=1200, height=500)

        add_prdct = Button(
            self.content_frame, text="Add Product", relief="flat",
            bg="#3962A3", fg="White",
            activebackground="#3962A3", activeforeground="White",
            font=("Arial", 10)
        )
        add_prdct.place(x=30, y=30, width=120, height=35)

        add_tran = Button(
            self.content_frame, text="Add Transaction", relief="flat",
            bg="#359E0B", fg="White",
            activebackground="#359E0B", activeforeground="White",
            font=("Arial", 10)
        )
        add_tran.place(x=170, y=30, width=150, height=35)

        view_rprts = Button(
            self.content_frame, text="View Reports", relief="flat",
            bg="#DBA919", fg="White",
            activebackground="#DBA919", activeforeground="White",
            font=("Arial", 10)
        )
        view_rprts.place(x=340, y=30, width=140, height=35)

        users = Button(
            self.content_frame, text="Users", relief="flat",
            bg="#C07783", fg="White",
            activebackground="#C07783", activeforeground="White",
            font=("Arial", 10)
        )
        users.place(x=500, y=30, width=100, height=35)

        search_lbl = Label(
            self.content_frame, text="Search",
            bg="white", fg="Black",
            font=("Arial", 13, "bold")
        )
        search_lbl.place(x=630, y=35)

        self.entry = Entry(
            self.content_frame,
            width=25,
            font=("Arial", 13),
            bg="#FBF7EA",
            fg="Black"
        )
        self.entry.place(x=700, y=35, width=220, height=28)

        refresh_btn = Button(
            self.content_frame,
            text="⟳ Refresh",
            bg="#2ECC71",
            fg="white",
            relief="flat",
            activebackground="#48C9B0",
            font=("Arial", 10)
        )
        refresh_btn.place(x=940, y=32, width=100, height=32)

    def stats(self):
        frame = Frame(self.content_frame, bg="#E8E8E8")
        frame.place(x=30, y=100, height=320, width=350)

        try:
            cursor = self.dbcon.cursor()
            cursor.execute("select count(*) from products")
            prdct_num = cursor.fetchone()[0]
            prdct_str = str(prdct_num)

            total_prdcts = Label(frame,text="Total Products :",bg="#E8E8E8",fg="Black",font=("Arial", 13, "bold"))
            total_prdcts.place(x=20,y=20)

            if prdct_str == "0":
                p_ttl = Label(frame,text="No products",bg="#E8E8E8",fg="#8D6F64",font=("Arial", 13, "bold"))
                p_ttl.place(x=160,y=21)

            else:
                ttl = Label(frame, text=prdct_str, bg="#E8E8E8", fg="#8D6F64", font=("Arial", 13, "bold"))
                ttl.place(x=160, y=21)

            cursor.execute("select count(*) from users")
            user_num = cursor.fetchone()[0]
            u_str = str(user_num)

            ttl_users = Label(frame,text="Total Users :",bg="#E8E8E8",fg="Black",font=("Arial", 13, "bold"))
            ttl_users.place(x=20,y=60)

            if u_str == "0":
                u_ttl = Label(frame,text="No users",bg="#E8E8E8",fg="#8D6F64",font=("Arial", 13, "bold"))
                u_ttl.place(x=130,y=61)

            else:
                u_ttl = Label(frame,text=u_str,bg="#E8E8E8",fg="#8D6F64",font=("Arial", 13, "bold"))
                u_ttl.place(x=130,y=61)

            cursor.execute("select count(*) from transactions")
            tran_num = cursor.fetchone()[0]
            t_str = str(tran_num)

            ttl_tran = Label(frame,text="Total Transactions :",bg="#E8E8E8",fg="Black",font=("Arial", 13, "bold"))
            ttl_tran.place(x=20,y=100)

            if t_str == "0":
                t_ttl = Label(frame,text="No Transactions",bg="#E8E8E8",fg="#8D6F64",font=("Arial", 13, "bold"))
                t_ttl.place(x=180,y=101)

            else:
                t_ttl = Label(frame,text=t_str,bg="#E8E8E8",fg="#8D6F64",font=("Arial", 13, "bold"))
                t_ttl.place(x=150,y=101)

            cursor.execute("select coalesce(sum(total_amount),0) from transactions where type = 'Purchase'")
            ttl_rev = cursor.fetchone()[0]
            rev = str(ttl_rev)

            total_revenue = Label(frame,text="Total Revenue :",bg="#E8E8E8",fg="Black",font=("Arial", 13, "bold"))
            total_revenue.place(x=20,y=140)

            t_ttl = Label(frame, text=f"${rev}", bg="#E8E8E8", fg="#8D6F64", font=("Arial", 13, "bold"))
            t_ttl.place(x=150, y=141)

        finally:
            cursor.close()











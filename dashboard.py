from tkinter import *
from tkinter import ttk
import mysql.connector

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
        self.treeview()
        self.stats()
        self.load_latest_trans()

    def main_window(self):
        dashboard_window = Toplevel()
        dashboard_window.title("Desktop Inventory Management System")
        dashboard_window.geometry("1200x700")
        dashboard_window.config(bg="#111828")

        heading = Label(
            dashboard_window,
            text="Dashboard",
            bg="#111828",
            fg="#F3F4F6",
            font=("Segoe UI", 40, "bold")
        )
        heading.place(x=450, y=10)

        main_frame = Frame(dashboard_window, bg="#0B1220")
        main_frame.place(x=30, y=100, width=1140, height=560)

        sub_heading = Label(
            main_frame,
            text="Welcome, Admin!",
            bg="#0B1220",
            fg="#8A95B8",
            font=("Segoe UI", 26, "bold")
        )
        sub_heading.place(x=20, y=10)

        underline = Frame(main_frame, bg="#2ED3B7", height=3, width=1140)
        underline.place(x=0, y=60)

        self.content_frame = Frame(main_frame, bg="#151F32")
        self.content_frame.place(x=0, y=80, width=1140, height=500)

        add_prdct = Button(
            self.content_frame, text="Add Product", relief="flat",
            bg="#2ED3B7", fg="#0B1220",
            activebackground="#31E3BF", activeforeground="#0B1220",
            font=("Segoe UI", 11, "bold")
        )
        add_prdct.place(x=30, y=30, width=120, height=35)

        add_tran = Button(
            self.content_frame, text="Add Transaction", relief="flat",
            bg="#1C2A43", fg="#F3F4F6",
            activebackground="#223555", activeforeground="#2ED3B7",
            font=("Segoe UI", 11, "bold")
        )
        add_tran.place(x=170, y=30, width=150, height=35)

        view_rprts = Button(
            self.content_frame, text="View Reports", relief="flat",
            bg="#151F32", fg="#2ED3B7",
            activebackground="#1C2A43", activeforeground="#31E3BF",
            font=("Segoe UI", 11, "bold")
        )
        view_rprts.place(x=340, y=30, width=140, height=35)

        users = Button(
            self.content_frame, text="Users", relief="flat",
            bg="#F472B6", fg="#0B1220",
            activebackground="#F688C5", activeforeground="#0B1220",
            font=("Segoe UI", 11, "bold")
        )
        users.place(x=500, y=30, width=100, height=35)

        search_lbl = Label(
            self.content_frame, text="Search",
            bg="#151F32", fg="#F3F4F6",
            font=("Segoe UI", 13, "bold")
        )
        search_lbl.place(x=630, y=35)

        self.entry = Entry(
            self.content_frame,
            width=25,
            font=("Segoe UI", 13),
            bg="#0B1220",
            fg="#F3F4F6",
            insertbackground="#2ED3B7",
            highlightbackground="#2ED3B7",
            highlightcolor="#2ED3B7",
            relief="flat"
        )
        self.entry.place(x=700, y=35, width=220, height=28)

        refresh_btn = Button(
            self.content_frame,
            text="⟳ Refresh",
            bg="#151F32",
            fg="#2ED3B7",
            relief="flat",
            activebackground="#1C2A43",
            activeforeground="#31E3BF",
            font=("Segoe UI", 11, "bold")
        )
        refresh_btn.place(x=940, y=32, width=100, height=32)

        stats_lbl = Label(
            self.content_frame,
            text="Stats",
            bg="#151F32",
            fg="#F3F4F6",
            font=("Segoe UI", 24, "bold")
        )
        stats_lbl.place(x=30, y=85)

        latest_lbl = Label(
            self.content_frame,
            text="Latest transactions",
            bg="#151F32",
            fg="#F3F4F6",
            font=("Segoe UI", 24, "bold")
        )
        latest_lbl.place(x=400, y=85)

    def treeview(self):
        style = ttk.Style()
        style.theme_use("default")

        style.configure("Treeview",
                        background="#151F32",
                        foreground="#F3F4F6",
                        fieldbackground="#151F32",
                        rowheight=30,
                        bordercolor="#0B1220",
                        relief="flat")

        style.configure("Treeview.Heading",
                        background="#2ED3B7",
                        foreground="#0B1220",
                        font=("Segoe UI", 12, "bold"),
                        height=10)
        style.map("Treeview",
                  background=[("selected", "#2ED3B7")],
                  foreground=[("selected", "#0B1220")])

        self.table = ttk.Treeview(
        self.content_frame,
        columns=("transaction_id", "products_id", "type", "quantity", "total_amount", "date"),
            show="headings"
            )

        self.table.heading("transaction_id", text="ID")
        self.table.column("transaction_id", width=80, anchor="center")

        self.table.heading("products_id", text="Product")
        self.table.column("products_id", width=120, anchor="center")

        self.table.heading("type", text="Type")
        self.table.column("type", width=100, anchor="center")

        self.table.heading("quantity", text="Quantity")
        self.table.column("quantity", width=80, anchor="center")

        self.table.heading("total_amount", text="Total")
        self.table.column("total_amount", width=100, anchor="center")

        self.table.heading("date", text="Date")
        self.table.column("date", width=120, anchor="center")

        self.table.place(x=400, y=150, width=710, height=270)

    def load_latest_trans(self):
        cursor = self.dbcon.cursor()
        cursor.execute(
            "SELECT transaction_id, products_id, type, quantity, total_amount, `date` FROM transactions ORDER BY transaction_id DESC LIMIT 3")
        rows = cursor.fetchall()
        cursor.close()

        for item in self.table.get_children():
            self.table.delete(item)

        if not rows:
            self.table.insert("", "end", values=("No transactions", "", "", "", "", ""))

        for row in rows:
            self.table.insert("","end",values=row)

    def stats(self):
        frame = Frame(self.content_frame, bg="#0B1220")
        frame.place(x=30, y=150, height=270, width=350)

        try:
            cursor = self.dbcon.cursor()
            cursor.execute("select count(*) from products")
            prdct_num = cursor.fetchone()[0]
            prdct_str = str(prdct_num)

            total_prdcts = Label(frame,text="Total Products :",bg="#0B1220",fg="#F3F4F6",font=("Segoe UI", 13, "bold"))
            total_prdcts.place(x=20,y=20)

            if prdct_str == "0":
                p_ttl = Label(frame,text="No products",bg="#0B1220",fg="#2ED3B7",font=("Segoe UI", 13, "bold"))
                p_ttl.place(x=160,y=21)

            else:
                ttl = Label(frame, text=prdct_str, bg="#0B1220", fg="#2ED3B7", font=("Segoe UI", 13, "bold"))
                ttl.place(x=160, y=21)

            cursor.execute("select count(*) from users")
            user_num = cursor.fetchone()[0]
            u_str = str(user_num)

            ttl_users = Label(frame,text="Total Users :",bg="#0B1220",fg="#F3F4F6",font=("Segoe UI", 13, "bold"))
            ttl_users.place(x=20,y=60)

            if u_str == "0":
                u_ttl = Label(frame,text="No users",bg="#0B1220",fg="#2ED3B7",font=("Segoe UI", 13, "bold"))
                u_ttl.place(x=130,y=61)

            else:
                u_ttl = Label(frame,text=u_str,bg="#0B1220",fg="#2ED3B7",font=("Segoe UI", 13, "bold"))
                u_ttl.place(x=130,y=61)

            cursor.execute("select count(*) from transactions")
            tran_num = cursor.fetchone()[0]
            t_str = str(tran_num)

            ttl_tran = Label(frame,text="Total Transactions :",bg="#0B1220",fg="#F3F4F6",font=("Segoe UI", 13, "bold"))
            ttl_tran.place(x=20,y=100)

            if t_str == "0":
                t_ttl = Label(frame,text="No Transactions",bg="#0B1220",fg="#2ED3B7",font=("Segoe UI", 13, "bold"))
                t_ttl.place(x=180,y=101)

            else:
                t_ttl = Label(frame,text=t_str,bg="#0B1220",fg="#2ED3B7",font=("Segoe UI", 13, "bold"))
                t_ttl.place(x=150,y=101)

            cursor.execute("select coalesce(sum(total_amount),0) from transactions where type = 'Purchase'")
            ttl_rev = cursor.fetchone()[0]
            rev = str(ttl_rev)

            total_revenue = Label(frame,text="Total Revenue :",bg="#0B1220",fg="#F3F4F6",font=("Segoe UI", 13, "bold"))
            total_revenue.place(x=20,y=140)

            rev_lbl = Label(frame, text=f"${rev}", bg="#0B1220", fg="#2ED3B7", font=("Segoe UI", 13, "bold"))
            rev_lbl.place(x=150, y=141)

        finally:
            cursor.close()











from tkinter import *
from tkinter import ttk
from tkinter import  messagebox
import mysql.connector
from tkcalendar import dateentry

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
        self.load_data()

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
                         command=self.user_activity,
                         relief="flat",
                         bg="#3962A3", fg="White",
                         activebackground="#3962A3",
                         activeforeground="White",
                         font=("Arial", 9))
        u_actvty.place(x=270, y=80)

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
                    combo.configure(foreground="Grey")

            def restore_placeholder(event):
                if combo.get() == "":
                    combo.set(placeholder_txt)
                    combo.configure(foreground="Black")

            combo.bind("<FocusIn>",clear_placeholder)
            combo.bind("<FocusOut>",restore_placeholder)

        self.combo_type = ttk.Combobox(self.content_frame, values=["Sale", "Purchase"], state="readonly", font=("Arial", 11))
        self.combo_type.place(x=110,y=120)

        self.combo_user = ttk.Combobox(self.content_frame, values=["Admin", "Staff"], state="readonly", font=("Arial", 11))
        self.combo_user.place(x=310,y=120)

        self.combo_date = ttk.Combobox(self.content_frame, values=["Today", "This week", "This month"], state="readonly", font=("Arial", 11))
        self.combo_date.place(x=510,y=120)

        add_combobox_placeholder(self.combo_type,"Select type...")
        add_combobox_placeholder(self.combo_user,"Select user...")
        add_combobox_placeholder(self.combo_date,"Select date...")

        filter_btn = Button(self.content_frame, text="Filter",
                relief="flat",
                bg="#3962A3", fg="White",
                activebackground="#3962A3",
                activeforeground="White",
                font=("Arial", 9),width=15)
        filter_btn.place(x=740, y=119)

        rev_lbl = Label(self.content_frame,text="Total Revenue :",bg="#F1F0F0", fg="Black", font=("Arial", 13, "bold"))
        rev_lbl.place(x=350, y=500)
        revenue = Label(self.content_frame,text=str(self.calculate_total_rev()),bg="#F1F0F0", fg="Black", font=("Arial", 13, "bold"))
        revenue.place(x=500, y=500)

        ttl_tran = Label(self.content_frame, text="Total Transactions :", bg="#F1F0F0", fg="Black", font=("Arial", 13, "bold"))
        ttl_tran.place(x=710, y=500)
        tot_transactions = Label(self.content_frame, text=str(self.calculate_total_trans()), bg="#F1F0F0", fg="Black", font=("Arial", 13, "bold"))
        tot_transactions.place(x=900, y=500)

        last_updted = Label(self.content_frame, text="Last Updated :", bg="#F1F0F0", fg="Black", font=("Arial", 13, "bold"))
        last_updted.place(x=710, y=600)
        last_updated = Label(self.content_frame, text=str(self.last_updated()), bg="#F1F0F0", fg="Black", font=("Arial", 13, "bold"))
        last_updated.place(x=900, y=600)

        ttl_prof = Label(self.content_frame, text="Total Profit :", bg="#F1F0F0", fg="Black", font=("Arial", 13, "bold"))
        ttl_prof.place(x=350, y=600)
        total_profit = Label(self.content_frame, text=str(self.total_profit_made()), bg="#F1F0F0", fg="Black", font=("Arial", 13, "bold"))
        total_profit.place(x=500, y=600)

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

    def load_data(self):
        try:
            cursor = self.dbcon.cursor()
            cursor.execute("select user_id,role from users")
            results = cursor.fetchall()

            self.user_map = {name:uid for uid,name in results}

            cursor.execute("select products_id, name from products")
            results1 = cursor.fetchall()

            self.prdct_map = {name:pid for pid,name in results1}

            cursor.execute("select `date`,user_id,type,products_id,quantity,total_amount from transactions")
            rows = cursor.fetchall()

            for item in self.table.get_children():
                self.table.delete(item)

            for row in rows:
                t_date,user_id,t_type,prd_id,qtty,total = row
                user_name = next((k for k, v in self.user_map.items() if v == user_id), user_id)
                prd_name = next((k for k, v in self.prdct_map.items() if v == prd_id), prd_id)
                self.table.insert("", "end", values=(t_date, user_name, t_type, prd_name, qtty, total))

        except mysql.connector.Error as err:
            messagebox.showerror("Database Error",str(err),parent=self.reports_win)
            return

        finally:
            cursor.close()

    def sales_report(self):
        cursor = self.dbcon.cursor()

        try:
            cursor.execute("select `date`,user_id,type,products_id,quantity,total_amount from transactions where type = 'Sale'")
            rows = cursor.fetchall()
            cursor.close()

            for item in self.table.get_children():
                self.table.delete(item)

            for row in rows:
                t_date,user_id,t_type,prd_id,qtty,total = row
                user_name = next((k for k, v in self.user_map.items() if v == user_id), user_id)
                prd_name = next((k for k, v in self.prdct_map.items() if v == prd_id), prd_id)
                self.table.insert("", "end", values=(t_date, user_name, t_type, prd_name, qtty, total))

        except:
            messagebox.showerror("Error","No transactions made under category 'Sale'",parent=self.reports_win)
            return

    def purchase_report(self):
        cursor = self.dbcon.cursor()

        try:
            cursor.execute("select `date`,user_id,type,products_id,quantity,total_amount from transactions where type = 'Purchase'")
            rows = cursor.fetchall()
            cursor.close()

            for item in self.table.get_children():
                self.table.delete(item)

            for row in rows:
                t_date,user_id,t_type,prd_id,qtty,total = row
                user_name = next((k for k, v in self.user_map.items() if v == user_id), user_id)
                prd_name = next((k for k, v in self.prdct_map.items() if v == prd_id), prd_id)
                self.table.insert("", "end", values=(t_date, user_name, t_type, prd_name, qtty, total))

        except:
            messagebox.showerror("Error","No transactions made under category 'Purchase'",parent=self.reports_win)
            return

    def user_activity(self):
        from datetime import datetime, date, timedelta

        popup = Toplevel(self.reports_win)
        popup.geometry("400x400")
        popup.title("User Activity")
        popup.config(bg="#1E1E1E")

        # ---------- Content Frame ----------
        content_frame = Frame(popup, bg="White")
        content_frame.place(x=20, y=50, width=360, height=300)

        # Heading
        heading = Label(popup, text="User Activity", bg="#1E1E1E", fg="White", font=("Georgia", 20, "bold"))
        heading.place(x=100, y=10)

        # ---------- User selection ----------
        Label(content_frame, text="Select User:", bg="White", fg="Black", font=("Arial", 12, "bold")).place(x=20, y=20)
        Label(content_frame, text="Filter By Date:", bg="White", fg="Black", font=("Arial", 12, "bold")).place(x=200,
                                                                                                               y=20)

        # User combobox
        user_list = list(self.user_map.keys())
        usr_combo = ttk.Combobox(content_frame, values=user_list, state="readonly", font=("Arial", 11))
        usr_combo.place(x=20, y=50, width=140)
        usr_combo.set("Select user...")

        # Date filter combobox
        date_combo = ttk.Combobox(content_frame, values=["Today", "This week", "This month"], state="readonly",
                                  font=("Arial", 11))
        date_combo.place(x=200, y=50, width=140)
        date_combo.set("Select filter...")

        # ---------- Summary Labels ----------
        total_trans_lbl = Label(content_frame, text="Total Transactions: 0", bg="White", fg="Black",
                                font=("Arial", 12, "bold"))
        total_trans_lbl.place(x=20, y=130)
        total_revenue_lbl = Label(content_frame, text="Total Revenue: 0", bg="White", fg="Black",
                                  font=("Arial", 12, "bold"))
        total_revenue_lbl.place(x=20, y=160)
        total_spent_lbl = Label(content_frame, text="Total Spent: 0", bg="White", fg="Black",
                                font=("Arial", 12, "bold"))
        total_spent_lbl.place(x=20, y=190)

        # ---------- Apply Filter ----------
        def apply_filter():
            selected_user = usr_combo.get()
            selected_date = date_combo.get()

            if selected_user in ["", "Select user..."]:
                messagebox.showwarning("Warning", "Please select a user.", parent=popup)
                return
            if selected_date in ["", "Select filter..."]:
                messagebox.showwarning("Warning", "Please select a date filter.", parent=popup)
                return

            cursor = self.dbcon.cursor()
            cursor.execute("select from ")

            # Filter data from main table
            # filtered_rows = []
            # for row_id in self.table.get_children():
            #     row = self.table.item(row_id, "values")
            #     row_user = row[1]  # column 1 = user
            #     row_date = datetime.strptime(row[0], "%Y-%m-%d").date()  # column 0 = date
            #
            #     if row_user != selected_user:
            #         continue
            #
            #     today_dt = date.today()
            #     if selected_date == "Today" and row_date != today_dt:
            #         continue
            #     elif selected_date == "This week":
            #         start_week = today_dt - timedelta(days=today_dt.weekday())
            #         end_week = start_week + timedelta(days=6)
            #         if not (start_week <= row_date <= end_week):
            #             continue
            #     elif selected_date == "This month" and row_date.month != today_dt.month:
            #         continue
            #
            #     filtered_rows.append(row)
            #
            # # Compute summaries
            # total_trans = len(filtered_rows)
            # total_amount = sum(float(row[5]) for row in filtered_rows if row[5])
            # total_spent = sum(float(row[5]) for row in filtered_rows if row[2] == "Purchase")
            # total_revenue = total_amount - total_spent
            #
            # total_trans_lbl.config(text=f"Total Transactions: {total_trans}")
            # total_revenue_lbl.config(text=f"Total Revenue: {total_revenue}")
            # total_spent_lbl.config(text=f"Total Spent: {total_spent}")

        Button(content_frame, text="Apply Filter", bg="#3962A3", fg="White", font=("Arial", 11, "bold"),
               command=apply_filter,relief="flat").place(x=120, y=85, width=120, height=30)

    def calculate_total_rev(self):
        cursor = self.dbcon.cursor()
        cursor.execute("select sum(total_amount) from transactions where type = 'Sale'")
        rev_result = cursor.fetchone()[0]
        cursor.close()
        return rev_result

    def calculate_total_trans(self):
        cursor = self.dbcon.cursor()
        cursor.execute("select count(transaction_id) from transactions")
        tran_result = cursor.fetchone()[0]
        cursor.close()
        return tran_result

    def last_updated(self):
        cursor = self.dbcon.cursor()
        try:
            cursor.execute("select max(`date`) from transactions")
            date_result = cursor.fetchone()
            if date_result and date_result[0]:
                return date_result[0]
            return "N/A"

        finally:
            cursor.close()

    def total_profit_made(self):
        cursor = self.dbcon.cursor()

        try:
            cursor.execute("select sum(total_amount) from transactions where type = 'Purchase'")
            spent = cursor.fetchone()[0] or 0

            cursor.execute("select sum(total_amount) from transactions where type = 'Sale'")
            earned = cursor.fetchone()[0] or 0

            return earned - spent

        finally:
            cursor.close()



















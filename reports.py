from tkinter import *
from tkinter import ttk, messagebox, filedialog
from datetime import datetime, date, timedelta
import mysql.connector
import csv
import os
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas

class ReportsManager:
    def __init__(self, root):
        try:
            self.dbcon = mysql.connector.connect(
                host="localhost",
                user="root",
                password="root",
                database="Inventory_manager_db"
            )
        except mysql.connector.Error as err:
            messagebox.showerror("Database Error", f"Failed to connect to database:\n{err}")
            return

        self.root = root
        self.user_map = {}     # id -> username
        self.prdct_map = {}    # id -> product name
        self.main_window()
        self.create_table_container()
        self.load_data()

    # ------------------- MAIN WINDOW -------------------
    def main_window(self):
        self.reports_win = Toplevel(self.root)
        self.reports_win.title("Desktop Inventory Management System")
        self.reports_win.geometry("1300x800")
        self.reports_win.config(bg="#111828")

        heading = Label(self.reports_win, text="Reports", bg="#111828", fg="#F3F4F6",
                        font=("Segoe UI", 42, "bold"))
        heading.place(x=500, y=5)

        self.content_frame = Frame(self.reports_win, bg="#0B1220")
        self.content_frame.place(x=30, y=80, width=1240, height=670)

        sub_heading = Label(self.content_frame, text="Welcome, Admin!", bg="#0B1220", fg="#8A95B8",
                            font=("Segoe UI", 24, "bold"))
        sub_heading.place(x=20, y=7)

        underline = Frame(self.content_frame, bg="#2ED3B7", height=3, width=1240)
        underline.place(x=0, y=55)

        self.panel_frame = Frame(self.content_frame, bg="#151F32")
        self.panel_frame.place(x=0, y=80, width=1240, height=590)

        self.create_quick_actions()
        self.create_filters()
        self.create_stats_frame()

    # ------------------- QUICK ACTIONS -------------------
    def create_quick_actions(self):
        Label(self.panel_frame, text="Quick Actions", bg="#151F32", fg="#F3F4F6",
              font=("Segoe UI", 20, "bold")).place(x=20, y=0)

        frame = Frame(self.panel_frame, bg="#151F32")
        frame.place(x=20, y=40, width=1200, height=50)

        Button(frame, text="Sales Report", bg="#2ED3B7", fg="#0B1220", relief="flat",
               font=("Segoe UI", 10, "bold"), width=14,
               command=lambda: self.apply_filter(type_filter="Sale")).pack(side=LEFT, padx=5)

        Button(frame, text="Purchase Report", bg="#1C2A43", fg="#F3F4F6", relief="flat",
               font=("Segoe UI", 10, "bold"), width=14,
               command=lambda: self.apply_filter(type_filter="Purchase")).pack(side=LEFT, padx=5)

        Button(frame, text="User Activity", bg="#151F32", fg="#2ED3B7", relief="flat",
               font=("Segoe UI", 10, "bold"), width=14, command=self.user_activity).pack(side=LEFT, padx=5)

        Frame(frame, bg="#151F32").pack(side=LEFT, expand=True)

        Button(frame, text="Print Report", bg="#151F32", fg="#2ED3B7", relief="flat",
               font=("Segoe UI", 10, "bold"), width=12, command=self.print_table).pack(side=RIGHT, padx=5)
        Button(frame, text="Export CSV", bg="#151F32", fg="#2ED3B7", relief="flat",
               font=("Segoe UI", 10, "bold"), width=12, command=self.export_csv).pack(side=RIGHT, padx=5)
        Button(frame, text="Export PDF", bg="#151F32", fg="#2ED3B7", relief="flat",
               font=("Segoe UI", 10, "bold"), width=12, command=self.export_pdf).pack(side=RIGHT, padx=5)

    # ------------------- FILTERS -------------------
    def create_filters(self):
        filter_section = Frame(self.panel_frame, bg="#151F32")
        filter_section.place(x=20, y=100, width=1200, height=80)

        Label(filter_section, text="Filter By :", bg="#151F32", fg="#F3F4F6",
              font=("Segoe UI", 12, "bold")).pack(side=LEFT, padx=(0, 12))

        style = ttk.Style()
        style.theme_use("clam")
        style.configure("TCombobox",
                        fieldbackground="#151F32",
                        background="#0B1220",
                        foreground="#F3F4F6",
                        bordercolor="#0B1220")

        self.combo_type = ttk.Combobox(filter_section, values=["Sale", "Purchase"], state="readonly",
                                       font=("Segoe UI", 11), width=17)
        self.combo_type.pack(side=LEFT, padx=5)
        self.combo_type.set("Select type...")

        # User combo
        self.combo_user = ttk.Combobox(filter_section, state="readonly",
                                       font=("Segoe UI", 11), width=17)
        self.combo_user.pack(side=LEFT, padx=5)
        self.combo_user.set("All users")  # Will be updated in load_data()

        self.combo_date = ttk.Combobox(filter_section, values=["Today", "This week", "This month"],
                                       state="readonly", font=("Segoe UI", 11), width=20)
        self.combo_date.pack(side=LEFT, padx=5)
        self.combo_date.set("Select date...")

        Button(filter_section, text="Filter", relief="flat", bg="#2ED3B7", fg="#0B1220",
               activebackground="#31E3BF", activeforeground="#0B1220", font=("Segoe UI", 10, "bold"),
               width=12, command=self.apply_filter).pack(side=LEFT, padx=(15, 0))

    # ------------------- STATS FRAME -------------------
    def create_stats_frame(self):
        self.stats_section = Frame(self.panel_frame, bg="#151F32")
        self.stats_section.place(x=20, y=510, width=1200, height=80)
        self.update_stats()

    def update_stats(self):
        for widget in self.stats_section.winfo_children():
            widget.destroy()
        stats = [
            ("Total Revenue:", self.calculate_total_rev()),
            ("Total Profit:", self.total_profit_made()),
            ("Total Sales:", self.total_sales_count()),
            ("Total Purchases:", self.total_purchase_count()),
            ("Avg Transaction:", self.avg_transaction_value()),
            ("Last Updated:", self.last_updated())
        ]
        col = 0
        for text, value in stats:
            Label(self.stats_section, text=text, bg="#151F32", fg="#F3F4F6", font=("Segoe UI", 13, "bold"))\
                .grid(row=0, column=col, padx=10, pady=5, sticky="w")
            Label(self.stats_section, text=str(value), bg="#151F32", fg="#2ED3B7", font=("Segoe UI", 13, "bold"))\
                .grid(row=1, column=col, padx=10, pady=5, sticky="w")
            col += 1

    # ------------------- TABLE -------------------
    def create_table_container(self):
        self.table_container = Frame(self.panel_frame, bg="#151F32")
        self.table_container.place(x=20, y=190, width=1200, height=300)

        style = ttk.Style()
        style.theme_use("default")
        style.configure("Treeview",
                        background="#151F32",
                        foreground="#F3F4F6",
                        fieldbackground="#151F32",
                        rowheight=28,
                        bordercolor="#0B1220",
                        relief="flat")
        style.configure("Treeview.Heading",
                        background="#2ED3B7",
                        foreground="#0B1220",
                        font=("Segoe UI", 11, "bold"))
        style.map("Treeview",
                  background=[("selected", "#2ED3B7")],
                  foreground=[("selected", "#0B1220")])

        self.table = ttk.Treeview(self.table_container,
                                  columns=("date", "user", "type", "product", "quantity", "total"),
                                  show="headings")

        headings = ["Date", "User", "Type", "Product", "Quantity", "Total"]
        widths = [120, 100, 100, 200, 100, 120]

        for col, width, heading in zip(self.table["columns"], widths, headings):
            self.table.heading(col, text=heading)
            self.table.column(col, width=width, anchor="center")

        self.table.place(x=0, y=0, width=1150, height=300)

        scrollbar = Scrollbar(self.table_container, orient="vertical", command=self.table.yview,
                              bg="#151F32", troughcolor="#0B1220", bd=0, highlightthickness=0)
        self.table.configure(yscrollcommand=scrollbar.set)
        scrollbar.place(x=1150, y=0, height=300)

    # ------------------- LOAD DATA -------------------
    def load_data(self):
        try:
            cursor = self.dbcon.cursor()

            # Load users
            cursor.execute("SELECT user_id, user_name FROM users")
            users = cursor.fetchall()
            self.user_map = {uid: username for uid, username in users} if users else {}
            user_list = ["All users"] + list(self.user_map.values())
            self.combo_user.config(values=user_list)
            self.combo_user.set("All users")

            # Load products
            cursor.execute("SELECT products_id, name FROM products")
            products = cursor.fetchall()
            self.prdct_map = {pid: name for pid, name in products} if products else {}

            # Load transactions
            cursor.execute("SELECT `date`, user_id, type, products_id, quantity, total_amount FROM transactions")
            rows = cursor.fetchall()
            self.populate_table(rows)

        except mysql.connector.Error as err:
            messagebox.showerror("Database Error", f"Failed to load data:\n{err}", parent=self.reports_win)
        finally:
            cursor.close()

    # ------------------- APPLY FILTER -------------------
    def apply_filter(self, type_filter=None):
        type_val = self.combo_type.get() if not type_filter else type_filter
        user_val = self.combo_user.get()
        date_val = self.combo_date.get()

        query = "SELECT `date`, user_id, type, products_id, quantity, total_amount FROM transactions WHERE 1=1"
        params = []

        if type_val != "Select type...":
            query += " AND type=%s"
            params.append(type_val)

        if user_val != "All users":
            # find user_id by name
            uid = None
            for k, v in self.user_map.items():
                if v == user_val:
                    uid = k
                    break
            if uid:
                query += " AND user_id=%s"
                params.append(uid)

        try:
            cursor = self.dbcon.cursor()
            cursor.execute(query, tuple(params))
            rows = cursor.fetchall()
        except mysql.connector.Error as err:
            messagebox.showerror("Error", f"Failed to fetch transactions:\n{err}", parent=self.reports_win)
            return
        finally:
            cursor.close()

        filtered_rows = []
        today_dt = date.today()
        for r in rows:
            try:
                if isinstance(r[0], datetime):
                    trans_date = r[0].date()
                else:
                    trans_date = datetime.strptime(str(r[0]), "%Y-%m-%d %H:%M:%S").date()
            except:
                continue

            if date_val == "Today" and trans_date != today_dt:
                continue
            elif date_val == "This week":
                start_week = today_dt - timedelta(days=today_dt.weekday())
                end_week = start_week + timedelta(days=6)
                if not (start_week <= trans_date <= end_week):
                    continue
            elif date_val == "This month" and trans_date.month != today_dt.month:
                continue

            filtered_rows.append(r)

        self.populate_table(filtered_rows)

    # ------------------- USER ACTIVITY -------------------
    def user_activity(self):
        popup = Toplevel(self.reports_win)
        popup.geometry("400x400")
        popup.title("User Activity")
        popup.config(bg="#111828")

        content_frame = Frame(popup, bg="#0B1220")
        content_frame.place(x=20, y=50, width=360, height=300)

        heading = Label(popup, text="User Activity", bg="#111828", fg="#F3F4F6", font=("Segoe UI", 20, "bold"))
        heading.place(x=100, y=10)

        Label(content_frame, text="Select User:", bg="#0B1220", fg="#F3F4F6", font=("Segoe UI", 12, "bold")).place(x=20, y=20)
        Label(content_frame, text="Filter By Date:", bg="#0B1220", fg="#F3F4F6", font=("Segoe UI", 12, "bold")).place(x=200, y=20)

        user_list = list(self.user_map.values())
        usr_combo = ttk.Combobox(content_frame, values=user_list, state="readonly", font=("Segoe UI", 11))
        usr_combo.place(x=20, y=50, width=140)
        usr_combo.set("Select user...")

        date_combo = ttk.Combobox(content_frame, values=["Today", "This week", "This month"], state="readonly", font=("Segoe UI", 11))
        date_combo.place(x=200, y=50, width=140)
        date_combo.set("Select filter...")

        total_trans_lbl = Label(content_frame, text="Total Transactions: 0", bg="#0B1220", fg="#F3F4F6",
                                font=("Segoe UI", 12, "bold"))
        total_trans_lbl.place(x=20, y=130)
        total_revenue_lbl = Label(content_frame, text="Total Revenue: 0", bg="#0B1220", fg="#2ED3B7",
                                  font=("Segoe UI", 12, "bold"))
        total_revenue_lbl.place(x=20, y=160)
        total_spent_lbl = Label(content_frame, text="Total Spent: 0", bg="#0B1220", fg="#F3F4F6",
                                font=("Segoe UI", 12, "bold"))
        total_spent_lbl.place(x=20, y=190)

        # Button to calculate stats
        def calc_activity():
            user_name = usr_combo.get()
            date_filter = date_combo.get()
            uid = None
            for k, v in self.user_map.items():
                if v == user_name:
                    uid = k
                    break
            if not uid:
                messagebox.showwarning("Warning", "Select a valid user.")
                return

            query = "SELECT `date`, type, total_amount FROM transactions WHERE user_id=%s"
            params = [uid]
            try:
                cursor = self.dbcon.cursor()
                cursor.execute(query, tuple(params))
                rows = cursor.fetchall()
            except mysql.connector.Error as err:
                messagebox.showerror("Error", f"Failed to fetch data:\n{err}", parent=popup)
                return
            finally:
                cursor.close()

            filtered_rows = []
            today_dt = date.today()
            for r in rows:
                try:
                    if isinstance(r[0], datetime):
                        t_date = r[0].date()
                    else:
                        t_date = datetime.strptime(str(r[0]), "%Y-%m-%d %H:%M:%S").date()
                except:
                    continue

                if date_filter == "Today" and t_date != today_dt:
                    continue
                elif date_filter == "This week":
                    start_week = today_dt - timedelta(days=today_dt.weekday())
                    end_week = start_week + timedelta(days=6)
                    if not (start_week <= t_date <= end_week):
                        continue
                elif date_filter == "This month" and t_date.month != today_dt.month:
                    continue

                filtered_rows.append(r)

            total_trans_lbl.config(text=f"Total Transactions: {len(filtered_rows)}")
            total_revenue = sum(r[2] for r in filtered_rows if r[1] == "Sale")
            total_spent = sum(r[2] for r in filtered_rows if r[1] == "Purchase")
            total_revenue_lbl.config(text=f"Total Revenue: {total_revenue}")
            total_spent_lbl.config(text=f"Total Spent: {total_spent}")

        Button(content_frame, text="Show", bg="#2ED3B7", fg="#0B1220", relief="flat",
               command=calc_activity).place(x=140, y=90)

    # ------------------- POPULATE TABLE -------------------
    def populate_table(self, rows):
        for item in self.table.get_children():
            self.table.delete(item)

        for row in rows:
            t_date, user_id, t_type, prd_id, qtty, total = row
            user_name = self.user_map.get(user_id, user_id)
            prd_name = self.prdct_map.get(prd_id, prd_id)
            self.table.insert("", "end", values=(t_date, user_name, t_type, prd_name, qtty, total))

        self.update_stats()

    # ------------------- PRINT / EXPORT -------------------
    def print_table(self):
        temp_file = "temp_report.csv"
        self.export_csv(temp_file)
        if os.name == "nt":
            os.startfile(temp_file, "print")
        else:
            messagebox.showinfo("Info", f"Print file created at {temp_file}, print manually.")

    def export_csv(self, file_path=None):
        if not file_path:
            file_path = filedialog.asksaveasfilename(defaultextension=".csv",
                                                     filetypes=[("CSV files", "*.csv")])
            if not file_path:
                return
        with open(file_path, mode="w", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow(["Date", "User", "Type", "Product", "Quantity", "Total"])
            for row_id in self.table.get_children():
                writer.writerow(self.table.item(row_id)["values"])
        messagebox.showinfo("Success", f"Report exported as CSV:\n{file_path}")

    def export_pdf(self):
        file_path = filedialog.asksaveasfilename(defaultextension=".pdf",
                                                 filetypes=[("PDF files", "*.pdf")])
        if not file_path:
            return
        c = canvas.Canvas(file_path, pagesize=letter)
        width, height = letter
        x_margin, y_margin = 40, 50
        y_pos = height - y_margin

        c.setFont("Helvetica-Bold", 14)
        c.drawString(x_margin, y_pos, "Inventory Report")
        y_pos -= 30

        headers = ["Date", "User", "Type", "Product", "Quantity", "Total"]
        c.setFont("Helvetica-Bold", 10)
        for i, header in enumerate(headers):
            c.drawString(x_margin + i*90, y_pos, header)
        y_pos -= 20

        c.setFont("Helvetica", 10)
        for row_id in self.table.get_children():
            row = self.table.item(row_id)["values"]
            for i, value in enumerate(row):
                c.drawString(x_margin + i*90, y_pos, str(value))
            y_pos -= 20
            if y_pos < 50:
                c.showPage()
                y_pos = height - y_margin
        c.save()
        messagebox.showinfo("Success", f"Report exported as PDF:\n{file_path}")

    # ------------------- STATS FUNCTIONS -------------------
    def calculate_total_rev(self):
        cursor = self.dbcon.cursor()
        cursor.execute("SELECT SUM(total_amount) FROM transactions WHERE type='Sale'")
        result = cursor.fetchone()[0] or 0
        cursor.close()
        return result

    def total_profit_made(self):
        cursor = self.dbcon.cursor()
        cursor.execute("SELECT SUM(total_amount) FROM transactions WHERE type='Sale'")
        earned = cursor.fetchone()[0] or 0
        cursor.execute("SELECT SUM(total_amount) FROM transactions WHERE type='Purchase'")
        spent = cursor.fetchone()[0] or 0
        cursor.close()
        return earned - spent

    def total_sales_count(self):
        cursor = self.dbcon.cursor()
        cursor.execute("SELECT COUNT(*) FROM transactions WHERE type='Sale'")
        result = cursor.fetchone()[0] or 0
        cursor.close()
        return result

    def total_purchase_count(self):
        cursor = self.dbcon.cursor()
        cursor.execute("SELECT COUNT(*) FROM transactions WHERE type='Purchase'")
        result = cursor.fetchone()[0] or 0
        cursor.close()
        return result

    def avg_transaction_value(self):
        cursor = self.dbcon.cursor()
        cursor.execute("SELECT AVG(total_amount) FROM transactions")
        result = cursor.fetchone()[0] or 0
        cursor.close()
        return round(result, 2)

    def last_updated(self):
        cursor = self.dbcon.cursor()
        cursor.execute("SELECT MAX(`date`) FROM transactions")
        result = cursor.fetchone()[0]
        cursor.close()
        if result:
            return result.strftime("%Y-%m-%d %H:%M:%S")
        return "N/A"

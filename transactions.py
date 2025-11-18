from tkinter import *
from tkinter import ttk
from tkinter import messagebox
import mysql.connector


class TransactionsManager:
    def __init__(self, root):
        self.dbcon = mysql.connector.connect(
            host="localhost",
            user="root",
            password="root",
            database="Inventory_manager_db"
        )
        self.root = root
        self.main_window()
        self.tree_view()

    def main_window(self):
        self.transactions_window = Toplevel()
        self.transactions_window.title("Desktop Inventory Management System")
        self.transactions_window.geometry("1300x800")
        self.transactions_window.config(bg="#111828")

        heading = Label(
            self.transactions_window,
            text="Transactions",
            bg="#111828",
            fg="#F3F4F6",
            font=("Segoe UI", 38, "bold")
        )
        heading.place(x=480, y=5)

        self.content_frame = Frame(self.transactions_window, bg="#0B1220")
        self.content_frame.place(x=30, y=80, width=1240, height=670)

        sub_heading = Label(
            self.content_frame,
            text="Welcome, Admin!",
            bg="#0B1220",
            fg="#8A95B8",
            font=("Segoe UI", 22, "bold")
        )
        sub_heading.place(x=20, y=9)

        underline = Frame(self.content_frame, bg="#2ED3B7", height=3, width=1240)
        underline.place(x=0, y=55)

        self.panel_frame = Frame(self.content_frame, bg="#151F32")
        self.panel_frame.place(x=0, y=80, width=1240, height=590)

        panel_heading = Label(self.panel_frame, text="Transaction Center", bg="#151F32", fg="#F3F4F6",
                              font=("Segoe UI", 19, "bold"))
        panel_heading.place(x=20, y=0)

        controls_frame = Frame(self.panel_frame, bg="#151F32")
        controls_frame.place(x=20, y=40, width=1200, height=60)

        actions_wrapper = Frame(controls_frame, bg="#151F32")
        actions_wrapper.pack(side=LEFT)

        add_tran = Button(
            actions_wrapper,
            text="Add Transaction",
            command=self.open_add_win,
            relief="flat",
            bg="#2ED3B7",
            fg="#0B1220",
            activebackground="#31E3BF",
            activeforeground="#0B1220",
            font=("Segoe UI", 10, "bold"),
            width=16
        )
        add_tran.pack(side=LEFT, padx=5)

        del_tran = Button(
            actions_wrapper,
            text="Delete Transaction",
            command=self.delete_tran,
            relief="flat",
            bg="#F472B6",
            fg="#0B1220",
            activebackground="#F688C5",
            activeforeground="#0B1220",
            font=("Segoe UI", 10, "bold"),
            width=16
        )
        del_tran.pack(side=LEFT, padx=5)

        search_wrapper = Frame(controls_frame, bg="#151F32")
        search_wrapper.pack(side=RIGHT)

        refresh_btn = Button(
            search_wrapper,
            text="⟳ Refresh",
            command=self.refresh_table,
            bg="#0B1220",
            fg="#2ED3B7",
            relief=FLAT,
            activebackground="#1C2A43",
            activeforeground="#31E3BF",
            font=("Segoe UI", 10, "bold"),
            width=12
        )
        refresh_btn.pack(side=RIGHT, padx=(10, 0))

        self.entry = Entry(search_wrapper, width=28, font=("Segoe UI", 12),
                           bg="#0B1220", fg="#F3F4F6",
                           insertbackground="#2ED3B7",
                           highlightbackground="#2ED3B7",
                           highlightcolor="#2ED3B7",
                           relief=FLAT)
        self.entry.pack(side=RIGHT, padx=5)
        self.entry.bind("<Return>", self.search_bind)

        search_sup = Label(
            search_wrapper,
            text="Search",
            bg="#151F32",
            fg="#F3F4F6",
            font=("Segoe UI", 12, "bold")
        )
        search_sup.pack(side=RIGHT, padx=5)

        self.table_container = Frame(self.panel_frame, bg="#151F32")
        self.table_container.place(x=20, y=120, width=1200, height=430)

        self.transactions_window.protocol("WM_DELETE_WINDOW", self.close_connection)

    def tree_view(self):
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

        self.table = ttk.Treeview(
            self.table_container,
            columns=("transaction_id", "products_id", "user_id", "type", "unit_price",
                     "quantity", "total_amount", "date"),
            show="headings"
        )

        headings = {
            "transaction_id": "Transaction ID",
            "products_id": "Product ID",
            "user_id": "User ID",
            "type": "Type (purchase/sale)",
            "unit_price": "Unit Price",
            "quantity": "Quantity",
            "total_amount": "Total",
            "date": "Date"
        }

        widths = {
            "transaction_id": 100,
            "products_id": 100,
            "user_id": 100,
            "type": 140,
            "unit_price": 100,
            "quantity": 80,
            "total_amount": 100,
            "date": 120
        }

        for col in headings:
            self.table.heading(col, text=headings[col])
            self.table.column(col, width=widths[col])

        self.table.place(x=0, y=0, width=1150, height=430)

        self.scroll = Scrollbar(self.table_container, orient="vertical", command=self.table.yview,
                                bg="#151F32", troughcolor="#0B1220", bd=0, highlightthickness=0)
        self.table.configure(yscrollcommand=self.scroll.set)
        self.scroll.place(x=1150, y=0, height=430)

        self.load_transactions()

    def load_transactions(self):
        cursor = self.dbcon.cursor()
        cursor.execute("select * from transactions")
        rows = cursor.fetchall()

        for item in self.table.get_children():
            self.table.delete(item)

        for row in rows:
            self.table.insert("", "end", values=row)

    def open_add_win(self):
        self.add_window()

    def add_window(self):
        self.add_win_popup = Toplevel()
        self.add_win_popup.geometry("500x500")
        self.add_win_popup.config(bg="#111828")

        content_frame = Frame(self.add_win_popup,bg="#0B1220")
        content_frame.place(x=50, y=70,width=400,height=350)

        heading1 = Label(self.add_win_popup, text="Add new transaction",bg="#111828",fg="#F3F4F6",font=("Segoe UI",20,"bold"))
        heading1.place(x=130,y=20)

        lbl1 = Label(content_frame,text="Product Name",bg="#0B1220",fg="#F3F4F6",font=("Segoe UI",11))
        lbl1.place(x=20,y=20)

        cursor = self.dbcon.cursor()
        cursor.execute("select products_id, name from products")
        result = cursor.fetchall()

        self.prdct_map = {name: pid for pid, name in result}
        cursor.close()

        if not self.prdct_map:
            messagebox.showerror("Error","No products found in database.",parent=self.add_win_popup)
            return

        self.combo1 = ttk.Combobox(content_frame,values=list(self.prdct_map.keys()),state="readonly",font=("Segoe UI",11))
        self.combo1.place(x=210,y=20)

        lbl2 = Label(content_frame, text="User Role",bg="#0B1220",fg="#F3F4F6",font=("Segoe UI",11))
        lbl2.place(x=20,y=60)

        cursor = self.dbcon.cursor()
        cursor.execute("select user_id, role from users")
        result1 = cursor.fetchall()

        self.user_map = {role: uid for uid,role in result1}
        cursor.close()

        if not self.user_map:
            messagebox.showerror("Error","No users found in database.",parent=self.add_win_popup)
            return

        self.combo2 = ttk.Combobox(content_frame,values= list(self.user_map.keys()),state="readonly",font=("Segoe UI",11))
        self.combo2.place(x=210,y=60)

        lbl3 = Label(content_frame, text="Type",bg="#0B1220",fg="#F3F4F6",font=("Segoe UI",11))
        lbl3.place(x=20,y=100)
        type_options = ["Purchase", "Sale"]
        self.combo3 = ttk.Combobox(content_frame,values= type_options,state="readonly",font=("Segoe UI",11))
        self.combo3.place(x=210,y=100)

        lbl4 = Label(content_frame, text="Unit Price",bg="#0B1220",fg="#F3F4F6",font=("Segoe UI",11))
        lbl4.place(x=20,y=140)
        common_entry = dict(width=18,font=("Segoe UI",13),bg="#151F32",fg="#F3F4F6",
                            insertbackground="#2ED3B7",highlightbackground="#2ED3B7",
                            highlightcolor="#2ED3B7",relief=FLAT)

        self.entry2 = Entry(content_frame,**common_entry)
        self.entry2.place(x=210,y=140)

        lbl5 = Label(content_frame, text="Quantity",bg="#0B1220",fg="#F3F4F6",font=("Segoe UI",11))
        lbl5.place(x=20,y=180)
        self.entry3 = Entry(content_frame,**common_entry)
        self.entry3.place(x=210,y=180)

        def add_n_close():
            product = self.combo1.get().strip()
            user = self.combo2.get().strip()
            tran_type = self.combo3.get().strip()

            if not product or not user or not tran_type:
                messagebox.showwarning("Warning", "Please fill all the dropdowns.", parent=self.add_win_popup)
                return

            prdct_id = self.prdct_map[product]
            u_id = self.user_map[user]

            try:
                uni_p = float(self.entry2.get().strip())
                qtty = int(self.entry3.get().strip())

            except ValueError:
                messagebox.showwarning("Warning","Please enter a numeric value for respective fields.",parent=self.add_win_popup)
                return

            ttl_amnt = qtty * uni_p

            cursor = self.dbcon.cursor()

            try:
                cursor.execute("insert into transactions(products_id,user_id,type,unit_price,quantity,total_amount) values(%s,%s,%s,%s,%s,%s)",(prdct_id,u_id,tran_type,uni_p,qtty,ttl_amnt))

                if tran_type.lower() == "purchase":
                    cursor.execute("update products set quantity = quantity + %s where products_id = %s",(qtty,prdct_id))

                elif tran_type.lower() == "sale":
                    cursor.execute("select quantity from products where products_id = %s",(prdct_id,))
                    quantity = cursor.fetchone()[0]

                    if quantity < qtty:
                        messagebox.showerror("Failed",f"Transaction failed - not enough stock for item: {product}.",parent=self.add_win_popup)
                        self.dbcon.rollback()
                        return

                    cursor.execute("update products set quantity = quantity - %s where products_id = %s",(qtty,prdct_id))

                self.dbcon.commit()
                messagebox.showinfo("Success", "Data successfully added to the database.", parent=self.add_win_popup)
                self.load_transactions()
                self.add_win_popup.destroy()

            except mysql.connector.Error as err:
                messagebox.showerror("Database Error",str(err),parent=self.add_win_popup)
                return

            finally:
                cursor.close()

        save_but = Button(content_frame,text="Save",command=add_n_close,font=("Segoe UI",10,"bold"),
                          fg="#0B1220",bg="#2ED3B7",relief="flat",width=12,height=2,
                          activebackground="#31E3BF",activeforeground="#0B1220")
        save_but.place(x=150,y=250)

    def delete_tran(self):
        items = self.table.selection()
        if not items:
            messagebox.showwarning("Warning", "Please select at least one record to delete.",
                                   parent=self.transactions_window)
            return

        confirmation = messagebox.askyesno("Confirm Deletion",
                                           "Are you sure you want to delete the selected record(s)?",
                                           parent=self.transactions_window)
        if not confirmation:
            return

        cursor = self.dbcon.cursor()
        try:
            for item in items:
                tran_id = self.table.item(item)["values"][0]

                cursor.execute("select products_id,type,quantity from transactions where transaction_id = %s",
                               (tran_id,))
                prdct_id, tran_type, tran_qtty = cursor.fetchone()

                # Correct stock adjustment
                if tran_type.lower() == "purchase":
                    cursor.execute("update products set quantity = quantity - %s where products_id = %s",
                                   (tran_qtty, prdct_id))
                elif tran_type.lower() == "sale":
                    cursor.execute("update products set quantity = quantity + %s where products_id = %s",
                                   (tran_qtty, prdct_id))

                cursor.execute("delete from transactions where transaction_id = %s", (tran_id,))

            self.dbcon.commit()
            messagebox.showinfo("Success", "Transaction(s) successfully deleted.", parent=self.transactions_window)
            self.load_transactions()

        except mysql.connector.Error as err:
            self.dbcon.rollback()
            messagebox.showerror("Database Error", str(err), parent=self.transactions_window)
        finally:
            cursor.close()

    def search_bind(self,event):
        self.search_tran()

    def search_tran(self):
        like_val = self.entry.get().strip()

        if not like_val:
            messagebox.showwarning("Warning","Input required in the field.",parent=self.transactions_window)
            return

        like_val = f"%{like_val}%"

        cursor = self.dbcon.cursor()
        cursor.execute("select * from transactions where transaction_id like %s or products_id like %s or user_id like %s or type like %s or unit_price like %s or quantity like %s or total_amount like %s or date like %s",(like_val,like_val,like_val,like_val,like_val,like_val,like_val,like_val))
        rows = cursor.fetchall()
        cursor.close()

        if not rows:
            messagebox.showerror("No match","No match have been found in the database.",parent=self.transactions_window)
            return

        for item in self.table.get_children():
            self.table.delete(item)

        for row in rows:
            self.table.insert("","end",values=row)

    def refresh_table(self):
        self.entry.delete(0,END)
        self.load_transactions()

    def close_connection(self):
        try:
            if self.dbcon.is_connected():
                self.dbcon.close()

        finally:
            self.transactions_window.destroy()




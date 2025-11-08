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
        self.transactions_window.config(bg="#1E1E1E")

        heading = Label(
            self.transactions_window,
            text="Transactions",
            bg="#1E1E1E",
            fg="White",
            font=("Georgia", 38, "bold")
        )
        heading.place(x=480, y=10)

        self.content_frame = Frame(self.transactions_window, bg="#F1F0F0")
        self.content_frame.place(x=30, y=80, width=1240, height=670)

        sub_heading = Label(
            self.content_frame,
            text="Welcome, Admin!",
            bg="#F1F0F0",
            fg="#1E1E1E",
            font=("TkDefaultFont", 22, "bold")
        )
        sub_heading.place(x=20, y=10)

        underline = Frame(self.content_frame, bg="#1E1E1E", height=3, width=1240)
        underline.place(x=0, y=55)

        add_tran = Button(
            self.content_frame,
            text="Add Transaction",
            command=self.open_add_win,
            relief="flat",
            bg="#3962A3",
            fg="White",
            activebackground="#3962A3",
            activeforeground="White",
            font=("Arial", 9)
        )
        add_tran.place(x=30, y=80)

        del_tran = Button(
            self.content_frame,
            text="Delete Transaction",
            command=self.delete_tran,
            relief="flat",
            bg="#F42325",
            fg="White",
            activebackground="#F42325",
            activeforeground="White",
            font=("Arial", 9)
        )
        del_tran.place(x=150, y=80)

        search_sup = Label(
            self.content_frame,
            text="Search",
            bg="#F1F0F0",
            fg="#1E1E1E",
            font=("Arial", 11, "bold")
        )
        search_sup.place(x=300, y=82)

        self.entry = Entry(self.content_frame, width=25, font=("Arial", 12))
        self.entry.place(x=370, y=83)
        self.entry.bind("<Return>", self.search_bind)

        refresh_btn = Button(
            self.content_frame,
            text="⟳ Refresh",
            command=self.refresh_table,
            bg="#2ECC71",
            fg="white",
            relief=FLAT,
            activebackground="#48C9B0",
            font=("Arial", 9)
        )
        refresh_btn.place(x=730, y=80)

        self.transactions_window.protocol("WM_DELETE_WINDOW", self.close_connection)

    def tree_view(self):
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

        self.table = ttk.Treeview(
            self.transactions_window,
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

        self.table.place(x=60, y=230, width=1180, height=500)

        self.scroll = Scrollbar(self.content_frame, orient="vertical", command=self.table.yview)
        self.table.configure(yscrollcommand=self.scroll.set)
        self.scroll.place(x=1220, y=160, height=540)

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
        self.add_win_popup.config(bg="#1E1E1E")

        content_frame = Frame(self.add_win_popup,bg="White")
        content_frame.place(x=50, y=70,width=400,height=350)

        heading1 = Label(self.add_win_popup, text="Add new transaction",bg="#1E1E1E",fg="White",font=("Georgia",20,"bold"))
        heading1.place(x=130,y=20)

        lbl1 = Label(content_frame,text="Product Name",bg="White",fg="Black",font=("Arial",10))
        lbl1.place(x=20,y=20)

        cursor = self.dbcon.cursor()
        cursor.execute("select products_id, name from products")
        result = cursor.fetchall()

        self.prdct_map = {name: pid for pid, name in result}
        cursor.close()

        if not self.prdct_map:
            messagebox.showerror("Error","No products found in database.",parent=self.add_win_popup)
            return

        self.combo1 = ttk.Combobox(content_frame,values=list(self.prdct_map.keys()),state="readonly")
        self.combo1.place(x=210,y=20)

        lbl2 = Label(content_frame, text="User Role",bg="White",fg="Black",font=("Arial",10))
        lbl2.place(x=20,y=60)

        cursor = self.dbcon.cursor()
        cursor.execute("select user_id, role from users")
        result1 = cursor.fetchall()

        self.user_map = {role: uid for uid,role in result1}
        cursor.close()

        if not self.user_map:
            messagebox.showerror("Error","No users found in database.",parent=self.add_win_popup)
            return

        self.combo2 = ttk.Combobox(content_frame,values= list(self.user_map.keys()),state="readonly")
        self.combo2.place(x=210,y=60)

        lbl3 = Label(content_frame, text="Type",bg="White",fg="Black",font=("Arial",10))
        lbl3.place(x=20,y=100)
        type_options = ["Purchase", "Sale"]
        self.combo3 = ttk.Combobox(content_frame,values= type_options,state="readonly")
        self.combo3.place(x=210,y=100)

        lbl4 = Label(content_frame, text="Unit Price",bg="White",fg="Black",font=("Arial",10))
        lbl4.place(x=20,y=140)
        self.entry2 = Entry(content_frame,width=18,font=("Arial",13),bg="#FEFAEA",fg="Black")
        self.entry2.place(x=210,y=140)

        lbl5 = Label(content_frame, text="Quantity",bg="White",fg="Black",font=("Arial",10))
        lbl5.place(x=20,y=180)
        self.entry3 = Entry(content_frame,width=18,font=("Arial",13),bg="#FEFAEA",fg="Black")
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

        save_but = Button(content_frame,text="Save",command=add_n_close,font=("Arial",8,"bold"),fg="White",bg="Green",relief="flat",width=10,height=2,activebackground="Green",activeforeground="White")
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




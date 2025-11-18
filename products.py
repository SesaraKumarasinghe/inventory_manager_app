from tkinter import *
from tkinter import ttk
import mysql.connector
from tkinter import messagebox

class ProductsManager:
    def __init__(self, root):

        self.dbcon = mysql.connector.connect(
            host="localhost",
            user="root",
            password="root",
            database="Inventory_manager_db"
        )

        self.root = root
        self.main_window()
        self.setup_treeview()

    def main_window(self):
        self.products_window = Toplevel()
        self.products_window.title("Desktop Inventory Management System")
        self.products_window.geometry("1300x800")  # 🔹 Reduced window size
        self.products_window.config(bg="#111828")

        heading = Label(self.products_window, text="Products", bg="#111828", fg="#F3F4F6", font=("Segoe UI", 42, "bold"))
        heading.place(x=520, y=10)

        self.main_frame = Frame(self.products_window, bg="#0B1220")
        self.main_frame.place(x=30, y=80, width=1240, height=670)

        sub_heading = Label(self.main_frame, text="Welcome, Admin!", bg="#0B1220", fg="#8A95B8",
                            font=("Segoe UI", 24, "bold"))
        sub_heading.place(x=20, y=10)

        underline = Frame(self.main_frame, bg="#2ED3B7", height=3, width=1240)
        underline.place(x=0, y=55)

        self.content_panel = Frame(self.main_frame, bg="#151F32")
        self.content_panel.place(x=0, y=80, width=1240, height=590)

        panel_heading = Label(self.content_panel, text="Manage Products", bg="#151F32", fg="#F3F4F6",
                              font=("Segoe UI", 22, "bold"))
        panel_heading.place(x=20, y=0)

        controls_frame = Frame(self.content_panel, bg="#151F32")
        controls_frame.place(x=20, y=40, width=1200, height=60)

        actions_wrapper = Frame(controls_frame, bg="#151F32")
        actions_wrapper.pack(side=LEFT, padx=5)

        add_prdct = Button(actions_wrapper, text="Add Product", command=self.open_add_win, relief=FLAT,
                           bg="#2ED3B7", fg="#0B1220", activebackground="#31E3BF", activeforeground="#0B1220",
                           font=("Segoe UI", 10, "bold"), width=14)
        add_prdct.pack(side=LEFT, padx=5)

        updte_prdct = Button(actions_wrapper, text="Update Product", command=self.update_window, relief=FLAT,
                             bg="#1C2A43", fg="#F3F4F6", activebackground="#223555", activeforeground="#2ED3B7",
                             font=("Segoe UI", 10, "bold"), width=14)
        updte_prdct.pack(side=LEFT, padx=5)

        del_prdct = Button(actions_wrapper, text="Delete Product", command=self.delete_prdct, relief=FLAT,
                           bg="#F472B6", fg="#0B1220", activebackground="#F688C5", activeforeground="#0B1220",
                           font=("Segoe UI", 10, "bold"), width=14)
        del_prdct.pack(side=LEFT, padx=5)

        search_wrapper = Frame(controls_frame, bg="#151F32")
        search_wrapper.pack(side=RIGHT, padx=5)

        self.entry = Entry(search_wrapper, width=28, font=("Segoe UI", 12), bg="#0B1220", fg="#F3F4F6",
                           insertbackground="#2ED3B7", highlightbackground="#2ED3B7", highlightcolor="#2ED3B7",
                           relief=FLAT)
        self.entry.pack(side=RIGHT, padx=(5, 0))
        self.entry.bind("<Return>", self.search_bind)

        search_lbl = Label(search_wrapper, text="Search", bg="#151F32", fg="#F3F4F6", font=("Segoe UI", 12, "bold"))
        search_lbl.pack(side=RIGHT, padx=(0, 8))

        refresh_btn = Button(search_wrapper, text="⟳ Refresh", command=self.refresh_table, bg="#0B1220", fg="#2ED3B7",
                             relief=FLAT, activebackground="#1C2A43", activeforeground="#31E3BF",
                             font=("Segoe UI", 10, "bold"), width=12)
        refresh_btn.pack(side=RIGHT, padx=5)

    def setup_treeview(self):
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
            self.content_panel,
            columns=("products_id", "name", "catagory_id", "supplier_id", "price", "quantity"),
            show="headings"
        )

        self.table.heading("products_id", text="Product ID")
        self.table.column("products_id", width=100, anchor="center")

        self.table.heading("name", text="Product Name")
        self.table.column("name", width=220, anchor="w")

        self.table.heading("catagory_id", text="Category ID")
        self.table.column("catagory_id", width=120, anchor="center")

        self.table.heading("supplier_id", text="Supplier ID")
        self.table.column("supplier_id", width=120, anchor="center")

        self.table.heading("price", text="Price")
        self.table.column("price", width=100, anchor="center")

        self.table.heading("quantity", text="Quantity")
        self.table.column("quantity", width=100, anchor="center")

        table_container = Frame(self.content_panel, bg="#151F32")
        table_container.place(x=20, y=120, width=1200, height=450)

        self.table.place(in_=table_container, x=0, y=0, width=1150, height=450)

        self.scroll = Scrollbar(table_container, orient="vertical", command=self.table.yview, bg="#151F32",
                                troughcolor="#0B1220", activebackground="#2ED3B7", bd=0, highlightthickness=0)
        self.table.configure(yscrollcommand=self.scroll.set)
        self.scroll.place(x=1150, y=0, height=450)

        self.load_products()

    def load_products(self):
        cursor = self.dbcon.cursor()
        cursor.execute("select * from products")
        rows = cursor.fetchall()

        for item in self.table.get_children():
            self.table.delete(item)

        for row in rows:
            self.table.insert("", "end", values=row)
        cursor = self.dbcon.cursor()
        cursor.execute("select * from products")
        rows = cursor.fetchall()

        for item in self.table.get_children():
            self.table.delete(item)

        for row in rows:
            self.table.insert("","end",values=row)

    def open_add_win(self):
        self.add_window()

    def add_window(self):
        self.add_win_popup = Toplevel()
        self.add_win_popup.geometry("500x500")
        self.add_win_popup.config(bg="#111828")

        content_frame = Frame(self.add_win_popup,bg="#0B1220")
        content_frame.place(x=50, y=70,width=400,height=350)

        heading1 = Label(self.add_win_popup, text="Add new product",bg="#111828",fg="#F3F4F6",font=("Segoe UI",20,"bold"))
        heading1.place(x=130,y=20)

        lbl1 = Label(content_frame, text="Enter product ID",bg="#0B1220",fg="#F3F4F6",font=("Segoe UI",11))
        lbl1.place(x=20,y=20)
        lbl3 = Label(content_frame, text="Enter product name",bg="#0B1220",fg="#F3F4F6",font=("Segoe UI",11))
        lbl3.place(x=20,y=60)
        lbl4 = Label(content_frame, text="Enter catagory",bg="#0B1220",fg="#F3F4F6",font=("Segoe UI",11))
        lbl4.place(x=20,y=100)
        lbl5 = Label(content_frame, text="Enter supplier",bg="#0B1220",fg="#F3F4F6",font=("Segoe UI",11))
        lbl5.place(x=20,y=140)
        lbl6 = Label(content_frame, text="Enter price",bg="#0B1220",fg="#F3F4F6",font=("Segoe UI",11))
        lbl6.place(x=20,y=180)
        lbl7 = Label(content_frame, text="Enter quantity",bg="#0B1220",fg="#F3F4F6",font=("Segoe UI",11))
        lbl7.place(x=20, y=220)

        entry_args = dict(width=18,font=("Segoe UI",13),bg="#151F32",fg="#F3F4F6",
                          insertbackground="#2ED3B7",highlightbackground="#2ED3B7",
                          highlightcolor="#2ED3B7",relief=FLAT)

        self.entry2 = Entry(content_frame,**entry_args)
        self.entry2.place(x=210,y=20)
        self.entry3 = Entry(content_frame,**entry_args)
        self.entry3.place(x=210,y=60)

        cursor = self.dbcon.cursor()
        cursor.execute("select catagory_id, catagory_name from catagories")
        result = cursor.fetchall()
        cursor.close()

        self.cat_map = {name:cid for cid,name in result}

        self.combo1 = ttk.Combobox(content_frame, values=list(self.cat_map.keys()), state="readonly")
        self.combo1.place(x=210,y=100)
        
        cursor = self.dbcon.cursor()
        cursor.execute("select supplier_id, name from suppliers")
        result2 = cursor.fetchall()
        cursor.close()

        self.sup_map = {name:sid for sid,name in result2}

        self.combo2 = ttk.Combobox(content_frame, values= list(self.sup_map.keys()),state="readonly")
        self.combo2.place(x=210,y=140)

        self.entry7 = Entry(content_frame,**entry_args)
        self.entry7.place(x=210,y=180)
        self.entry8 = Entry(content_frame,**entry_args)
        self.entry8.place(x=210,y=220)

        def add_n_close():
            prdct_id = self.entry2.get().strip()
            prdct_nm = self.entry3.get().strip()
            cat_name = self.combo1.get().strip()
            sup_name = self.combo2.get().strip()
            price =  self.entry7.get().strip()
            qtty = self.entry8.get().strip()

            cat_id = self.cat_map.get(cat_name)
            sup_id = self.sup_map.get(sup_name)

            if not prdct_id or not prdct_nm or not cat_id or not sup_id or not price or not qtty:
                messagebox.showwarning("Warning","Please don't leave any spaces behind.",parent=self.add_win_popup)
                return
            
            if not prdct_id.isdigit():
                messagebox.showwarning("Warning","Product ID must be a numerical value.",parent=self.add_win_popup)   
                return

            if prdct_nm.isdigit():
                messagebox.showwarning("Warning","Product name cannot contain digits.",parent=self.add_win_popup)
                return

            if not price.isdigit():
                messagebox.showwarning("Warning","Please enter numerical values for the price.",parent=self.add_win_popup)
                return

            if not qtty.isdigit():
                messagebox.showwarning("Warning","Please enter numerical values for the quantity.",parent=self.add_win_popup)
                return
            
            cursor = self.dbcon.cursor()

            try:
                cursor.execute("insert into products(products_id,name,catagory_id,supplier_id,price,quantity) values(%s,%s,%s,%s,%s,%s)",(prdct_id,prdct_nm,cat_id,sup_id,price,qtty))
                self.dbcon.commit()

            except mysql.connector.IntegrityError:
                messagebox.showerror("Duplicate Data","Data you have added already exists in the database.",parent=self.add_win_popup)
                return

            except mysql.connector.Error as err:
                messagebox.showerror("Database Error",str(err),parent=self.add_win_popup)
                return

            finally:
                cursor.close()

            messagebox.showinfo("Success","Data added successfully!",parent=self.add_win_popup)
            self.load_products()
            self.add_win_popup.destroy()


        save_but = Button(content_frame,text="Save",font=("Segoe UI",10,"bold"),command=add_n_close,
                          fg="#0B1220",bg="#2ED3B7",relief=FLAT,width=12,height=2,
                          activebackground="#31E3BF",activeforeground="#0B1220")
        save_but.place(x=150,y=270)

    def open_update_win(self):
        self.update_window()

    def update_window(self):
        self.update_win_popup = Toplevel()
        self.update_win_popup.geometry("500x500")
        self.update_win_popup.config(bg="#111828")

        content_frame = Frame(self.update_win_popup,bg="#0B1220")
        content_frame.place(x=50, y=100,width=400,height=350)

        prdct_id = Label(self.update_win_popup, text="Enter Product ID",bg="#111828",fg="#F3F4F6",font=("Segoe UI",11,"bold"))
        prdct_id.place(x=20,y=20)

        self.entry8 = Entry(self.update_win_popup,width=25,font=("Segoe UI",13),bg="#151F32",fg="#F3F4F6",
                             insertbackground="#2ED3B7",highlightbackground="#2ED3B7",highlightcolor="#2ED3B7",
                             relief=FLAT)
        self.entry8.place(x=130,y=20)

        lbl1 = Label(content_frame, text="Enter new product ID",bg="#0B1220",fg="#F3F4F6",font=("Segoe UI",11))
        lbl1.place(x=20,y=20)

        lbl3 = Label(content_frame, text="Enter new product name",bg="#0B1220",fg="#F3F4F6",font=("Segoe UI",11))
        lbl3.place(x=20,y=60)

        lbl4 = Label(content_frame, text="Enter new catagory",bg="White",fg="Black",font=("Arial",10))
        lbl4.place(x=20,y=100)

        lbl5 = Label(content_frame, text="Enter new supplier",bg="White",fg="Black",font=("Arial",10))
        lbl5.place(x=20,y=140)

        lbl6 = Label(content_frame, text="Enter new price",bg="White",fg="Black",font=("Arial",10))
        lbl6.place(x=20,y=180)

        lbl7 = Label(content_frame, text="Enter new quantity",bg="White",fg="Black",font=("Arial",10))
        lbl7.place(x=20, y=220)

        common_entry = dict(width=18,font=("Segoe UI",13),bg="#151F32",fg="#F3F4F6",
                            insertbackground="#2ED3B7",highlightbackground="#2ED3B7",
                            highlightcolor="#2ED3B7",relief=FLAT)

        self.entry9 = Entry(content_frame,**common_entry)
        self.entry9.place(x=210,y=20)

        self.entry10 = Entry(content_frame,**common_entry)
        self.entry10.place(x=210,y=60)
        
        cursor = self.dbcon.cursor()
        cursor.execute("select catagory_id, catagory_name from catagories")
        result = cursor.fetchall()
        cursor.close()

        self.new_cat_map = {name:cid for cid,name in result}

        self.combo3 = ttk.Combobox(content_frame,values=list(self.new_cat_map.keys()),state="readonly")
        self.combo3.place(x=210,y=100)

        cursor = self.dbcon.cursor()
        cursor.execute("select supplier_id, name from suppliers")
        result2 = cursor.fetchall()
        cursor.close()

        self.new_sup_map = {name:sid for sid,name in result2}

        self.combo4 = ttk.Combobox(content_frame,values=list(self.new_sup_map.keys()),state="readonly")
        self.combo4.place(x=210,y=140)

        self.entry11 = Entry(content_frame,**common_entry)
        self.entry11.place(x=210,y=180)
        self.entry12 = Entry(content_frame,**common_entry)
        self.entry12.place(x=210,y=220)

        def search_id():
            prdct_id = self.entry8.get().strip()

            if not prdct_id:
                messagebox.showwarning("Warning","Please don't leave any spaces behind.",parent=self.update_win_popup)
                return

            if not prdct_id.isdigit():
                messagebox.showwarning("Warning","Product ID must be a numerical value.",parent=self.update_win_popup)
                return
            
            cursor = self.dbcon.cursor()
            cursor.execute("select * from products where products_id = %s",(prdct_id,))
            available = cursor.fetchone()

            if available:
                messagebox.showinfo("Item Found",f"Product ID {prdct_id} exists in the database.\nYou may continue.",parent=self.update_win_popup)
                return
            
            else:
                messagebox.showerror("Not Found",f"Product ID {prdct_id} does not exist in the database.",parent=self.update_win_popup)
                return

        def update_n_close():
            old_id = self.entry8.get().strip()
            new_id = self.entry9.get().strip()
            new_nm = self.entry10.get().strip()
            new_cat = self.combo3.get().strip()
            new_sup = self.combo4.get().strip()
            new_price = self.entry11.get().strip()
            new_qtty = self.entry12.get().strip()

            if not old_id:
                messagebox.showwarning("Warning","Please enter current product ID.",parent=self.update_win_popup)
                return
            
            if not old_id.isdigit():
                messagebox.showwarning("Warning","Current product ID must be a numerical value.",parent=self.update_win_popup)   
                return       

            cursor = self.dbcon.cursor()
            cursor.execute("SELECT COUNT(*) FROM products WHERE products_id = %s", (old_id,))
            exists = cursor.fetchone()[0]

            if exists == 0:
                cursor.close()
                messagebox.showerror("Not Found",f"Product ID {old_id} does not exist in the database.\nPlease enter a valid ID.",parent=self.update_win_popup)
                return

            if not (old_id and new_id and new_nm and new_cat and new_sup and new_price and new_qtty):
                messagebox.showwarning("Warning","Please don't leave any spaces behind.",parent=self.update_win_popup)
                return   
            
            if not new_id.isdigit():
                messagebox.showwarning("Warning","Product ID must be a numerical value.",parent=self.update_win_popup)   
                return

            if new_nm.isdigit():
                messagebox.showwarning("Warning","Product name cannot contain digits.",parent=self.update_win_popup)
                return

            if new_cat not in self.new_cat_map or new_sup not in self.new_sup_map:
                messagebox.showwarning("Warning","Please select both a category and supplier.",parent=self.update_win_popup)
                return

            new_cat_id = self.new_cat_map[new_cat]
            new_sup_id = self.new_sup_map[new_sup]

            if not new_price.isdigit():
                messagebox.showwarning("Warning","Please enter numerical values for the price.",parent=self.update_win_popup)
                return
            
            if not new_qtty.isdigit():
                messagebox.showwarning("Warning","Please enter numerical values for the quantity.",parent=self.update_win_popup)
                return                
            
            try:
                cursor = self.dbcon.cursor()
                cursor.execute("update products set products_id = %s, name = %s, catagory_id = %s, supplier_id = %s, price = %s, quantity = %s where products_id = %s",(new_id,new_nm,new_cat_id,new_sup_id,new_price,new_qtty,old_id))
                self.dbcon.commit()

            except mysql.connector.IntegrityError:
                messagebox.showerror("Update Failed","Data you have entered already exists please try again.",parent=self.update_win_popup)
                return
            
            except mysql.connector.Error as err:
                messagebox.showerror("Database Error",str(err),parent=self.update_win_popup)
                return
            
            finally:
                cursor.close()

            messagebox.showinfo("Success","Data updated successfully",parent=self.update_win_popup)
            self.load_products()
            self.update_win_popup.destroy()
            
        Button(self.update_win_popup, text="Search", command=search_id, font=("Segoe UI",9,"bold"),
        fg="#0B1220", bg="#2ED3B7", activebackground="#31E3BF", activeforeground="#0B1220", width=10, height=1).place(x=390, y=20)
            
        save_but = Button(content_frame,text="Save",font=("Segoe UI",10,"bold"),fg="#0B1220",bg="#2ED3B7",
                          command=update_n_close,relief=FLAT,width=12,height=2,activebackground="#31E3BF",
                          activeforeground="#0B1220")
        save_but.place(x=150,y=270)

    def delete_prdct(self):
        selected_items = self.table.selection() 

        if not selected_items:
            messagebox.showwarning("Error","No item(s) selected.",parent=self.products_window)  
            return

        confirmation = messagebox.askyesno("Confirmation","Do you confirm to delete the selected item(s)?",parent=self.products_window)     

        if not confirmation:
            return
        
        cursor = self.dbcon.cursor()

        for item in selected_items:
            values = self.table.item(item,"values")
            prdct_id = values[0]

            cursor.execute("delete from products where products_id = %s",(prdct_id,))
            self.table.delete(item)

        self.dbcon.commit()
        cursor.close()
        self.load_products()
        messagebox.showinfo("Deleted","Deletion successful.",parent=self.products_window)

    def search_bind(self,event):
        self.search_prdct()

    def search_prdct(self):
        value = self.entry.get().strip()

        if not value:
            messagebox.showwarning("No Input","No input entered in the field.",parent=self.products_window)
            return
        
        cursor = self.dbcon.cursor()
        like_val = f"%{value}%"
        cursor.execute("""
            SELECT * FROM products 
            WHERE products_id LIKE %s OR name LIKE %s OR catagory_id LIKE %s 
            OR supplier_id LIKE %s OR price LIKE %s OR quantity LIKE %s
            """, (like_val, like_val, like_val, like_val, like_val, like_val))
        rows = cursor.fetchall()
        cursor.close()

        for item in self.table.get_children():
            self.table.delete(item)
            
        for row in rows:
            self.table.insert("","end",values=row)

        if not rows:
            messagebox.showinfo("No Match","No matching result found.",parent=self.products_window)
            return
        
    def refresh_table(self):
        self.load_products()

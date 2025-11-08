efrom tkinter import *
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
        self.products_window.config(bg="#1E1E1E")

        heading = Label(self.products_window, text="Products", bg="#1E1E1E", fg="White", font=("Georgia", 42, "bold"))
        heading.place(x=520, y=10)

        self.main_frame = Frame(self.products_window, bg="#F1F0F0")
        self.main_frame.place(x=30, y=80, width=1240, height=670)

        sub_heading = Label(self.main_frame, text="Welcome, Admin!", bg="#F1F0F0", fg="#1E1E1E",
                            font=("TkDefaultFont", 24, "bold"))
        sub_heading.place(x=20, y=10)

        underline = Frame(self.main_frame, bg="#1E1E1E", height=3, width=1240)
        underline.place(x=0, y=55)

        add_prdct = Button(self.main_frame, text="Add Product", command=self.open_add_win, relief=FLAT,
                           bg="#3962A3", fg="White", activebackground="#3962A3", activeforeground="White",
                           font=("Arial", 9))
        add_prdct.place(x=30, y=80)

        updte_prdct = Button(self.main_frame, text="Update Product", command=self.update_window, relief=FLAT,
                             bg="#359E0B", fg="White", activebackground="#359E0B", activeforeground="White",
                             font=("Arial", 9))
        updte_prdct.place(x=140, y=80)

        del_prdct = Button(self.main_frame, text="Delete Product", command=self.delete_prdct, relief=FLAT,
                           bg="#F42325", fg="White", activebackground="#F42325", activeforeground="White",
                           font=("Arial", 9))
        del_prdct.place(x=270, y=80)

        search_lbl = Label(self.main_frame, text="Search", bg="#F1F0F0", fg="#1E1E1E", font=("Arial", 11, "bold"))
        search_lbl.place(x=400, y=82)

        self.entry = Entry(self.main_frame, width=25, font=("Arial", 12))
        self.entry.place(x=470, y=83)
        self.entry.bind("<Return>", self.search_bind)

        refresh_btn = Button(self.main_frame, text="⟳ Refresh", command=self.refresh_table, bg="#2ECC71", fg="white",
                             relief=FLAT, activebackground="#48C9B0", font=("Arial", 9))
        refresh_btn.place(x=770, y=80)

    def setup_treeview(self):
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
            self.main_frame,
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

        self.table.place(x=20, y=150, width=1180, height=500)

        self.scroll = Scrollbar(self.main_frame, orient="vertical", command=self.table.yview)
        self.table.configure(yscrollcommand=self.scroll.set)
        self.scroll.place(x=1200, y=150, height=500)

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
        self.add_win_popup.config(bg="#1E1E1E")

        content_frame = Frame(self.add_win_popup,bg="White")
        content_frame.place(x=50, y=70,width=400,height=350)

        heading1 = Label(self.add_win_popup, text="Add new product",bg="#1E1E1E",fg="White",font=("Georgia",20,"bold"))
        heading1.place(x=130,y=20)

        lbl1 = Label(content_frame, text="Enter product ID",bg="White",fg="Black",font=("Arial",10))
        lbl1.place(x=20,y=20)
        lbl3 = Label(content_frame, text="Enter product name",bg="White",fg="Black",font=("Arial",10))
        lbl3.place(x=20,y=60)
        lbl4 = Label(content_frame, text="Enter catagory",bg="White",fg="Black",font=("Arial",10))
        lbl4.place(x=20,y=100)
        lbl5 = Label(content_frame, text="Enter supplier",bg="White",fg="Black",font=("Arial",10))
        lbl5.place(x=20,y=140)
        lbl6 = Label(content_frame, text="Enter price",bg="White",fg="Black",font=("Arial",10))
        lbl6.place(x=20,y=180)
        lbl7 = Label(content_frame, text="Enter quantity",bg="White",fg="Black",font=("Arial",10))
        lbl7.place(x=20, y=220)

        self.entry2 = Entry(content_frame,width=18,font=("Arial",13),bg="#FEFAEA",fg="Black")
        self.entry2.place(x=210,y=20)
        self.entry3 = Entry(content_frame,width=18,font=("Arial",13),bg="#FEFAEA",fg="Black")
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

        self.entry7 = Entry(content_frame,width=18,font=("Arial",13),bg="#FEFAEA",fg="Black")
        self.entry7.place(x=210,y=180)
        self.entry8 = Entry(content_frame,width=18,font=("Arial",13),bg="#FEFAEA",fg="Black")
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


        save_but = Button(content_frame,text="Save",font=("Arial",8,"bold"),command=add_n_close,fg="White",bg="Green",relief=FLAT,width=10,height=2,activebackground="Green",activeforeground="White")
        save_but.place(x=150,y=270)

    def open_update_win(self):
        self.update_window()

    def update_window(self):
        self.update_win_popup = Toplevel()
        self.update_win_popup.geometry("500x500")
        self.update_win_popup.config(bg="#1E1E1E")

        content_frame = Frame(self.update_win_popup,bg="White")
        content_frame.place(x=50, y=100,width=400,height=350)

        prdct_id = Label(self.update_win_popup, text="Enter Product ID",bg="#1E1E1E",fg="White",font=("Arial",10))
        prdct_id.place(x=20,y=20)

        self.entry8 = Entry(self.update_win_popup,width=25,font=("Arial",13))
        self.entry8.place(x=130,y=20)

        lbl1 = Label(content_frame, text="Enter new product ID",bg="White",fg="Black",font=("Arial",10))
        lbl1.place(x=20,y=20)

        lbl3 = Label(content_frame, text="Enter new product name",bg="White",fg="Black",font=("Arial",10))
        lbl3.place(x=20,y=60)

        lbl4 = Label(content_frame, text="Enter new catagory",bg="White",fg="Black",font=("Arial",10))
        lbl4.place(x=20,y=100)

        lbl5 = Label(content_frame, text="Enter new supplier",bg="White",fg="Black",font=("Arial",10))
        lbl5.place(x=20,y=140)

        lbl6 = Label(content_frame, text="Enter new price",bg="White",fg="Black",font=("Arial",10))
        lbl6.place(x=20,y=180)

        lbl7 = Label(content_frame, text="Enter new quantity",bg="White",fg="Black",font=("Arial",10))
        lbl7.place(x=20, y=220)

        self.entry9 = Entry(content_frame,width=18,font=("Arial",13),bg="#FEFAEA",fg="Black")
        self.entry9.place(x=210,y=20)

        self.entry10 = Entry(content_frame,width=18,font=("Arial",13),bg="#FEFAEA",fg="Black")
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

        self.entry11 = Entry(content_frame,width=18,font=("Arial",13),bg="#FEFAEA",fg="Black")
        self.entry11.place(x=210,y=180)
        self.entry12 = Entry(content_frame,width=18,font=("Arial",13),bg="#FEFAEA",fg="Black")
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
            
        Button(self.update_win_popup, text="Search", command=search_id, font=("Arial",8,"bold"),
        fg="White", bg="#325789", width=10, height=1).place(x=390, y=20)
            
        save_but = Button(content_frame,text="Save",font=("Arial",8,"bold"),fg="White",bg="Green",command=update_n_close,relief=FLAT,width=10,height=2,activebackground="Green",activeforeground="White")
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

from tkinter import *
from tkinter import ttk
import mysql.connector
from tkinter import messagebox
import re

class Suppliermanager:
    def __init__(self,root):

        self.dbcon = mysql.connector.connect(
            host="localhost",
            user="root",
            password="root",
            database="Inventory_manager_db"
        )

        self.root = root
        self.create_window()
        self.setup_treeview()

    def create_window(self):
        self.suppliers_window = Toplevel()
        self.suppliers_window.title("Desktop Inventory Management System")
        self.suppliers_window.geometry("1920x1080")
        self.suppliers_window.config(bg="#1E1E1E")

        heading = Label(self.suppliers_window, text="Suppliers", bg="#1E1E1E", fg="White", font=("Georgia",50,"bold"))
        heading.place(x=750, y=10)

        self.content_frame = Frame(self.suppliers_window,bg="#F1F0F0")
        self.content_frame.place(x=50, y=100, width=1800, height=900)

        sub_heading = Label(self.content_frame, text="Welcome, Admin!", bg="#F1F0F0", fg="#1E1E1E", font=("TkDefaultFont",30,"bold"))
        sub_heading.place(x=20, y=10)

        underline = Frame(self.content_frame, bg="#1E1E1E", height=4, width=1800)
        underline.place(x=0,y=70)

        add_sup = Button(self.content_frame, text="Add Supplier",command=self.open_add_win,relief=FLAT, bg="#3962A3", fg="White",activebackground="#3962A3",activeforeground="White",font=("Arial",10))
        add_sup.place(x=30, y=100)
        updte_sup = Button(self.content_frame,command=self.open_update_win, text="Update Supplier",relief=FLAT, bg="#359E0B", fg="White",activebackground="#359E0B",activeforeground="White",font=("Arial",10))
        updte_sup.place(x=135, y=100)
        del_sup = Button(self.content_frame, text="Delete Supplier",command=self.delete_sup,relief=FLAT, bg="#F42325", fg="White",activebackground="#F42325",activeforeground="White",font=("Arial",10))
        del_sup.place(x=270, y=100)

        search_sup = Label(self.content_frame,text="Search", bg="#F1F0F0",fg="#1E1E1E",font=("Arial",13,"bold"))
        search_sup.place(x=400, y=102)

        def refresh_table():
            self.load_suppliers()

        refresh_btn = Button(self.content_frame, text="⟳ Refresh",command=refresh_table, bg="#2ECC71", fg="white", relief=FLAT,activebackground="#48C9B0", font=("Arial", 10))
        refresh_btn.place(x=770,y=100)

        self.entry = Entry(self.content_frame,width=25,font=("Arial",13))
        self.entry.bind("<Return>",self.search_bind)
        self.entry.place(x=470,y=103)

        self.suppliers_window.protocol("WM_DELETE_WINDOW",self.on_close)

    def setup_treeview(self):

        style = ttk.Style()
        style.theme_use("default")

        style.configure("Treeview",
                        background="White",
                        foreground="Black",
                        fieldbackground="White",
                        rowheight=30)

        style.configure("Treeview.Heading",
                        background="#548DCF",
                        foreground="White",
                        font=("Arial",12,"bold"),
                        height=10)

        self.table = ttk.Treeview(self.content_frame, columns=("supplier_id", "name", "contact_info"), show="headings")
        self.table.heading("supplier_id", text="Supplier ID")
        self.table.heading("name", text="Supplier Name")
        self.table.heading("contact_info", text="Contact Info")
        self.table.column("supplier_id", width=200, anchor="w")
        self.table.column("name", width=400, anchor="w")
        self.table.column("contact_info", width=600, anchor="w")
        self.table.place(x=20, y=150, width=1750, height=700)

        self.scrollbar = Scrollbar(self.content_frame, orient="vertical", command=self.table.yview)
        self.table.configure(yscrollcommand=self.scrollbar.set)
        self.scrollbar.place(x=1770, y=150, height=700)


        self.load_suppliers()

    def load_suppliers(self):
        cursor = self.dbcon.cursor()
        cursor.execute("select * from suppliers")
        rows = cursor.fetchall()

        for item in self.table.get_children():
            self.table.delete(item)

        for row in rows:
            self.table.insert("","end",values=row)

    def open_add_win(self):
        self.add_window()

    def add_window(self):
        add_win_popup = Toplevel()
        add_win_popup.geometry("500x500")
        add_win_popup.config(bg="#1E1E1E")

        content_frame = Frame(add_win_popup,bg="White")
        content_frame.place(x=50, y=70,width=400,height=350)

        heading1 = Label(add_win_popup, text="Add new supplier",bg="#1E1E1E",fg="White",font=("Georgia",20,"bold"))
        heading1.place(x=130,y=20)


        lbl1 = Label(content_frame, text="Enter supplier ID",bg="White",fg="Black",font=("Arial",10))
        lbl1.place(x=20,y=20)
        lbl3 = Label(content_frame, text="Enter supplier name",bg="White",fg="Black",font=("Arial",10))
        lbl3.place(x=20,y=60)
        lbl4 = Label(content_frame, text="Enter Contact_info",bg="White",fg="Black",font=("Arial",10))
        lbl4.place(x=20,y=100)
 
        self.entry2 = Entry(content_frame,width=18,font=("Arial",13),bg="#FEFAEA",fg="Black")
        self.entry2.place(x=210,y=20)
        self.entry3 = Entry(content_frame,width=18,font=("Arial",13),bg="#FEFAEA",fg="Black")
        self.entry3.place(x=210,y=60)
        self.entry4 = Entry(content_frame,width=18,font=("Arial",13),bg="#FEFAEA",fg="Black")
        self.entry4.place(x=210,y=100)

        def add_n_close():
            sup_id = self.entry2.get().strip()
            sup_name = self.entry3.get().strip()
            sup_info = self.entry4.get().strip()

            email_pat = r'^[\w\.-]+@[\w\.-]+\.\w+$'

            phone_pat = r'^\d{10}$'

            if not sup_id or not sup_name or not sup_info:
                messagebox.showwarning("Warning","Please don't leave any spaces behind.",parent=add_win_popup)
                return
        
            if sup_id.isalpha():
                messagebox.showwarning("Warning","Please enter only numerical values for supplier ID.",parent=add_win_popup)
                return
        
            if sup_name.isdigit():
                messagebox.showwarning("Warning","Please enter only letters for supplier name.",parent=add_win_popup)
                return
        
            if not (re.match(email_pat,sup_info) or re.match(phone_pat,sup_info)):
                messagebox.showwarning("Warning","Please enter valid contact method. (Email/Phone)",parent=add_win_popup)
                return
            
            cursor = self.dbcon.cursor()

            try:
                cursor.execute("insert into suppliers(supplier_id,name,contact_info) values(%s,%s,%s)",(sup_id,sup_name,sup_info))
                self.dbcon.commit()

            except mysql.connector.IntegrityError:
                messagebox.showerror("Duplicate","Data you entered already exists please try again.",parent=add_win_popup)
                return
        
            except mysql.connector.Error as err:
                connection_err = messagebox.showerror("Databse Error",str(err),parent=add_win_popup)
                return
        
            finally:
                cursor.close()

            messagebox.showinfo("Success","Data added successfully!",parent=add_win_popup)
            self.load_suppliers()
            add_win_popup.destroy()

        save_but = Button(content_frame,text="Save",command=add_n_close,font=("Arial",8,"bold"),fg="White",bg="Green",relief=FLAT,width=10,height=2,activebackground="Green",activeforeground="White")
        save_but.place(x=150,y=200)
        
    def open_update_win(self):
        self.update_window()

    def update_window(self):
        update_win_popup = Toplevel()
        update_win_popup.geometry("500x500")
        update_win_popup.config(bg="#1E1E1E")

        content_frame = Frame(update_win_popup,bg="White")
        content_frame.place(x=50, y=100,width=400,height=350)

        prdct_id = Label(update_win_popup, text="Enter Supplier ID",bg="#1E1E1E",fg="White",font=("Arial",10))
        prdct_id.place(x=20,y=20)
        self.entry5 = Entry(update_win_popup,width=25,font=("Arial",13))
        self.entry5.place(x=130,y=20)

        lbl1 = Label(content_frame, text="Enter new supplier ID",bg="White",fg="Black",font=("Arial",10))
        lbl1.place(x=20,y=20)
        lbl3 = Label(content_frame, text="Enter new supplier name",bg="White",fg="Black",font=("Arial",10))
        lbl3.place(x=20,y=60)
        lbl4 = Label(content_frame, text="Enter new contact info", bg="White", fg="Black",font=("Arial",10))
        lbl4.place(x=20,y=100)

        self.entry6 = Entry(content_frame,width=18,font=("Arial",13),bg="#FEFAEA",fg="Black")
        self.entry6.place(x=210,y=20)
        self.entry7 = Entry(content_frame,width=18,font=("Arial",13),bg="#FEFAEA",fg="Black")
        self.entry7.place(x=210,y=60)
        self.entry8 = Entry(content_frame,width=18,font=("Arial",13),bg="#FEFAEA",fg="Black")
        self.entry8.place(x=210,y=100)

        def check_id():
            sup_id = self.entry5.get().strip()

            if not sup_id:
                messagebox.showwarning("Warning","Please don't leave spaces behind.",parent=update_win_popup)
                return
            
            if not sup_id.isdigit():
                messagebox.showwarning("Warning","Supplier ID must be numerical.",parent=update_win_popup)
                return
            
            cursor = self.dbcon.cursor()
            cursor.execute("select * from suppliers where supplier_id = %s",(sup_id,))
            result = cursor.fetchone()
            cursor.close()
            
            if result:
                messagebox.showinfo("Found",f"Supplier ID {sup_id} exists in the database.\nYou may continue.",parent=update_win_popup)
                return
                
            else:
                messagebox.showerror("Not Found",f"Supplier ID {sup_id} does not exist in the database.",parent=update_win_popup)
                return
                
        def update_n_close():
            old_sup_id = self.entry5.get().strip()
            new_sup_id = self.entry6.get().strip()
            new_name = self.entry7.get().strip()
            new_cntct = self.entry8.get().strip()

            if not (old_sup_id and new_sup_id and new_name and new_cntct):
                messagebox.showwarning("Warning","Please don't leave empty spaces behind.",parent=update_win_popup)
                return
            
            if not old_sup_id.isdigit():
                messagebox.showwarning("Warning","Supplier ID must be numerical.",parent=update_win_popup)
                return
            
            if not new_sup_id.isdigit():
                messagebox.showwarning("Warning","New supplier ID also must be numerical.",parent=update_win_popup)
                return
            
            if new_name.isdigit():
                messagebox.showwarning("Warning","New supplier name cannot contain digits.",parent=update_win_popup)
                return
            
            phone_pat = r'^\d{10}$'
            email_pat = r'^[\w\.-]+@[\w\.-]+\.\w+$'

            if not (re.match(email_pat,new_cntct) or re.match(phone_pat,new_cntct)):
                messagebox.showwarning("Warning","Please enter valid contact method. (Email/Phone)",parent=update_win_popup)
                return
            
            cursor = self.dbcon.cursor()

            try:
                cursor.execute("update suppliers set supplier_id = %s, name = %s, contact_info = %s where supplier_id = %s",(new_sup_id,new_name,new_cntct,old_sup_id))
                self.dbcon.commit()

            except mysql.connector.IntegrityError:
                messagebox.showerror("Error","Duplicate Category ID.",parent=update_win_popup)
                return
            
            except mysql.connector.Error as err:
                messagebox.showerror("Database Error",str(err),parent=update_win_popup)
                return
            
            finally:
                cursor.close()

            messagebox.showinfo("Success","Supplier updated successfully!",parent=update_win_popup)
            self.load_suppliers()
            update_win_popup.destroy()


        Button(update_win_popup, text="Search", command=check_id, font=("Arial",8,"bold"),
               fg="White", bg="#325789", width=10, height=1).place(x=390, y=20)
            
        save_but = Button(content_frame,text="Save",command=update_n_close,font=("Arial",8,"bold"),fg="White",bg="Green",relief=FLAT,width=10,height=2,activebackground="Green",activeforeground="White")
        save_but.place(x=150,y=200)

    def delete_sup(self):
        selected_items = self.table.selection()

        if not selected_items:
            messagebox.showwarning("Error","No item(s) selected.",parent=self.suppliers_window)
            return
        
        confirmation = messagebox.askyesno("Confirmation","Do you confirm to delete the selected item(s)?",parent=self.suppliers_window)

        if not confirmation:
            return
        
        cursor = self.dbcon.cursor()

        for item in selected_items:
            values = self.table.item(item,"values")
            sup_id = values[0]

            cursor.execute("delete from suppliers where supplier_id = %s",(sup_id,))
            self.table.delete(item)

        self.dbcon.commit()
        cursor.close()
        self.load_suppliers()
        messagebox.showinfo("Deleted","Deletion successful.",parent=self.suppliers_window)

    def search_sup(self):
        search_val = self.entry.get().strip()

        if not search_val:
            messagebox.showwarning("Warning","Input required in the entry.",parent=self.suppliers_window)
            return
        
        cursor = self.dbcon.cursor()

        like_val = f"%{search_val}%"

        cursor.execute("select * from suppliers where supplier_id like %s or name like %s or contact_info like %s",(like_val,like_val,like_val))
        result = cursor.fetchall()
        cursor.close()

        if result:
            for item in self.table.get_children():
                self.table.delete(item)
                
            for row in result:
                self.table.insert("","end",values=row)

        else:
            messagebox.showerror("No Match","No matching results have been found.",parent=self.suppliers_window)
            return
        
    def search_bind(self,event):
        self.search_sup()

    def close_connection(self):
        if self.dbcon.is_connected():
            self.dbcon.close()

    def on_close(self):
        self.close_connection()
        self.suppliers_window.destroy()



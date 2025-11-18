from tkinter import *
from tkinter import ttk
import mysql.connector
from tkinter import messagebox
import re

class Suppliermanager:
    def __init__(self, root):
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
        self.suppliers_window.geometry("1300x800")  # 🔹 Resized window
        self.suppliers_window.config(bg="#111828")

        heading = Label(self.suppliers_window, text="Suppliers",
                        bg="#111828", fg="#F3F4F6",
                        font=("Segoe UI", 42, "bold"))
        heading.place(x=500, y=3)

        self.content_frame = Frame(self.suppliers_window, bg="#0B1220")
        self.content_frame.place(x=30, y=80, width=1240, height=670)

        sub_heading = Label(self.content_frame, text="Welcome, Admin!",
                            bg="#0B1220", fg="#8A95B8",
                            font=("Segoe UI", 24, "bold"))
        sub_heading.place(x=20, y=7)

        underline = Frame(self.content_frame, bg="#2ED3B7", height=3, width=1240)
        underline.place(x=0, y=55)

        self.panel_frame = Frame(self.content_frame, bg="#151F32")
        self.panel_frame.place(x=0, y=80, width=1240, height=590)

        panel_heading = Label(self.panel_frame, text="Supplier Directory", bg="#151F32", fg="#F3F4F6",
                              font=("Segoe UI", 19, "bold"))
        panel_heading.place(x=20, y=0)

        controls_frame = Frame(self.panel_frame, bg="#151F32")
        controls_frame.place(x=20, y=40, width=1200, height=60)

        actions_wrapper = Frame(controls_frame, bg="#151F32")
        actions_wrapper.pack(side=LEFT)

        add_sup = Button(actions_wrapper, text="Add Supplier",
                         command=self.open_add_win, relief=FLAT,
                         bg="#2ED3B7", fg="#0B1220",
                         activebackground="#31E3BF",
                         activeforeground="#0B1220",
                         font=("Segoe UI", 10, "bold"), width=14)
        add_sup.pack(side=LEFT, padx=5)

        updte_sup = Button(actions_wrapper, text="Update Supplier",
                           command=self.open_update_win, relief=FLAT,
                           bg="#1C2A43", fg="#F3F4F6",
                           activebackground="#223555",
                           activeforeground="#2ED3B7",
                           font=("Segoe UI", 10, "bold"), width=14)
        updte_sup.pack(side=LEFT, padx=5)

        del_sup = Button(actions_wrapper, text="Delete Supplier",
                         command=self.delete_sup, relief=FLAT,
                         bg="#F472B6", fg="#0B1220",
                         activebackground="#F688C5",
                         activeforeground="#0B1220",
                         font=("Segoe UI", 10, "bold"), width=14)
        del_sup.pack(side=LEFT, padx=5)

        search_wrapper = Frame(controls_frame, bg="#151F32")
        search_wrapper.pack(side=RIGHT)

        refresh_btn = Button(search_wrapper, text="⟳ Refresh",
                             command=self.load_suppliers,
                             bg="#0B1220", fg="#2ED3B7",
                             relief=FLAT, activebackground="#1C2A43",
                             activeforeground="#31E3BF",
                             font=("Segoe UI", 10, "bold"), width=12)
        refresh_btn.pack(side=RIGHT, padx=(10, 0))

        self.entry = Entry(search_wrapper, width=28, font=("Segoe UI", 12),
                           bg="#0B1220", fg="#F3F4F6",
                           insertbackground="#2ED3B7",
                           highlightbackground="#2ED3B7",
                           highlightcolor="#2ED3B7",
                           relief=FLAT)
        self.entry.bind("<Return>", self.search_bind)
        self.entry.pack(side=RIGHT, padx=5)

        search_sup = Label(search_wrapper, text="Search",
                           bg="#151F32", fg="#F3F4F6",
                           font=("Segoe UI", 12, "bold"))
        search_sup.pack(side=RIGHT, padx=5)

        self.suppliers_window.protocol("WM_DELETE_WINDOW", self.on_close)

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

        table_container = Frame(self.panel_frame, bg="#151F32")
        table_container.place(x=20, y=120, width=1200, height=450)

        self.table = ttk.Treeview(table_container,
                                  columns=("supplier_id", "name", "contact_info"),
                                  show="headings")

        self.table.heading("supplier_id", text="Supplier ID")
        self.table.heading("name", text="Supplier Name")
        self.table.heading("contact_info", text="Contact Info")

        self.table.column("supplier_id", width=150, anchor="center")
        self.table.column("name", width=300, anchor="w")
        self.table.column("contact_info", width=500, anchor="w")

        self.table.place(x=0, y=0, width=1150, height=450)

        self.scrollbar = Scrollbar(table_container, orient="vertical", command=self.table.yview,
                                   bg="#151F32", troughcolor="#0B1220", bd=0, highlightthickness=0)
        self.table.configure(yscrollcommand=self.scrollbar.set)
        self.scrollbar.place(x=1150, y=0, height=450)

        self.load_suppliers()

    def load_suppliers(self):
        cursor = self.dbcon.cursor()
        cursor.execute("select * from suppliers")
        rows = cursor.fetchall()
        cursor.close()

        for item in self.table.get_children():
            self.table.delete(item)

        for row in rows:
            self.table.insert("", "end", values=row)

    def open_add_win(self):
        self.add_window()

    def add_window(self):
        add_win_popup = Toplevel()
        add_win_popup.geometry("500x500")
        add_win_popup.config(bg="#111828")

        content_frame = Frame(add_win_popup,bg="#0B1220")
        content_frame.place(x=50, y=70,width=400,height=350)

        heading1 = Label(add_win_popup, text="Add new supplier",bg="#111828",fg="#F3F4F6",font=("Segoe UI",20,"bold"))
        heading1.place(x=130,y=20)


        lbl1 = Label(content_frame, text="Enter supplier ID",bg="#0B1220",fg="#F3F4F6",font=("Segoe UI",11))
        lbl1.place(x=20,y=20)
        lbl3 = Label(content_frame, text="Enter supplier name",bg="#0B1220",fg="#F3F4F6",font=("Segoe UI",11))
        lbl3.place(x=20,y=60)
        lbl4 = Label(content_frame, text="Enter Contact_info",bg="#0B1220",fg="#F3F4F6",font=("Segoe UI",11))
        lbl4.place(x=20,y=100)
 
        common_entry = dict(width=18,font=("Segoe UI",13),bg="#151F32",fg="#F3F4F6",
                            insertbackground="#2ED3B7",highlightbackground="#2ED3B7",
                            highlightcolor="#2ED3B7",relief=FLAT)

        self.entry2 = Entry(content_frame,**common_entry)
        self.entry2.place(x=210,y=20)
        self.entry3 = Entry(content_frame,**common_entry)
        self.entry3.place(x=210,y=60)
        self.entry4 = Entry(content_frame,**common_entry)
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

        save_but = Button(content_frame,text="Save",command=add_n_close,font=("Segoe UI",10,"bold"),fg="#0B1220",bg="#2ED3B7",relief=FLAT,width=12,height=2,activebackground="#31E3BF",activeforeground="#0B1220")
        save_but.place(x=150,y=200)
        
    def open_update_win(self):
        self.update_window()

    def update_window(self):
        update_win_popup = Toplevel()
        update_win_popup.geometry("500x500")
        update_win_popup.config(bg="#111828")

        content_frame = Frame(update_win_popup,bg="#0B1220")
        content_frame.place(x=50, y=100,width=400,height=350)

        prdct_id = Label(update_win_popup, text="Enter Supplier ID",bg="#111828",fg="#F3F4F6",font=("Segoe UI",11,"bold"))
        prdct_id.place(x=20,y=20)
        self.entry5 = Entry(update_win_popup,width=25,font=("Segoe UI",13),bg="#151F32",fg="#F3F4F6",
                            insertbackground="#2ED3B7",highlightbackground="#2ED3B7",highlightcolor="#2ED3B7",
                            relief=FLAT)
        self.entry5.place(x=130,y=20)

        lbl1 = Label(content_frame, text="Enter new supplier ID",bg="#0B1220",fg="#F3F4F6",font=("Segoe UI",11))
        lbl1.place(x=20,y=20)
        lbl3 = Label(content_frame, text="Enter new supplier name",bg="#0B1220",fg="#F3F4F6",font=("Segoe UI",11))
        lbl3.place(x=20,y=60)
        lbl4 = Label(content_frame, text="Enter new contact info", bg="#0B1220", fg="#F3F4F6",font=("Segoe UI",11))
        lbl4.place(x=20,y=100)

        entry_args = dict(width=18,font=("Segoe UI",13),bg="#151F32",fg="#F3F4F6",
                          insertbackground="#2ED3B7",highlightbackground="#2ED3B7",
                          highlightcolor="#2ED3B7",relief=FLAT)

        self.entry6 = Entry(content_frame,**entry_args)
        self.entry6.place(x=210,y=20)
        self.entry7 = Entry(content_frame,**entry_args)
        self.entry7.place(x=210,y=60)
        self.entry8 = Entry(content_frame,**entry_args)
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


        Button(update_win_popup, text="Search", command=check_id, font=("Segoe UI",9,"bold"),
               fg="#0B1220", bg="#2ED3B7", activebackground="#31E3BF",
               activeforeground="#0B1220", width=10, height=1).place(x=390, y=20)
            
        save_but = Button(content_frame,text="Save",command=update_n_close,font=("Segoe UI",10,"bold"),fg="#0B1220",bg="#2ED3B7",relief=FLAT,width=12,height=2,activebackground="#31E3BF",activeforeground="#0B1220")
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



from tkinter import *
from tkinter import ttk
import mysql.connector
from tkinter import messagebox

class CatagoryManager:
    def __init__(self, root):
        self.dbcon = mysql.connector.connect(
            host="localhost",
            user="root",
            password="root",
            database="Inventory_manager_db"
        )
        self.root = root
        self.create_window()
        self.set_up_treeview()

    def create_window(self):
        self.catagory_window = Toplevel(self.root)
        self.catagory_window.title("Desktop Inventory Management System")
        self.catagory_window.geometry("1300x800")  # 🔹 Standard window size
        self.catagory_window.config(bg="#111828")

        heading = Label(self.catagory_window, text="Categories",
                        bg="#111828", fg="#F3F4F6",
                        font=("Segoe UI", 42, "bold"))
        heading.place(x=500, y=10)

        self.create_main_frame()

    def create_main_frame(self):
        self.content_frame = Frame(self.catagory_window, bg="#0B1220")
        self.content_frame.place(x=30, y=80, width=1240, height=670)

        sub_heading = Label(self.content_frame, text="Welcome, Admin!",
                            bg="#0B1220", fg="#8A95B8",
                            font=("Segoe UI", 24, "bold"))
        sub_heading.place(x=20, y=10)

        underline = Frame(self.content_frame, bg="#2ED3B7", height=3, width=1240)
        underline.place(x=0, y=55)

        self.panel_frame = Frame(self.content_frame, bg="#151F32")
        self.panel_frame.place(x=0, y=80, width=1240, height=590)

        panel_heading = Label(self.panel_frame, text="Manage Categories", bg="#151F32", fg="#F3F4F6",
                              font=("Segoe UI", 22, "bold"))
        panel_heading.place(x=20, y=0)

        controls_frame = Frame(self.panel_frame, bg="#151F32")
        controls_frame.place(x=20, y=40, width=1200, height=60)

        actions_wrapper = Frame(controls_frame, bg="#151F32")
        actions_wrapper.pack(side=LEFT)

        add_cat = Button(actions_wrapper, text="Add Category",
                         command=self.open_add_win, relief=FLAT,
                         bg="#2ED3B7", fg="#0B1220",
                         activebackground="#31E3BF",
                         activeforeground="#0B1220",
                         font=("Segoe UI", 10, "bold"), width=14)
        add_cat.pack(side=LEFT, padx=5)

        update_cat = Button(actions_wrapper, text="Update Category",
                            command=self.open_update_win, relief=FLAT,
                            bg="#1C2A43", fg="#F3F4F6",
                            activebackground="#223555",
                            activeforeground="#2ED3B7",
                            font=("Segoe UI", 10, "bold"), width=14)
        update_cat.pack(side=LEFT, padx=5)

        del_cat = Button(actions_wrapper, text="Delete Category",
                         command=self.delete_items, relief=FLAT,
                         bg="#F472B6", fg="#0B1220",
                         activebackground="#F688C5",
                         activeforeground="#0B1220",
                         font=("Segoe UI", 10, "bold"), width=14)
        del_cat.pack(side=LEFT, padx=5)

        search_wrapper = Frame(controls_frame, bg="#151F32")
        search_wrapper.pack(side=RIGHT)

        refresh_btn = Button(search_wrapper, text="⟳ Refresh",
                             command=self.load_catagories,
                             bg="#0B1220", fg="#2ED3B7",
                             relief=FLAT, activebackground="#1C2A43",
                             activeforeground="#31E3BF",
                             font=("Segoe UI", 10, "bold"), width=12)
        refresh_btn.pack(side=RIGHT, padx=(10, 0))

        self.search_entry = Entry(search_wrapper, width=28, font=("Segoe UI", 12),
                                  bg="#0B1220", fg="#F3F4F6", insertbackground="#2ED3B7",
                                  highlightbackground="#2ED3B7", highlightcolor="#2ED3B7",
                                  relief=FLAT)
        self.search_entry.bind("<Return>", self.search_cat_event)
        self.search_entry.pack(side=RIGHT, padx=5)

        search_cat = Label(search_wrapper, text="Search",
                           bg="#151F32", fg="#F3F4F6",
                           font=("Segoe UI", 12, "bold"))
        search_cat.pack(side=RIGHT, padx=5)

        self.catagory_window.protocol("WM_DELETE_WINDOW", self.on_close)

    def set_up_treeview(self):
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
                                  columns=("catagory_id", "catagory_name"),
                                  show="headings")

        self.table.heading("catagory_id", text="Category ID")
        self.table.heading("catagory_name", text="Category Name")

        self.table.column("catagory_id", width=250, anchor="center")
        self.table.column("catagory_name", width=500, anchor="w")

        self.table.place(x=0, y=0, width=1150, height=450)

        self.scrollbar = Scrollbar(table_container, orient="vertical", command=self.table.yview,
                                   bg="#151F32", troughcolor="#0B1220", bd=0, highlightthickness=0)
        self.table.configure(yscrollcommand=self.scrollbar.set)
        self.scrollbar.place(x=1150, y=0, height=450)

        self.load_catagories()

    def load_catagories(self):
        cursor = self.dbcon.cursor()
        cursor.execute("SELECT * FROM catagories")
        rows = cursor.fetchall()
        cursor.close()

        for item in self.table.get_children():
            self.table.delete(item)
        for row in rows:
            self.table.insert("", "end", values=row)

    def open_add_win(self):
        self.add_window()

    def open_update_win(self):
        self.update_window()

    def add_window(self):
        add_win_popup = Toplevel(self.catagory_window)
        add_win_popup.geometry("500x500")
        add_win_popup.config(bg="#111828")

        content_frame = Frame(add_win_popup,bg="#0B1220")
        content_frame.place(x=50, y=70,width=400,height=350)

        heading1 = Label(add_win_popup, text="Add new catagory",bg="#111828",fg="#F3F4F6",font=("Segoe UI",20,"bold"))
        heading1.place(x=130,y=20)


        lbl1 = Label(content_frame, text="Enter catagory ID",bg="#0B1220",fg="#F3F4F6",font=("Segoe UI",11))
        lbl1.place(x=20,y=20)
        lbl3 = Label(content_frame, text="Enter catagory name",bg="#0B1220",fg="#F3F4F6",font=("Segoe UI",11))
        lbl3.place(x=20,y=60)
  
 
        self.entry2 = Entry(content_frame,width=18,font=("Segoe UI",13),bg="#151F32",fg="#F3F4F6",
                             insertbackground="#2ED3B7",highlightbackground="#2ED3B7", highlightcolor="#2ED3B7",
                             relief=FLAT)
        self.entry2.place(x=210,y=20)
        self.entry3 = Entry(content_frame,width=18,font=("Segoe UI",13),bg="#151F32",fg="#F3F4F6",
                             insertbackground="#2ED3B7",highlightbackground="#2ED3B7", highlightcolor="#2ED3B7",
                             relief=FLAT)
        self.entry3.place(x=210,y=60)

        def add_data_savenclose():
            cat_id = self.entry2.get().strip()
            cat_name = self.entry3.get().strip()

            if not cat_id or not cat_name:
                no_input_msg = messagebox.showwarning("Warning","Please don't leave empty spaces behind.",parent=add_win_popup)
                return
            
            if not cat_id.isdigit():
                cat_id_wrong = messagebox.showwarning("Warning","Please enter only numerical values for catagory ID.",parent=add_win_popup)
                return
            
            if cat_name.isdigit():
                cat_name_wrong = messagebox.showwarning("Warning","Please enter only letters for catagory name.",parent=add_win_popup)
                return
            
            cursor = self.dbcon.cursor()

            try:
                cursor.execute("insert into catagories(catagory_id,catagory_name) values(%s,%s)",(cat_id,cat_name))
                self.dbcon.commit()

            except mysql.connector.IntegrityError:
                duplicate_err = messagebox.showerror("Error","Duplicate data.The values already exists in the database.",parent=add_win_popup)
                return
        
            except mysql.connector.Error as err:
                connection_err = messagebox.showerror("Databse Error",str(err),parent=add_win_popup)
                return
        
            finally:
                cursor.close()
            
            success = messagebox.showinfo("Success","Data added into the database successfully!",parent=add_win_popup)
            self.load_catagories()
            add_win_popup.destroy()

        save_but = Button(content_frame,text="Save",command=add_data_savenclose,font=("Segoe UI",10,"bold"),
                          fg="#0B1220",bg="#2ED3B7",relief=FLAT,width=12,height=2,
                          activebackground="#31E3BF",activeforeground="#0B1220")
        save_but.place(x=150,y=150)

    def update_window(self):
        update_win_popup = Toplevel(self.catagory_window)
        update_win_popup.geometry("500x500")
        update_win_popup.config(bg="#111828")

        content_frame = Frame(update_win_popup,bg="#0B1220")
        content_frame.place(x=50, y=100,width=400,height=350)

        Label(update_win_popup, text="Enter catagory ID",bg="#111828",fg="#F3F4F6",font=("Segoe UI",11,"bold")).place(x=20,y=20)
        entry1 = Entry(update_win_popup,width=25,font=("Segoe UI",13),bg="#151F32",fg="#F3F4F6",
                       insertbackground="#2ED3B7",highlightbackground="#2ED3B7",highlightcolor="#2ED3B7",
                       relief=FLAT)
        entry1.place(x=130,y=20)

        Label(content_frame, text="Enter new catagory ID",bg="#0B1220",fg="#F3F4F6",font=("Segoe UI",11)).place(x=20,y=20)
        Label(content_frame, text="Enter new catagory name",bg="#0B1220",fg="#F3F4F6",font=("Segoe UI",11)).place(x=20,y=60)

        entry2 = Entry(content_frame,width=18,font=("Segoe UI",13),bg="#151F32",fg="#F3F4F6",
                       insertbackground="#2ED3B7",highlightbackground="#2ED3B7",highlightcolor="#2ED3B7",
                       relief=FLAT)
        entry2.place(x=210,y=20)
        entry3 = Entry(content_frame,width=18,font=("Segoe UI",13),bg="#151F32",fg="#F3F4F6",
                       insertbackground="#2ED3B7",highlightbackground="#2ED3B7",highlightcolor="#2ED3B7",
                       relief=FLAT)
        entry3.place(x=210,y=60)

        

        def search_cat_id():
            cat_id = entry1.get().strip()
            if not cat_id:
                messagebox.showwarning("Warning","Please enter a category ID.",parent=update_win_popup)
                return
            if not cat_id.isdigit():
                messagebox.showwarning("Warning","Category ID must be numerical.",parent=update_win_popup)
                return

            cursor = self.dbcon.cursor()
            cursor.execute("SELECT * FROM catagories WHERE catagory_id = %s", (cat_id,))
            result = cursor.fetchone()
            cursor.close()

            if result:
                messagebox.showinfo("Data Found", f"Category ID {cat_id} exists. You may update it.", parent=update_win_popup)
                return
            
            else:
                messagebox.showerror("Not Found", f"Category ID {cat_id} does not exist.", parent=update_win_popup)
                return

        def update_n_close():
            old_id = entry1.get().strip()
            new_id = entry2.get().strip()
            new_name = entry3.get().strip()

            if not old_id:
                messagebox.showwarning("Warning","Please fill the old category ID.",parent=update_win_popup)
                return
            if not new_id or not new_name:
                messagebox.showwarning("Warning","Please fill all fields.",parent=update_win_popup)
                return
            if not new_id.isdigit():
                messagebox.showwarning("Warning","New category ID must be numerical.",parent=update_win_popup)
                return
            if new_name.isdigit():
                messagebox.showwarning("Warning","Category name must contain only letters.",parent=update_win_popup)
                return

            cursor = self.dbcon.cursor()
            try:
                cursor.execute("UPDATE catagories SET catagory_id=%s, catagory_name=%s WHERE catagory_id=%s", (new_id,new_name,old_id))
                self.dbcon.commit()

            except mysql.connector.IntegrityError:
                messagebox.showerror("Error","Duplicate Category ID.",parent=update_win_popup)
                return
            
            except mysql.connector.Error as err:
                messagebox.showerror("Database Error",str(err),parent=update_win_popup)
                return
            
            finally:
                cursor.close()

            messagebox.showinfo("Success","Category updated successfully!",parent=update_win_popup)
            self.load_catagories()
            update_win_popup.destroy()

        Button(update_win_popup, text="Search", command=search_cat_id, font=("Segoe UI",9,"bold"),
               fg="#0B1220", bg="#2ED3B7", activebackground="#31E3BF",
               activeforeground="#0B1220", width=10, height=1).place(x=390, y=20)

        Button(content_frame, text="Update", command=update_n_close, font=("Segoe UI",10,"bold"),
               fg="#0B1220", bg="#2ED3B7", activebackground="#31E3BF",
               activeforeground="#0B1220", width=12, height=2, relief=FLAT).place(x=150, y=150)

    def delete_items(self):
        selected_items = self.table.selection()

        if not selected_items:
            messagebox.showerror("Error","No items selected.",parent=self.catagory_window)
            return
        
        confirm = messagebox.askyesno("Confirm","Do you want to delete the selected item(s)?",parent=self.catagory_window)

        if not confirm:
            return
        
        cursor = self.dbcon.cursor()

        for item in selected_items:
            values = self.table.item(item,"values")
            cat_id = values[0]

            cursor.execute("delete from catagories where catagory_id = %s",(cat_id,))
            self.table.delete(item)

        self.dbcon.commit()
        cursor.close()
        self.load_catagories()
        messagebox.showinfo("Deleted","Deletion successful.",parent=self.catagory_window)

    def search_cat_event(self, event):
        self.search()

    def search(self):
        search_val = self.search_entry.get().strip()

        if not search_val:
            messagebox.showwarning("Warning","Input required in the entry.",parent=self.catagory_window)
            return
        
        cursor = self.dbcon.cursor()

        like_val = f"%{search_val}%"

        cursor.execute("select * from catagories where catagory_id like %s or catagory_name like %s",(like_val,like_val))
        result = cursor.fetchall()
        cursor.close()

        if result:

            for item in self.table.get_children():
                self.table.delete(item)

            for row in result:
                self.table.insert("","end",values=row)

        else:
            messagebox.showerror("No Match","No matching results have been found.",parent=self.catagory_window)

    def close_connection(self):
        if self.dbcon.is_connected():
            self.dbcon.close()

    def on_close(self):
        self.close_connection()
        self.catagory_window.destroy()




        

    




   
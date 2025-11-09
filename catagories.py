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
        self.catagory_window.config(bg="#1E1E1E")

        heading = Label(self.catagory_window, text="Categories",
                        bg="#1E1E1E", fg="White",
                        font=("Georgia", 42, "bold"))
        heading.place(x=500, y=10)

        self.create_main_frame()

    def create_main_frame(self):
        self.content_frame = Frame(self.catagory_window, bg="#F1F0F0")
        self.content_frame.place(x=30, y=80, width=1240, height=670)

        sub_heading = Label(self.content_frame, text="Welcome, Admin!",
                            bg="#F1F0F0", fg="#1E1E1E",
                            font=("TkDefaultFont", 24, "bold"))
        sub_heading.place(x=20, y=10)

        underline = Frame(self.content_frame, bg="#1E1E1E", height=3, width=1240)
        underline.place(x=0, y=55)

        # 🔹 Buttons
        add_cat = Button(self.content_frame, text="Add Category",
                         command=self.open_add_win, relief=FLAT,
                         bg="#3962A3", fg="White",
                         activebackground="#3962A3",
                         activeforeground="White",
                         font=("Arial", 9))
        add_cat.place(x=30, y=80)

        update_cat = Button(self.content_frame, text="Update Category",
                            command=self.open_update_win, relief=FLAT,
                            bg="#359E0B", fg="White",
                            activebackground="#359E0B",
                            activeforeground="White",
                            font=("Arial", 9))
        update_cat.place(x=140, y=80)

        del_cat = Button(self.content_frame, text="Delete Category",
                         command=self.delete_items, relief=FLAT,
                         bg="#F42325", fg="White",
                         activebackground="#F42325",
                         activeforeground="White",
                         font=("Arial", 9))
        del_cat.place(x=270, y=80)

        search_cat = Label(self.content_frame, text="Search",
                           bg="#F1F0F0", fg="#1E1E1E",
                           font=("Arial", 11, "bold"))
        search_cat.place(x=400, y=82)

        self.search_entry = Entry(self.content_frame, width=25, font=("Arial", 12))
        self.search_entry.bind("<Return>", self.search_cat_event)
        self.search_entry.place(x=470, y=83)

        refresh_btn = Button(self.content_frame, text="⟳ Refresh",
                             command=self.load_catagories,
                             bg="#2ECC71", fg="white",
                             relief=FLAT, activebackground="#48C9B0",
                             font=("Arial", 9))
        refresh_btn.place(x=770, y=80)

        self.catagory_window.protocol("WM_DELETE_WINDOW", self.on_close)

    def set_up_treeview(self):
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
                                  columns=("catagory_id", "catagory_name"),
                                  show="headings")

        self.table.heading("catagory_id", text="Category ID")
        self.table.heading("catagory_name", text="Category Name")

        self.table.column("catagory_id", width=250, anchor="center")
        self.table.column("catagory_name", width=500, anchor="w")

        self.table.place(x=20, y=150, width=1180, height=480)

        self.scrollbar = Scrollbar(self.content_frame, orient="vertical", command=self.table.yview)
        self.table.configure(yscrollcommand=self.scrollbar.set)
        self.scrollbar.place(x=1200, y=150, height=480)

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
        add_win_popup.config(bg="#1E1E1E")

        content_frame = Frame(add_win_popup,bg="White")
        content_frame.place(x=50, y=70,width=400,height=350)

        heading1 = Label(add_win_popup, text="Add new catagory",bg="#1E1E1E",fg="White",font=("Georgia",20,"bold"))
        heading1.place(x=130,y=20)


        lbl1 = Label(content_frame, text="Enter catagory ID",bg="White",fg="Black",font=("Arial",10))
        lbl1.place(x=20,y=20)
        lbl3 = Label(content_frame, text="Enter catagory name",bg="White",fg="Black",font=("Arial",10))
        lbl3.place(x=20,y=60)
  
 
        self.entry2 = Entry(content_frame,width=18,font=("Arial",13),bg="#FEFAEA",fg="Black")
        self.entry2.place(x=210,y=20)
        self.entry3 = Entry(content_frame,width=18,font=("Arial",13),bg="#FEFAEA",fg="Black")
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

        save_but = Button(content_frame,text="Save",command=add_data_savenclose,font=("Arial",8,"bold"),fg="White",bg="Green",relief=FLAT,width=10,height=2,activebackground="Green",activeforeground="White")
        save_but.place(x=150,y=150)

    def update_window(self):
        update_win_popup = Toplevel(self.catagory_window)
        update_win_popup.geometry("500x500")
        update_win_popup.config(bg="#1E1E1E")

        content_frame = Frame(update_win_popup,bg="White")
        content_frame.place(x=50, y=100,width=400,height=350)

        Label(update_win_popup, text="Enter catagory ID",bg="#1E1E1E",fg="White",font=("Arial",10)).place(x=20,y=20)
        entry1 = Entry(update_win_popup,width=25,font=("Arial",13))
        entry1.place(x=130,y=20)

        Label(content_frame, text="Enter new catagory ID",bg="White",fg="Black",font=("Arial",10)).place(x=20,y=20)
        Label(content_frame, text="Enter new catagory name",bg="White",fg="Black",font=("Arial",10)).place(x=20,y=60)

        entry2 = Entry(content_frame,width=18,font=("Arial",13),bg="#FEFAEA",fg="Black")
        entry2.place(x=210,y=20)
        entry3 = Entry(content_frame,width=18,font=("Arial",13),bg="#FEFAEA",fg="Black")
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

        Button(update_win_popup, text="Search", command=search_cat_id, font=("Arial",8,"bold"),
               fg="White", bg="#325789", width=10, height=1).place(x=390, y=20)

        Button(content_frame, text="Update", command=update_n_close, font=("Arial",8,"bold"),
               fg="White", bg="Green", width=10, height=2).place(x=150, y=150)

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




        

    




   
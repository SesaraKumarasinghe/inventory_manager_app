from tkinter import *
from tkinter import ttk, messagebox
import mysql.connector

class Users:
    def __init__(self, root):
        self.root = root
        self.dbcon = mysql.connector.connect(
            host="localhost",
            user="root",
            password="root",
            database="Inventory_manager_db"
        )

        self.main_window()
        self.create_treeview()
        self.load_users()
        self.create_stats()

    def main_window(self):
        self.dashboard_window = Toplevel()
        self.dashboard_window.title("Desktop Inventory Management System")
        self.dashboard_window.geometry("1200x700")
        self.dashboard_window.config(bg="#111828")
        self.dashboard_window.protocol("WM_DELETE_WINDOW", self.on_close)

        heading = Label(self.dashboard_window, text="Users", bg="#111828", fg="#F3F4F6",
                        font=("Segoe UI", 40, "bold"))
        heading.place(x=460, y=5)

        main_frame = Frame(self.dashboard_window, bg="#0B1220")
        main_frame.place(x=30, y=100, width=1140, height=560)

        sub_heading = Label(main_frame, text="Welcome, Admin!", bg="#0B1220", fg="#8A95B8",
                            font=("Segoe UI", 26, "bold"))
        sub_heading.place(x=20, y=7)

        underline = Frame(main_frame, bg="#2ED3B7", height=3, width=1140)
        underline.place(x=0, y=60)

        self.content_frame = Frame(main_frame, bg="#151F32")
        self.content_frame.place(x=0, y=80, width=1140, height=500)

        add_btn = Button(self.content_frame, text="Add User", relief="flat", command=self.add_user,
                         bg="#2ED3B7", fg="#0B1220", font=("Segoe UI", 11, "bold"),
                         activebackground="#31E3BF", activeforeground="#0B1220")
        add_btn.place(x=30, y=30, width=120, height=35)

        update_btn = Button(self.content_frame, text="Update User", relief="flat", command=self.open_update_win,
                            bg="#1C2A43", fg="#F3F4F6", font=("Segoe UI", 11, "bold"),
                            activebackground="#223555", activeforeground="#2ED3B7")
        update_btn.place(x=170, y=30, width=150, height=35)

        delete_btn = Button(self.content_frame, text="Delete User", relief="flat", command=self.delete_user,
                            bg="#F472B6", fg="#0B1220", font=("Segoe UI", 11, "bold"),
                            activebackground="#F688C5", activeforeground="#0B1220")
        delete_btn.place(x=340, y=30, width=150, height=35)

        refresh_btn = Button(self.content_frame, text="⟳ Refresh", relief="flat", command=self.load_users,
                             bg="#151F32", fg="#2ED3B7", font=("Segoe UI", 11, "bold"),
                             activebackground="#1C2A43", activeforeground="#31E3BF")
        refresh_btn.place(x=510, y=30, width=100, height=35)

        # Search Entry
        search_lbl = Label(self.content_frame, text="Search", bg="#151F32", fg="#F3F4F6",
                           font=("Segoe UI", 13, "bold"))
        search_lbl.place(x=630, y=35)

        self.search_entry = Entry(self.content_frame, width=25, font=("Segoe UI", 13), bg="#0B1220",
                                  fg="#F3F4F6", insertbackground="#2ED3B7", relief="flat",
                                  highlightbackground="#2ED3B7", highlightcolor="#2ED3B7")
        self.search_entry.place(x=700, y=35, width=220, height=28)
        self.search_entry.bind("<Return>", self.search_bind)

        stats_lbl = Label(self.content_frame, text="Stats", bg="#151F32", fg="#F3F4F6",
                          font=("Segoe UI", 24, "bold"))
        stats_lbl.place(x=30, y=85)

        latest_lbl = Label(self.content_frame, text="Latest Transactions", bg="#151F32", fg="#F3F4F6",
                           font=("Segoe UI", 24, "bold"))
        latest_lbl.place(x=400, y=85)

    def create_treeview(self):
        style = ttk.Style()
        style.theme_use("default")
        style.configure("Treeview", background="#151F32", foreground="#F3F4F6",
                        fieldbackground="#151F32", rowheight=30, relief="flat")
        style.configure("Treeview.Heading", background="#2ED3B7", foreground="#0B1220",
                        font=("Segoe UI", 12, "bold"))
        style.map("Treeview", background=[("selected", "#2ED3B7")], foreground=[("selected", "#0B1220")])

        self.table = ttk.Treeview(self.content_frame, columns=("user_id", "user_name", "role"), show="headings")
        self.table.heading("user_id", text="User ID")
        self.table.heading("user_name", text="Username")
        self.table.heading("role", text="Role")
        self.table.column("user_id", width=80, anchor="center")
        self.table.column("user_name", width=120, anchor="center")
        self.table.column("role", width=100, anchor="center")
        self.table.place(x=400, y=150, width=710, height=270)

    def load_users(self):
        cursor = self.dbcon.cursor()
        cursor.execute("SELECT user_id, user_name, role FROM users")
        rows = cursor.fetchall()
        cursor.close()

        self.table.delete(*self.table.get_children())
        if rows:
            for row in rows:
                self.table.insert("", "end", values=row)
        else:
            self.table.insert("", "end", values=("No Users", "", ""))

    def create_stats(self):
        frame = Frame(self.content_frame, bg="#0B1220")
        frame.place(x=30, y=150, width=350, height=270)

        cursor = self.dbcon.cursor()

        cursor.execute("SELECT COUNT(*) FROM users")
        total_users = cursor.fetchone()[0]

        cursor.execute("SELECT COUNT(*) FROM users WHERE role='Admin'")
        total_admins = cursor.fetchone()[0]

        cursor.execute("SELECT COUNT(*) FROM users WHERE role!='Admin'")
        total_non_admins = cursor.fetchone()[0]

        cursor.execute("SELECT user_name FROM users ORDER BY user_id DESC LIMIT 1")
        latest_user = cursor.fetchone()
        latest_user = latest_user[0] if latest_user else "N/A"

        cursor.close()

        stats = [
            ("Total Users:", total_users),
            ("Total Admins:", total_admins),
            ("Total Non-Admins:", total_non_admins),
            ("Latest User Added:", latest_user)
        ]

        y_pos = 20
        for text, val in stats:
            Label(frame, text=text, bg="#0B1220", fg="#F3F4F6", font=("Segoe UI", 13, "bold")).place(x=20, y=y_pos)
            Label(frame, text=str(val), bg="#0B1220", fg="#2ED3B7", font=("Segoe UI", 13, "bold")).place(x=180, y=y_pos)
            y_pos += 40

    def add_user(self):
        add_win = Toplevel()
        add_win.geometry("500x400")
        add_win.config(bg="#111828")
        add_win.title("Add User")

        heading = Label(add_win, text="Add New User", bg="#111828", fg="#F3F4F6",
                        font=("Segoe UI", 19, "bold"))
        heading.place(x=140, y=5)

        content_frame = Frame(add_win, bg="#0B1220")
        content_frame.place(x=50, y=50, width=400, height=300)

        labels = ["Username", "Role", "Password"]
        entries = {}
        y_pos = 20
        for lbl in labels:
            Label(content_frame, text=f"Enter {lbl}", bg="#0B1220", fg="#F3F4F6", font=("Segoe UI", 11)).place(x=20, y=y_pos)
            ent = Entry(content_frame, width=25, font=("Segoe UI", 13), bg="#151F32", fg="#F3F4F6",
                        insertbackground="#2ED3B7", highlightbackground="#2ED3B7", highlightcolor="#2ED3B7", relief=FLAT)
            ent.place(x=150, y=y_pos)
            entries[lbl] = ent
            y_pos += 50

        def save_user():
            usr_name = entries["Username"].get().strip()
            usr_role = entries["Role"].get().strip()
            pw = entries["Password"].get().strip()
            if not usr_name or not usr_role or not pw:
                messagebox.showwarning("Warning", "Fields cannot be empty.", parent=add_win)
                return

            cursor = self.dbcon.cursor()
            try:
                cursor.execute("INSERT INTO users(user_name,password,role) VALUES (%s,%s,%s)", (usr_name, pw, usr_role))
                self.dbcon.commit()
            except mysql.connector.IntegrityError:
                messagebox.showerror("Error", "Duplicate data.", parent=add_win)
            finally:
                cursor.close()

            messagebox.showinfo("Success", "User added!", parent=add_win)
            self.load_users()
            add_win.destroy()

        Button(content_frame, text="Save", command=save_user, font=("Segoe UI", 10, "bold"),
               fg="#0B1220", bg="#2ED3B7", relief=FLAT, width=12, height=2,
               activebackground="#31E3BF", activeforeground="#0B1220").place(x=130, y=200)

    def open_update_win(self):
        update_win = Toplevel()
        update_win.geometry("500x400")
        update_win.config(bg="#111828")
        update_win.title("Update User")

        heading = Label(update_win, text="Update User", bg="#111828", fg="#F3F4F6",
                        font=("Segoe UI",19, "bold"))
        heading.place(x=150, y=5)

        content_frame = Frame(update_win, bg="#0B1220")
        content_frame.place(x=50, y=50, width=400, height=300)

        labels = ["User ID", "New Username", "Old Password", "New Password", "Role"]
        entries = {}
        y_pos = 20
        for lbl in labels:
            Label(content_frame, text=f"Enter {lbl}", bg="#0B1220", fg="#F3F4F6", font=("Segoe UI", 11)).place(x=20, y=y_pos)
            ent = Entry(content_frame, width=20, font=("Segoe UI", 13), bg="#151F32", fg="#F3F4F6",
                        insertbackground="#2ED3B7", highlightbackground="#2ED3B7", highlightcolor="#2ED3B7", relief=FLAT)
            ent.place(x=180, y=y_pos)
            entries[lbl] = ent
            y_pos += 40

        def update_user():
            usr_id = entries["User ID"].get().strip()
            new_name = entries["New Username"].get().strip()
            old_pw = entries["Old Password"].get().strip()
            new_pw = entries["New Password"].get().strip()
            role = entries["Role"].get().strip()

            if not (usr_id and new_name and old_pw and new_pw and role):
                messagebox.showwarning("Warning", "Fields cannot be empty.", parent=update_win)
                return

            cursor = self.dbcon.cursor()
            try:
                cursor.execute(
                    "UPDATE users SET user_name=%s, password=%s, role=%s WHERE user_id=%s AND password=%s",
                    (new_name, new_pw, role, usr_id, old_pw)
                )
                self.dbcon.commit()
                if cursor.rowcount == 0:
                    messagebox.showerror("Error", "Invalid User ID or Password.", parent=update_win)
                else:
                    messagebox.showinfo("Success", "User updated successfully.", parent=update_win)
                    self.load_users()
                    update_win.destroy()
            finally:
                cursor.close()

        Button(content_frame, text="Save", command=update_user, font=("Segoe UI", 10, "bold"),
               fg="#0B1220", bg="#2ED3B7", relief=FLAT, width=12, height=2,
               activebackground="#31E3BF", activeforeground="#0B1220").place(x=120, y=220)

    def search_sup(self):
        search_val = self.search_entry.get().strip()
        if not search_val:
            messagebox.showwarning("Warning", "Please enter a search value.", parent=self.dashboard_window)
            return

        cursor = self.dbcon.cursor()
        like_val = f"%{search_val}%"
        cursor.execute("SELECT user_id, user_name, role FROM users WHERE user_id LIKE %s OR user_name LIKE %s OR role LIKE %s",
                       (like_val, like_val, like_val))
        rows = cursor.fetchall()
        cursor.close()

        self.table.delete(*self.table.get_children())
        if rows:
            for row in rows:
                self.table.insert("", "end", values=row)
        else:
            messagebox.showinfo("No Match", "No matching results found.", parent=self.dashboard_window)

    def search_bind(self, event):
        self.search_sup()

    def delete_user(self):
        selected = self.table.selection()
        if not selected:
            messagebox.showwarning("Warning", "No user selected.", parent=self.dashboard_window)
            return

        confirm = messagebox.askyesno("Confirm Delete", f"Delete {len(selected)} user(s)?", parent=self.dashboard_window)
        if not confirm:
            return

        cursor = self.dbcon.cursor()
        try:
            for item in selected:
                user_id = self.table.item(item, "values")[0]
                cursor.execute("DELETE FROM users WHERE user_id=%s", (user_id,))
                self.table.delete(item)
            self.dbcon.commit()
            messagebox.showinfo("Deleted", "Selected user(s) deleted.", parent=self.dashboard_window)
        finally:
            cursor.close()

    def close_connection(self):
        if self.dbcon.is_connected():
            self.dbcon.close()

    def on_close(self):
        self.close_connection()
        self.dashboard_window.destroy()

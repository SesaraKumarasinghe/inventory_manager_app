from tkinter import *
from PIL import Image, ImageTk
from dashboard import Dashboard
from products import ProductsManager
from suppliers import Suppliermanager
from transactions import TransactionsManager
from catagories import CatagoryManager
from reports import ReportsManager

def logged_in_window():
    window2 = Toplevel()
    window2.title("Desktop Inventory Management System")
    window2.geometry("1920x1080")
    window2.config(bg="#111828")

    heading = Label(window2,text="Welcome to DIM System",fg="#F3F4F6",bg="#111828",font=("Segoe UI",48,"bold"))
    heading.place(x=600,y=30)

    underline = Frame(window2, bg="#2ED3B7", height=4, width=1050)
    underline.place(x=460,y=115)

    content_frame = Frame(window2, bg="#0B1220")
    content_frame.place(x=600, y=150, width=750, height=580)

    panel_heading = Label(content_frame, text="Select a Module", fg="#F3F4F6", bg="#0B1220",
                          font=("Segoe UI", 22, "bold"))
    panel_heading.place(x=30, y=10)

    accent = Frame(content_frame, bg="#2ED3B7", height=3, width=750)
    accent.place(x=0, y=70)

    button_grid = Frame(content_frame, bg="#0B1220")
    button_grid.place(x=30, y=90, width=690, height=460)

    img = Image.open("C:\\Pythonprogrammes\\Inventory_management_app\\New folder\\DASHBOARD.jpg")
    dashboard_img = ImageTk.PhotoImage(img)

    def open_dashboard():
        Dashboard(window2)

    dashboard_but = Button(button_grid,text="Dashboard",command=open_dashboard,fg="#F3F4F6",bg="#151F32",font=("Segoe UI", 11, "bold"), image=dashboard_img,compound=TOP,relief=FLAT,activebackground="#1C2A43",activeforeground="#2ED3B7",bd=0,padx=10,pady=10)
    dashboard_but.image = dashboard_img
    dashboard_but.grid(row=0, column=0, padx=20, pady=20)

    img2 = Image.open("C:\\Pythonprogrammes\\Inventory_management_app\\New folder\\PRODUCT.jpg")
    product_img = ImageTk.PhotoImage(img2)

    def open_products():
        ProductsManager(window2)

    product_but = Button(button_grid,text="Products",command=open_products ,fg="#F3F4F6",bg="#151F32",font=("Segoe UI", 11, "bold"), image=product_img,compound=TOP,relief=FLAT,activebackground="#1C2A43",activeforeground="#2ED3B7",bd=0,padx=10,pady=10)
    product_but.image = product_img
    product_but.grid(row=0, column=1, padx=20, pady=20)

    img3 = Image.open("C:\\Pythonprogrammes\\Inventory_management_app\\New folder\\SUPPLIER.jpg")
    supplier_img = ImageTk.PhotoImage(img3)

    def open_suppliers():
        Suppliermanager(window2)

    supplier_but = Button(button_grid,text="Suppliers",command=open_suppliers,fg="#F3F4F6",bg="#151F32",font=("Segoe UI", 11, "bold"), image=supplier_img,compound=TOP,relief=FLAT,activebackground="#1C2A43",activeforeground="#2ED3B7",bd=0,padx=10,pady=10)
    supplier_but.image = supplier_img
    supplier_but.grid(row=0, column=2, padx=20, pady=20)

    img4 = Image.open("C:\\Pythonprogrammes\\Inventory_management_app\\New folder\\TRANSACTIONS.jpg")
    transaction_img = ImageTk.PhotoImage(img4)
    
    def open_transactions():
        TransactionsManager(window2)

    transaction_but = Button(button_grid,text="Transactions",fg="#F3F4F6",command=open_transactions,bg="#151F32",font=("Segoe UI", 11, "bold"), image=transaction_img ,compound=TOP,relief=FLAT,activebackground="#1C2A43",activeforeground="#2ED3B7",bd=0,padx=10,pady=10)
    transaction_but.image = transaction_img
    transaction_but.grid(row=1, column=0, padx=20, pady=20)

    img5 = Image.open("C:\\Pythonprogrammes\\Inventory_management_app\\New folder\\REPORTS.jpg")
    report_img = ImageTk.PhotoImage(img5)

    def open_reports():
        ReportsManager(window2)

    report_but = Button(button_grid,text="Reports",command=open_reports,fg="#F3F4F6",bg="#151F32",font=("Segoe UI", 11, "bold"), image=report_img ,compound=TOP,relief=FLAT,activebackground="#1C2A43",activeforeground="#2ED3B7",bd=0,padx=10,pady=10)
    report_but.image = report_img
    report_but.grid(row=1, column=1, padx=20, pady=20)

    img6 = Image.open("C:\\Pythonprogrammes\\Inventory_management_app\\New folder\\screenshot5.jpg")
    catagory_img = ImageTk.PhotoImage(img6)

    def open_catagories():
        CatagoryManager(window2)

    catagory_but = Button(button_grid,text="Catagories",command=open_catagories,fg="#F3F4F6",bg="#151F32",font=("Segoe UI", 11, "bold"), image=catagory_img ,compound=TOP,relief=FLAT,activebackground="#1C2A43",activeforeground="#2ED3B7",bd=0,padx=10,pady=10)
    catagory_but.image = catagory_img
    catagory_but.grid(row=1, column=2, padx=20, pady=20)



    

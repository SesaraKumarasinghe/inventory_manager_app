from tkinter import *
from PIL import Image, ImageTk
from dashboard import Dashboard
from products import ProductsManager
from suppliers import Suppliermanager
from transactions import TransactionsManager
from catagories import CatagoryManager

def logged_in_window():
    window2 = Toplevel()
    window2.title("Desktop Inventory Management System")
    window2.geometry("1920x1080")
    window2.config(bg="#1E1E1E")

    heading = Label(window2,text="Welcome to DIM System",fg="White",bg="#1E1E1E",font=("Georgia",50,"bold")).place(x=570,y=30)

    underline = Frame(window2, bg="white", height=4, width=1000)
    underline.place(x=500,y=120)

    content_frame = Frame(window2, bg="#252526")
    content_frame.place(x=650, y=150, width=700, height=550)

    img = Image.open("C:\\Pythonprogrammes\\Inventory_management_app\\New folder\\DASHBOARD.jpg")
    dashboard_img = ImageTk.PhotoImage(img)

    def open_dashboard():
        Dashboard(window2)

    dashboard_but = Button(content_frame,text="Dashboard",command=open_dashboard,fg="Black",bg="#BF9031",font=("Georgia", 10, "bold"), image=dashboard_img,compound=TOP,relief=FLAT,activebackground="White",activeforeground="Black",bd=0)
    dashboard_but.image = dashboard_img
    dashboard_but.place(x=50, y=50)

    img2 = Image.open("C:\\Pythonprogrammes\\Inventory_management_app\\New folder\\PRODUCT.jpg")
    product_img = ImageTk.PhotoImage(img2)

    def open_products():
        ProductsManager(window2)

    product_but = Button(content_frame,text="Products",command=open_products ,fg="Black",bg="#BF9031",font=("Georgia", 10, "bold"), image=product_img,compound=TOP,relief=FLAT,activebackground="White",activeforeground="Black",bd=0)
    product_but.image = product_img
    product_but.place(x=270, y=50)

    img3 = Image.open("C:\\Pythonprogrammes\\Inventory_management_app\\New folder\\SUPPLIER.jpg")
    supplier_img = ImageTk.PhotoImage(img3)

    def open_suppliers():
        Suppliermanager(window2)

    supplier_but = Button(content_frame,text="Suppliers",command=open_suppliers,fg="Black",bg="#BF9031",font=("Georgia", 10, "bold"), image=supplier_img,compound=TOP,relief=FLAT,activebackground="White",activeforeground="Black",bd=0)
    supplier_but.image = supplier_img
    supplier_but.place(x=490, y=50)

    img4 = Image.open("C:\\Pythonprogrammes\\Inventory_management_app\\New folder\\TRANSACTIONS.jpg")
    transaction_img = ImageTk.PhotoImage(img4)
    
    def open_transactions():
        TransactionsManager(window2)

    transaction_but = Button(content_frame,text="Transactions",fg="Black",command=open_transactions,bg="#BF9031",font=("Georgia", 10, "bold"), image=transaction_img ,compound=TOP,relief=FLAT,activebackground="White",activeforeground="Black",bd=0)
    transaction_but.image = transaction_img
    transaction_but.place(x=50, y=300)

    img5 = Image.open("C:\\Pythonprogrammes\\Inventory_management_app\\New folder\\REPORTS.jpg")
    report_img = ImageTk.PhotoImage(img5)

    report_but = Button(content_frame,text="Reports",fg="Black",bg="#BF9031",font=("Georgia", 10, "bold"), image=report_img ,compound=TOP,relief=FLAT,activebackground="White",activeforeground="Black",bd=0)
    report_but.image = report_img
    report_but.place(x=270, y=300)

    img6 = Image.open("C:\\Pythonprogrammes\\Inventory_management_app\\New folder\\screenshot5.jpg")
    catagory_img = ImageTk.PhotoImage(img6)

    def open_catagories():
        CatagoryManager(window2)

    catagory_but = Button(content_frame,text="Catagories",command=open_catagories,fg="Black",bg="#BF9031",font=("Georgia", 10, "bold"), image=catagory_img ,compound=TOP,relief=FLAT,activebackground="White",activeforeground="Black",bd=0)
    catagory_but.image = catagory_img
    catagory_but.place(x=490, y=300)



    

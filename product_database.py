import mysql.connector

dbcon = mysql.connector.connect(
    host="localhost",
    user="root",
    password="root",
    database="testdb"
)

cursor = dbcon.cursor()


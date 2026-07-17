import mysql.connector

connection = mysql.connector.connect(
    host="localhost",
    user="root",
    password="pooja@MYSQL66",
    database="day7_sales_db"
)

print("Connected Successfully!")

connection.close()
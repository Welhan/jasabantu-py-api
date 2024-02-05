# # Database configuration
# MYSQL_HOST = 'localhost'
# MYSQL_USER = 'root'  # Ganti dengan username MySQL Anda
# MYSQL_PASSWORD = ''  # Ganti dengan password MySQL Anda
# MYSQL_DB = 'jasabantu'  # Ganti dengan nama database Anda


import mysql.connector

def create_connection():
    conn = mysql.connector.connect(
        host="localhost",
        user="root",
        password="",
        database="jasabantu"
    )
    return conn

def create_connection_admin():
    conn = mysql.connector.connect(
        host="localhost",
        user="root",
        password="",
        database="jasabantu-admin"
    )
    return conn

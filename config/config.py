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
        database="jasabantu_mitra"
    )
    return conn

def create_connection_auth():
    conn = mysql.connector.connect(
        host="localhost",
        user="root",
        password="",
        database="jasabantu-oauth"
    )
    return conn

from database import mysql
from datetime import datetime


class User:        
    def create_user(self, name, username, phone):
        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO user (Name, Username, Phone, CreatedDate) VALUES (%s, %s, %s, %s)", (name, username, phone, datetime.now()))
        mysql.connection.commit()
        cur.close()

    def get_users(self):
        cur = mysql.connection.cursor()
        cur.execute("SELECT * FROM user")
        users = cur.fetchall()
        cur.close()
        return users

    def get_user_by_id(self, user_id):
        cur = mysql.connection.cursor()
        cur.execute("SELECT * FROM user WHERE id = %s", (user_id,))
        user = cur.fetchone()
        cur.close()
        return user

    def delete_user(self, user_id):
        cur = mysql.connection.cursor()
        cur.execute("UPDATE user SET ActiveStatus = %s, UpdatedDate = %s WHERE ID = %s", (0, datetime.now(), user_id,))
        mysql.connection.commit()
        cur.close()

    def checkUsername(self, username):
        cur = mysql.connection.cursor()
        cur.execute("SELECT ID FROM user WHERE Username = %s", (username,))
        user = cur.fetchone()
        cur.close()
        return user

    def checkPhoneRegistered(self, phone):
        cur = mysql.connection.cursor()
        cur.execute('SELECT Phone FROM user WHERE Phone = %s', (phone,))
        user = cur.fetchone()
        cur.close()
        return user
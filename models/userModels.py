from database import mysql
from datetime import datetime

from config.config import create_connection
from config.config import create_connection_admin

class User:        
    USER_REQUEST_TABLE = "user"
    def create_user(self, name, username, phone):
        conn = create_connection()
        cur = conn.cursor()
        query = "INSERT INTO {} (Name, Username, Phone, CreatedDate) VALUES (%s, %s, %s, %s)".format(self.USER_REQUEST_TABLE)
        cur.execute(query, (name, username, phone, datetime.now()))
        conn.commit()
        cur.close()
        if cur.rowcount == 1:
            return cur.lastrowid
        else:
            return 0
        
    def updateUniqueID(self, uniqueid, phone):
        conn = create_connection()
        cur = conn.cursor()
        query = "UPDATE {} SET UniqueID = %s WHERE Phone = %s".format(self.USER_REQUEST_TABLE)
        cur.execute(query, (uniqueid, phone))
        conn.commit()
        cur.close()

    def get_users(self):
        conn = create_connection()
        cur = conn.cursor()
        query = "SELECT * FROM {}".format(self.USER_REQUEST_TABLE)
        cur.execute(query)
        users = cur.fetchall()
        cur.close()
        return users

    def get_user_by_id(self, user_id):
        conn = create_connection()
        cur = conn.cursor()
        query = "SELECT * FROM {} WHERE id = %s".format(self.USER_REQUEST_TABLE)
        cur.execute(query, (user_id,))
        user = cur.fetchone()
        cur.close()
        return user

    def delete_user(self, user_id):
        conn = create_connection()
        cur = conn.cursor()
        query = "UPDATE {} SET ActiveStatus = %s, UpdatedDate = %s WHERE ID = %s".format(self.USER_REQUEST_TABLE)
        cur.execute(query, (0, datetime.now(), user_id,))
        conn.commit()
        cur.close()

    def checkUsername(self, username):
        conn = create_connection()
        cur = conn.cursor()
        query = "SELECT ID FROM {} WHERE Username = %s".format(self.USER_REQUEST_TABLE)
        cur.execute(query, (username,))
        user = cur.fetchone()
        cur.close()
        return user

    def checkPhoneRegistered(self, phone):
        conn = create_connection()
        cur = conn.cursor()
        query = "SELECT Phone FROM {} WHERE Phone = %s".format(self.USER_REQUEST_TABLE)
        cur.execute(query, (phone,))
        user = cur.fetchone()
        cur.close()
        return user
    
    def checkPin(self, phone):
        conn = create_connection()
        cur = conn.cursor()
        query = "SELECT Phone FROM {} WHERE Phone = %s".format(self.USER_REQUEST_TABLE)
        cur.execute(query, (phone,))
        user = cur.fetchone()
        cur.close()
        return user
    
    def getUserByPhone(self, phone):
        conn = create_connection()
        cur = conn.cursor()
        query = "SELECT * FROM {} WHERE Phone = %s".format(self.USER_REQUEST_TABLE)
        cur.execute(query, (phone,))
        user = cur.fetchone()
        cur.close()
        return user
    

    def getUserByUniqueID(self, uniqueid):
        conn = create_connection()
        cur = conn.cursor()
        query = "SELECT * FROM {} WHERE UniqueID = %s".format(self.USER_REQUEST_TABLE)
        cur.execute(query, (uniqueid,))
        user = cur.fetchone()
        cur.close()
        return user
    
    # def saveProfile(self, username, address):
    #     conn = create_connection()
    #     cur = conn.cursor()
    #     cur.execute('SELECT Phone FROM user WHERE Phone = %s', (phone,))
    #     user = cur.fetchone()
    #     cur.close()
    #     return user

    def updatePin(self, uniqueID, pin):
        conn = create_connection()
        cur = conn.cursor()
        query = "UPDATE {} Set Pin = %s WHERE UniqueID = %s".format(self.USER_REQUEST_TABLE)
        cur.execute(query, (pin, uniqueID))
        conn.commit()
        cur.close()
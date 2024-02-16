from database import mysql
from datetime import datetime

from config.config import create_connection
from config.config import create_connection_admin

class User:        
    USER_REQUEST_TABLE = "user"
    def create_user_by_phone(self, phone, uniqueID):
        conn = create_connection()
        cur = conn.cursor()
        query = "INSERT INTO {} (Phone, UniqueID, CreatedDate) VALUES (%s, %s, %s)".format(self.USER_REQUEST_TABLE)
        cur.execute(query, (phone, uniqueID, datetime.now()))
        conn.commit()
        cur.close()
        if cur.rowcount == 1:
            return cur.lastrowid
        else:
            return 0
        
    def create_user_by_email(self, email):
        conn = create_connection()
        cur = conn.cursor()
        query = "INSERT INTO {} (Email, CreatedDate) VALUES (%s, %s)".format(self.USER_REQUEST_TABLE)
        cur.execute(query, (email, datetime.now()))
        conn.commit()
        cur.close()
        if cur.rowcount == 1:
            return cur.lastrowid
        else:
            return 0
    
    def setProfile(self, uniqueid, name):
        conn = create_connection()
        cur = conn.cursor()
        query = "UPDATE {} SET Name = %s WHERE UniqueID = %s".format(self.USER_REQUEST_TABLE)
        cur.execute(query, (name, uniqueid))
        conn.commit()
        cur.close()
        if cur.rowcount == 1:
            return True
        else:
            return False
        
    def updateUniqueID(self, uniqueid, phone = '', email = ''):
        conn = create_connection()
        cur = conn.cursor()
        if phone :
            query = "UPDATE {} SET UniqueID = %s WHERE Phone = %s".format(self.USER_REQUEST_TABLE)
            val = (uniqueid, phone)
        else:
            query = "UPDATE {} SET UniqueID = %s WHERE Email = %s".format(self.USER_REQUEST_TABLE)
            val = (uniqueid, email)
        cur.execute(query, val)
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
        query = "SELECT * FROM {} WHERE UniqueID = %s".format(self.USER_REQUEST_TABLE)
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
        query = "SELECT Phone, Name, Pin, UniqueID FROM {} WHERE Phone = %s".format(self.USER_REQUEST_TABLE)
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
        query = "SELECT Phone, Name, Pin, UniqueID FROM {} WHERE Phone = %s".format(self.USER_REQUEST_TABLE)
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
        query = "UPDATE {} SET Pin = %s WHERE UniqueID = %s".format(self.USER_REQUEST_TABLE)
        cur.execute(query, (pin, uniqueID))
        conn.commit()
        cur.close()

    def getUserByEmail(self, email):
        conn = create_connection()
        cur = conn.cursor()
        query = "SELECT Email, Name, Pin, UniqueID FROM {} WHERE Email = %s".format(self.USER_REQUEST_TABLE)
        cur.execute(query, (email,))
        user = cur.fetchone()
        cur.close()
        return user
    
    def getLastUniqueID(self):
        conn = create_connection()
        cur = conn.cursor()
        query = "SELECT ID, UniqueID FROM {} ORDER BY ID DESC LIMIT 1".format(self.USER_REQUEST_TABLE)
        cur.execute(query)
        uniqueid = cur.fetchone()
        cur.close
        return uniqueid
    
    def getLastCounterUniqueID(self):
        conn = create_connection()
        cur = conn.cursor()
        cur.execute("SELECT Counter FROM systab")
        counter = cur.fetchone()
        cur.close
        return counter
    
    def checkCounterPin(self, uniqueid):
        conn = create_connection()
        cur = conn.cursor()
        query = "SELECT CounterFailed FROM {} WHERE UniqueID = %s".format(self.USER_REQUEST_TABLE)
        cur.execute(query, (uniqueid,))
        counter = cur.fetchone()
        cur.close
        return counter
    
    def counterPin(self, uniqueid, counter):
        conn = create_connection()
        cur = conn.cursor()
        query = "UPDATE {} SET CounterFailed = %s WHERE UniqueID = %s".format(self.USER_REQUEST_TABLE)
        cur.execute(query, (counter, uniqueid,))
        conn.commit()
        cur.close()

    def setNonActiveUser(self, uniqueid):
        conn = create_connection()
        cur = conn.cursor()
        query = "UPDATE {} SET ActiveStatus = %s WHERE UniqueID = %s".format(self.USER_REQUEST_TABLE)
        cur.execute(query, (0, uniqueid,))
        conn.commit()
        cur.close()
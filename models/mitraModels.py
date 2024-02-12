from database import mysql
from datetime import datetime

from config.config import create_connection_admin

class Mitra:        
    MITRA_REQUEST_TABLE = "user"

    def registerMitra(self,UniqueID, nama, email, pin):
        conn = create_connection_admin()
        cur = conn.cursor()
        query = "INSERT INTO {} (Nama, Email, Pin, )".format(self.MITRA_REQUEST_TABLE)
        cur.execute(query, (UniqueID,))
        mitra = cur.fetchone()
        cur.close
        return mitra
    
    def getMitraLogin(self, email = '', phone = ''):
        conn = create_connection_admin()
        cur = conn.cursor()
        if(email) :
            query = "SELECT Email, Pin FROM {} WHERE 1 = 1".format(self.MITRA_REQUEST_TABLE)
            query += " AND Email = %s"
            cur.execute(query, (email,))
        if(phone) : 
            query = "SELECT Phone, Pin FROM {} WHERE 1 = 1".format(self.MITRA_REQUEST_TABLE)
            query += " AND Phone = %s"
            cur.execute(query, (phone,))
        mitra = cur.fetchone()
        cur.close
        return mitra
    

    def getLastUniqueID(self):
        conn = create_connection_admin()
        cur = conn.cursor()
        query = "SELECT ID, UniqueID FROM {} ORDER BY ID DESC LIMIT 1".format(self.MITRA_REQUEST_TABLE)
        cur.execute(query)
        uniqueid = cur.fetchone()
        cur.close
        return uniqueid
    
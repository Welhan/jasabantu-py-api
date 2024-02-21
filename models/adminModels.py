from config.config import create_connection
from config.config import create_connection_admin

from datetime import datetime


class Admin:        
    ADMIN_REQUEST_TABLE = "admin"

    def getDataAdminByEmail(self, email):
        conn = create_connection_admin()
        cur = conn.cursor()
        query = "SELECT * FROM {} WHERE Email = %s".format(self.ADMIN_REQUEST_TABLE)
        cur.execute(query, (email,))

        mitra = cur.fetchone()
        cur.close()
        return mitra
    
    def updateLogin(self, email):
        conn = create_connection_admin()
        cur = conn.cursor()
        query = "UPDATE {} SET LoginF = %s, LastLogin = %s WHERE Email = %s".format(self.ADMIN_REQUEST_TABLE)
        cur.execute(query, (1, datetime.now(), email))
        conn.commit()
        cur.close()
        return True if cur.rowcount == 1 else False
    
    def logoutAdmin(self, email):
        conn = create_connection_admin()
        cur = conn.cursor()
        query = "UPDATE {} SET LoginF = %s WHERE Email = %s".format(self.ADMIN_REQUEST_TABLE)
        cur.execute(query, (0,  email))
        conn.commit()
        cur.close()
        return True if cur.rowcount == 1 else False
    
    
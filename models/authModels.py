from config.config import create_connection_auth
from datetime import datetime

class Auth:
    AUTH_DB = "oauthuser"
    def new_login(self, uniqueID, token, addr = ""):
        conn = create_connection_auth()
        cur = conn.cursor()
        query = "INSERT INTO {} (UniqueID, Token, Mac_Addr, CreatedDate) VALUES (%s, %s, %s, %s)".format(self.AUTH_DB)
        cur.execute(query, (uniqueID, token, addr, datetime.now()))
        conn.commit()
        cur.close()
        if cur.rowcount == 1:
            return cur.lastrowid
        else:
            return 0
        
    def update_login(self, uniqueID, token, addr = ""):
        conn = create_connection_auth()
        cur = conn.cursor()
        query = "UPDATE {} SET Token = %s, Address = %s WHERE UniqueID = %s".format(self.AUTH_DB)
        cur.execute(query, (token, addr, uniqueID,))
        conn.commit()
        cur.close()
        if cur.rowcount == 1:
            return True
        else:
            return False
        
    def check_uniqueID(self, uniqueID):
        conn = create_connection_auth()
        cur = conn.cursor()
        query = "SELECT * FROM {} WHERE UniqueID = %s".format(self.AUTH_DB)
        cur.execute(query, (uniqueID,))
        auth = cur.fetchone()
        cur.close()
        return False if auth is None else True
    
    def logout(self, uniqueID):
        conn = create_connection_auth()
        cur = conn.cursor()
        query = "DELETE FROM {} WHERE UniqueID = %s".format(self.AUTH_DB)
        cur.execute(query, (uniqueID,))
        conn.commit()
        auth = cur.rowcount
        cur.close()
        if auth > 0 :
            return True
        else : 
            return False

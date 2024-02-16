from config.config import create_connection
from config.config import create_connection_admin

class Mitra:        
    MITRA_REQUEST_TABLE = "user"

    def getMitra(self):
        conn = create_connection_admin()
        cur = conn.cursor()
        query = "SELECT * FROM {}".format(self.MITRA_REQUEST_TABLE)
        cur.execute(query)
        mitra = cur.fetchall()
        cur.close
        return mitra
    
    def registerMitra(self, uniqueid='', nama='', email='', phone='', pin = '', address = ''):
        conn = create_connection_admin()
        cur = conn.cursor()
        query = "INSERT INTO {} (UniqueID, Name, Email, Phone, Pin, Address) VALUES (%s,%s,%s,%s,%s,%s)".format(self.MITRA_REQUEST_TABLE)
        try:
            cur.execute(query, (uniqueid, nama, email, phone,pin, address))
            conn.commit()
            cur.close()
            conn.close()
            return True
        except Exception as e:
            print("Error:", e)
            cur.close()
            conn.close()
            return False

    
    def getMitraLogin(self, email = '', phone = ''):
        conn = create_connection_admin()
        cur = conn.cursor()
        if(email) :
            query = "SELECT Email, Pin FROM {} WHERE 1 = 1".format(self.MITRA_REQUEST_TABLE)
            query += " AND Email = %s"
            try:
                cur.execute(query, (email,))
                mitra = cur.fetchone()
                cur.close
                return mitra
            except Exception as e:
                print("Error:", e)
                cur.close()
                conn.close()
                return False
            
        if(phone) : 
            query = "SELECT Phone, Pin FROM {} WHERE 1 = 1".format(self.MITRA_REQUEST_TABLE)
            query += " AND Phone = %s"
            try:
                cur.execute(query, (phone,))
                mitra = cur.fetchone()
                cur.close
                return mitra
            except Exception as e:
                print("Error:", e)
                cur.close()
                conn.close()
                return False
        
    

    def getLastUniqueID(self):
        conn = create_connection_admin()
        cur = conn.cursor()
        query = "SELECT ID, UniqueID FROM {} ORDER BY ID DESC LIMIT 1".format(self.MITRA_REQUEST_TABLE)
        cur.execute(query)
        uniqueid = cur.fetchone()
        cur.close
        return uniqueid
    
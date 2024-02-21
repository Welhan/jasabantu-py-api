from config.config import create_connection
from config.config import create_connection_admin

class Mitra:        
    MITRA_REQUEST_TABLE = "user"

    def getMitra(self, start='', length='', email='', name='', phone=''):
        conn = create_connection_admin()
        cur = conn.cursor()
        query = "SELECT UniqueID, Phone, Name, Address, Email, CreatedDate FROM {}".format(self.MITRA_REQUEST_TABLE)
        if email or name or phone:
            conditions = []
            params = []
            if email:
                conditions.append("Email = %s")
                params.append(email)
            if name:
                conditions.append("Name = %s")
                params.append(name)
            if phone:
                conditions.append("Phone = %s")
                params.append(phone)
            
            if conditions:
                query += " WHERE " + " AND ".join(conditions)
                cur.execute(query, tuple(params))
        else:
            query += " LIMIT %s OFFSET %s"
            cur.execute(query, (length, start))

        mitra = cur.fetchall()
        cur.close()
        return mitra

    
    def getDataMitra(self, uniqueid):
        conn = create_connection_admin()
        cur = conn.cursor()
        query = "SELECT Name, Phone, Email, Address FROM {} WHERE UniqueID = %s".format(self.MITRA_REQUEST_TABLE)
        cur.execute(query, (uniqueid,))
        mitra = cur.fetchone()
        cur.close()
        return mitra

    def getTotalMitra(self):
        conn = create_connection_admin()
        cur = conn.cursor()
        query = "SELECT Value FROM systab WHERE Config = 'Counter'"
        cur.execute(query)
        uniqueid = cur.fetchone()
        cur.close
        return uniqueid
    
    
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
        

    def updateDataMitra(self, nama = '', email = '', phone = '', address = '', uniqueid = ''):
        conn = create_connection_admin()
        cur = conn.cursor()
        query = "UPDATE {} SET Name = %s, Email = %s, Phone = %s, Address = %s WHERE UniqueID = %s".format(self.MITRA_REQUEST_TABLE)
        try:
            cur.execute(query, (nama, email, phone, address, uniqueid))
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
            query = "SELECT Email, Pin, UniqueID FROM {} WHERE 1 = 1".format(self.MITRA_REQUEST_TABLE)
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
            query = "SELECT Phone, Pin, UniqueID FROM {} WHERE 1 = 1".format(self.MITRA_REQUEST_TABLE)
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
    
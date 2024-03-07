from config.config import create_connection

class Sys:        
    SYSTAB = "systab"
    def prefix(self):
        conn = create_connection()
        cur = conn.cursor()
        query = "SELECT Value FROM {} WHERE Config = 'Prefix'".format(self.SYSTAB)
        cur.execute(query)
        result = cur.fetchone()
        cur.close()
        return result
    
    def endfix(self):
        conn = create_connection()
        cur = conn.cursor()
        query = "SELECT Value FROM {} WHERE Config = 'Counter'".format(self.SYSTAB)
        cur.execute(query)
        result = cur.fetchone()
        cur.close()
        return result
    
    def addCounter(self, counter):
        conn = create_connection()
        cur = conn.cursor()
        query = "UPDATE {} SET Value = %s WHERE Config = 'Counter'".format(self.SYSTAB)
        cur.execute(query, (counter,))
        conn.commit()
        cur.close()

    def checkMaintenanceState(self):
        conn = create_connection()
        cur = conn.cursor()
        query = "SELECT Value FROM {} WHERE Config = %s".format(self.SYSTAB)
        cur.execute(query, ('Maintenance',))
        users = cur.fetchall()
        cur.close()
        return users

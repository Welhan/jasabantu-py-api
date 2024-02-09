from database import mysql
from datetime import datetime

from config.config import create_connection
from config.config import create_connection_admin

class Mitra:        
    MITRA_REQUEST_TABLE = "user"

    def getLastUniqueID(self):
        conn = create_connection_admin()
        cur = conn.cursor()
        query = "SELECT ID, UniqueID FROM {} ORDER BY ID DESC LIMIT 1".format(self.MITRA_REQUEST_TABLE)
        cur.execute(query)
        uniqueid = cur.fetchone()
        cur.close
        return uniqueid
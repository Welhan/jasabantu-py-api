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
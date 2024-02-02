from database import mysql
from datetime import datetime
import pytz
from config.constants import zona_waktu

class Otp:
    OTP_REQUEST_TABLE = "otp_request"
    # lokasi = 'Asia/Jakarta'
    # zona_waktu = pytz.timezone(lokasi)
    def create_otp(self, phone, otp):
        cur = mysql.connection.cursor()
        query = "INSERT INTO {} (Phone, Otp,CreatedDate) VALUES (%s, %s, %s)".format(self.OTP_REQUEST_TABLE)
        cur.execute(query, (phone, otp,datetime.now(zona_waktu)))
        mysql.connection.commit()
        cur.close()

    def check_otp(self, phone, otp):
        cur = mysql.connection.cursor()
        cur.execute("SELECT ID, CreatedDate FROM otp_request WHERE Phone = %s AND Otp = %s", (phone, otp,))
        check = cur.fetchone()
        cur.close()
        return check
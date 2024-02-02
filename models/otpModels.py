from database import mysql
from datetime import datetime
import pytz
from config.constants import zona_waktu

class Otp:
    OTP_REQUEST_TABLE = "otp_request"
    # lokasi = 'Asia/Jakarta'
    # zona_waktu = pytz.timezone(lokasi)
    def create_otp(self, phone, otp, counter):
        cur = mysql.connection.cursor()
        query = "INSERT INTO {} (Phone, Otp, RequestDate, Counter) VALUES (%s, %s, %s, %s)".format(self.OTP_REQUEST_TABLE)
        cur.execute(query, (phone, otp ,datetime.now(zona_waktu), counter,))
        mysql.connection.commit()
        cur.close()

    def update_otp(self, phone, otp, counter):
        cur = mysql.connection.cursor()
        query = "UPDATE {} SET Otp = %s, Counter = %s, RequestDate = %s WHERE Phone = %s".format(self.OTP_REQUEST_TABLE)
        cur.execute(query, (otp, counter, datetime.now(zona_waktu), phone,))
        mysql.connection.commit()
        cur.close()

    def check_phone_exist(self, phone):
        cur = mysql.connection.cursor()
        cur.execute("SELECT ID, Counter, RequestDate FROM otp_request WHERE Phone = %s ", (phone,))
        check = cur.fetchone()
        cur.close()
        return check

    def check_otp(self, phone, otp):
        cur = mysql.connection.cursor()
        cur.execute("SELECT ID, RequestDate FROM otp_request WHERE Phone = %s AND Otp = %s", (phone, otp,))
        check = cur.fetchone()
        cur.close()
        return check
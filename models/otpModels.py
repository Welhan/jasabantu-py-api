from database import mysql
from datetime import datetime
from config.constants import zona_waktu

from config.config import create_connection
from config.config import create_connection_admin

class Otp:
    OTP_REQUEST_TABLE = "otp_request"
    # lokasi = 'Asia/Jakarta'
    # zona_waktu = pytz.timezone(lokasi)
    def create_otp(self, phone, otp, counter):
        conn = create_connection()
        cur = conn.cursor()        
        query = "INSERT INTO {} (Phone, Otp, RequestDate, Counter) VALUES (%s, %s, %s, %s)".format(self.OTP_REQUEST_TABLE)
        cur.execute(query, (phone, otp ,datetime.now(zona_waktu), counter,))
        conn.commit()
        cur.close()

    def update_otp(self, phone, otp, counter):
        conn = create_connection()
        cur = conn.cursor()        
        query = "UPDATE {} SET Otp = %s, Counter = %s, RequestDate = %s WHERE Phone = %s".format(self.OTP_REQUEST_TABLE)
        cur.execute(query, (otp, counter, datetime.now(zona_waktu), phone,))
        conn.commit()
        cur.close()

    def check_phone_exist(self, phone, otp = 0):
        conn = create_connection()
        cur = conn.cursor()        
        if otp :
            cur.execute("SELECT ID, Counter, RequestDate FROM otp_request WHERE Phone = %s AND Otp = %s", (phone, otp,))
        else:
            cur.execute("SELECT ID, Counter, RequestDate FROM otp_request WHERE Phone = %s ", (phone,))
        check = cur.fetchone()
        cur.close()
        return check

    def check_otp(self, phone):
        conn = create_connection()
        cur = conn.cursor()        
        cur.execute("SELECT ID, Otp FROM otp_request WHERE Phone = %s", (phone,))
        check = cur.fetchone()
        cur.close()
        return check    

    def checkOtp(self, otp):
        conn = create_connection()
        cur = conn.cursor()        
        cur.execute("SELECT ID FROM otp_request WHERE Otp = %s", (otp,))
        check = cur.fetchone()
        cur.close()
        return check
    
    def delete_otp (self, phone):
        conn = create_connection()
        cur = conn.cursor()        
        query = "DELETE FROM {} WHERE Phone = %s".format(self.OTP_REQUEST_TABLE)
        cur.execute(query, (phone,))
        conn.commit()
        cur.close()
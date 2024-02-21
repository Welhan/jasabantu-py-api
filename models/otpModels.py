from database import mysql
from datetime import datetime
from config.constants import zona_waktu

from config.config import create_connection

class Otp:
    OTP_REQUEST_TABLE = "otp_request"
    # lokasi = 'Asia/Jakarta'
    # zona_waktu = pytz.timezone(lokasi)
    def create_otp(self, requestFrom, otp, counter):
        conn = create_connection()
        cur = conn.cursor()        
        query = "INSERT INTO {} (RequestFrom, Otp, RequestDate, Counter) VALUES (%s, %s, %s, %s)".format(self.OTP_REQUEST_TABLE)
        cur.execute(query, (requestFrom, otp ,datetime.now(zona_waktu), counter,))
        conn.commit()
        cur.close()

    def update_otp(self, requestFrom, otp, counter):
        conn = create_connection()
        cur = conn.cursor()        
        query = "UPDATE {} SET Otp = %s, Counter = %s, RequestDate = %s WHERE RequestFrom = %s".format(self.OTP_REQUEST_TABLE)
        cur.execute(query, (otp, counter, datetime.now(zona_waktu), requestFrom,))
        conn.commit()
        cur.close()

    def check_request_exist(self, requestFrom, otp = 0):
        conn = create_connection()
        cur = conn.cursor()        
        if otp :
            cur.execute("SELECT ID, Counter, RequestDate FROM otp_request WHERE RequestFrom = %s AND Otp = %s", (requestFrom, otp,))
        else:
            cur.execute("SELECT ID, Counter, RequestDate FROM otp_request WHERE RequestFrom = %s ", (requestFrom,))
        check = cur.fetchone()
        cur.close()
        return check

    def check_otp(self, phone):
        conn = create_connection()
        cur = conn.cursor()        
        cur.execute("SELECT ID, Otp, Counter FROM otp_request WHERE RequestFrom = %s", (phone,))
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
        query = "DELETE FROM {} WHERE RequestFrom = %s".format(self.OTP_REQUEST_TABLE)
        cur.execute(query, (phone,))
        conn.commit()
        cur.close()
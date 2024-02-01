from database import mysql
from datetime import datetime

class Otp:
    OTP_REQUEST_TABLE = "otp_request"
    def create_otp(self, phone, otp):
        cur = mysql.connection.cursor()
        # cur.execute("INSERT INTO {} (Phone, Otp) VALUES (%s, %s)", (phone, otp)).format(self.OTP_REQUEST_TABLE)
        cur.execute("INSERT INTO otp_request (Phone, Otp) VALUES (%s, %s)", (phone, otp))
        mysql.connection.commit()
        cur.close()
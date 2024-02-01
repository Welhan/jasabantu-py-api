from database import mysql
from datetime import datetime

class Otp:
    OTP_REQUEST_TABLE = "otp_request"
    def create_otp(self, phone, otp):
        cur = mysql.connection.cursor()
        query = "INSERT INTO {} (Phone, Otp) VALUES (%s, %s)".format(self.OTP_REQUEST_TABLE)
        cur.execute(query, (phone, otp))
        # cur.execute("INSERT INTO otp_request (Phone, Otp) VALUES (%s, %s)", (phone, otp))
        mysql.connection.commit()
        cur.close()
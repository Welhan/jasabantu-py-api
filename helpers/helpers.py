from flask import Blueprint, jsonify, request
from models.userModels import User
from models.otpModels import Otp
import random
import bcrypt
import requests
import time

from config.constants import WA_ENGINE, SECRET_KEY, SALT_KEY



user_model = User()
otp_model = Otp()

def generate_otp(phone, type):
    otp = str(random.randint(1000,9999))
    data = {
            "message" : "*" +str(otp)+"* adalah kode OTP untuk pendaftaran akun anda. Mohon untuk tidak membagikan atau memberitahukan kode ini kepada siapapun.",
            "recipient" : phone
        }
    checkOtpPhone = otp_model.check_phone_exist(phone)

    if checkOtpPhone is not None:
        count = int(checkOtpPhone[1])
        if count + 1 >= 6:
            delay = 86400
        else:
            if count + 1 >= 5 :
                delay = (count * 3600) - 5
            else:
                delay = (count * 300) - 5

        if delay > 86400: 
            delay = 5

    else:
        count = 0
        delay = 5

    time.sleep(2)
    if(type == 'WA'):
        response = requests.post(WA_ENGINE, data=data)
        if response.status_code == 200:
            data = response.json()
            
            if checkOtpPhone is None:
                otp_model.create_otp(phone, bcrypt.hashpw(otp.encode('utf-8'), SALT_KEY), count + 1)
            else:
                otp_model.update_otp(phone, bcrypt.hashpw(otp.encode('utf-8'), SALT_KEY), count + 1)
            return True
        else:
            return False
    elif(type == 'SMS'): 
        response = requests.post(WA_ENGINE, data=data)
        if response.status_code == 200:
            data = response.json()
            if checkOtpPhone is None:
                otp_model.create_otp(phone, bcrypt.hashpw(otp.encode('utf-8'), SALT_KEY), count + 1)
            else:
                otp_model.update_otp(phone, bcrypt.hashpw(otp.encode('utf-8'), SALT_KEY), count + 1)
            return True
        else:
            return False
    else:
        return False
    
def checkOtp(otp,phone):
    getOtp = otp_model.check_otp(phone)
    if bcrypt.checkpw(otp.encode('utf-8'), getOtp[1].encode('utf-8')):
        return True
    else:
        return False

def checkPin(phone = '', email='', uniqueid ='', pin=''):
    if(phone):
       result = user_model.getUserByPhone(phone)[4]
    elif(email):
       result = user_model.getUserByEmail(email)[4]
    elif(uniqueid):
       result = user_model.getUserByUniqueID(uniqueid)[4]
    else:
        return False
    if(pin == result):
        return True
    else:
        return False
    
    
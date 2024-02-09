from flask import Blueprint, jsonify, request
from models.userModels import User
from models.otpModels import Otp
from models.authModels import Auth
from models.mitraModels import Mitra
import random
import bcrypt
import requests
import time
import jwt

from config.constants import WA_ENGINE, SECRET_KEY, SALT_KEY



user_model = User()
otp_model = Otp()
auth_model = Auth()
mitra_model = Mitra()

def generate_otp(phone, type):
    otp = str(random.randint(100000,999999))
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
    
    otp = bcrypt.hashpw(otp.encode('utf-8'), SALT_KEY)
    if(type == 'WA'):
        response = requests.post(WA_ENGINE, data=data)
        if response.status_code == 200:
            data = response.json()
            
            if checkOtpPhone is None:
                otp_model.create_otp(phone, otp, count + 1)
            else:
                otp_model.update_otp(phone, otp, count + 1)
            return True
        else:
            return False
    elif(type == 'SMS'): 
        response = requests.post(WA_ENGINE, data=data)
        if response.status_code == 200:
            data = response.json()
            if checkOtpPhone is None:
                otp_model.create_otp(phone, otp, count + 1)
            else:
                otp_model.update_otp(phone, otp, count + 1)
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
    if bcrypt.checkpw(pin.encode('utf-8'), result.encode('utf-8')):
        return True
    else:
        return False
    
def generate_token(UniqueID):
    payload = {'uniqueID' : UniqueID}
    return jwt.encode(payload, SECRET_KEY,algorithm='HS256')

def insert_oauth(uniqueID, token, addr = ""):
    insert = auth_model.new_login(uniqueID, token, addr)

    if insert > 1:
        return True
    
    return False

def generate_uniqueid():
    user = user_model.getLastUniqueID()
    mitra = mitra_model.getLastUniqueID()
    user = str(user[1])
    mitra = str(mitra[1])
    user = int(user[5:])
    mitra = int(mitra[5:])
    UniqueID = str(random.randint(10000,99999))
    if user > mitra:
        return UniqueID + str(user + 1)
    elif user < mitra:
        return UniqueID + str(mitra + 1)
    elif user == mitra:
        return UniqueID + str(user + 1)

    
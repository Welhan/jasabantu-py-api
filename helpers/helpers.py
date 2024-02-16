# from flask import Blueprint, jsonify, request
from models.userModels import User
from models.otpModels import Otp
from models.authModels import Auth
from models.mitraModels import Mitra
from models.sysModel import Sys
import random
import bcrypt
import requests
import time
import jwt
from config.constants import *
import base64
import re

user_model = User()
otp_model = Otp()
auth_model = Auth()
mitra_model = Mitra()
sys_model = Sys()

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

def checkPin(user ='', pin=''):
    if user:
        if user.isdigit():
            result = user_model.getUserByPhone(user)[2]
        elif user.isalpha():
            result = user_model.getUserByEmail(user)[2]
    else:
        return False
    
    if result is not None:
        if bcrypt.checkpw(pin.encode('utf-8'), result.encode('utf-8')):
            return True
        else:
            return False
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

def update_oauth(uniqueID, token, addr = ""):
    insert = auth_model.update_login(uniqueID, token, addr)

    if insert > 1:
        return True
    return False

def generate_uniqueid():
    Prefix = str(sys_model.prefix()[0])
    Counter = sys_model.endfix()[0]
    if(Counter is None) :
        LastCounter = 1
    else :
        LastCounter = int(Counter) + 1
    UniqueID = Prefix + str(random.randint(10000,99999)) + str(LastCounter)
    sys_model.addCounter(LastCounter)
    return UniqueID

def rot(text):
    result = ''
    for char in text:
        if char in ROT_KEY:
            new_char = ROT_KEY[(ROT_KEY.index(char) + ROT_NUM) % len(ROT_KEY)]
        else:
            result += char
        result += new_char
    return result

def unrot(text):
    result = ''
    for char in text:
        if char in ROT_KEY: 
            new_char = ROT_KEY[(ROT_KEY.index(char) - ROT_NUM) % len(ROT_KEY)]
        else:
            new_char = char  
        result += new_char  
    return result

def generate_encode(text):
    result = rot(text)

    # return result

    return base64.b64encode(result.encode('utf-8')).decode()

def generate_decode(token):
   result = base64.b64decode(token).decode()
   return unrot(result)

def is_valid_email(email):
    pattern = r'^[\w\.-]+@[\w\.-]+\.\w+$'
    if re.match(pattern, email):
        return True
    else:
        return False
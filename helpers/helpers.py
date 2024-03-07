# from flask import Blueprint, jsonify, request
from datetime import date
from flask import Request, request
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
import re
import base64
from email.mime.text import MIMEText
from google_auth_oauthlib.flow import InstalledAppFlow
from google.oauth2.credentials import Credentials
from google.auth.transport.requests import Request
from googleapiclient.discovery import build
import pickle
import os

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
    
    checkOtpPhone = otp_model.check_request_exist(phone)

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
            return [True, delay]
        else:
            return False
    elif(type == 'SMS'): 
        response = requests.post(WA_ENGINE + 'send-message-bot', data=data)
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
        if char in NEW_KEY:
            new_char = NEW_KEY[(NEW_KEY.index(char) + ROT_NUM) % len(NEW_KEY)]
        else:
            result += char
        result += new_char
    return result

def unrot(text):
    result = ''
    for char in text:
        if char in NEW_KEY: 
            new_char = NEW_KEY[(NEW_KEY.index(char) - ROT_NUM) % len(NEW_KEY)]
        else:
            new_char = char  
        result += new_char  
    return result

def encode(text):
    result = rot(text)
    return PREFIX_KEY + base64.b64encode(result.encode('utf-8')).decode() # ignore

def decode(token):
    token = token.split("$")[3] 
    result = base64.b64decode(token).decode()
    return unrot(result)

def is_valid_email(email):
    pattern = r'^[\w\.-]+@[\w\.-]+\.\w+$'
    if re.match(pattern, email):
        return True
    else:
        return False
    
def send_otp_email(email):
    otp = str(random.randint(100000,999999))

    SCOPES = ['https://www.googleapis.com/auth/gmail.send']
    creds = None

    if os.path.exists('config/token.pickle'):
        with open('config/token.pickle', 'rb') as token:
            creds = pickle.load(token)
            if creds.refresh_token:
                creds.refresh(Request())
                with open('config/token.pickle', 'wb') as token:
                    pickle.dump(creds, token)
    
    if not creds or not creds.valid:
        flow = InstalledAppFlow.from_client_secrets_file('config/credential.json', SCOPES)
        creds = flow.run_local_server(port=0, prompt='consent')
    
    with open('config/token.pickle', 'wb') as token:
        pickle.dump(creds, token)

    service = build('gmail', 'v1', credentials=creds)

    message = MIMEText(f"""
    <html>
        <body>
            <div style="font-family: Helvetica,Arial,sans-serif; min-width:1000px; overflow:auto; line-height:2">
                <div style="margin:50px auto; width:100%; padding:20px 0">
                    <div style="border-bottom:1px solid #eee">
                        <a href="" style="font-size:1.4em; color: #f39c12; text-decoration:none; font-weight:600">JasaBantu</a>
                    </div>
                    <p style="font-size:1.1em">Hi,</p>
                    <p>Thank you for choosing JasaBantu. Use the following OTP to complete your Sign Up procedures. OTP is valid for 5 minutes</p>
                    <h2 style="background: #f39c12; margin: 0 auto; width: max-content; padding: 0 10px; color: #fff; border-radius: 4px;">{otp}</h2>
                    <p style="font-size:0.9em;">Regards,<br />JasaBantu</p>
                    <hr style="border:none; border-top:1px solid #eee" />
                    <div style="float:right; padding:8px 0; color:#aaa; font-size:0.8em; line-height:1; font-weight:300">
                        <p>PT. Aplikasi Karya Jasa Bantu</p>
                        <p>Ruko Boston RBRB 10-11</p>
                        <p>Pantai Indah Kapuk 2</p>
                    </div>
                </div>
            </div>
        </body>
    </html>
    """, 'html')
    message['to'] = email
    message['subject'] = 'OTP Verification'

    raw_message = base64.urlsafe_b64encode(message.as_bytes()).decode()

    checkEmail = otp_model.check_request_exist(email)

    if checkEmail is not None:
        if(checkEmail[2] == date.today()):
            count = int(checkEmail[1])
            if count + 1 >= 6:
                delay = 86400
            else:
                if count + 1 >= 5 :
                    delay = (count * 3600) - 5
                else:
                    delay = (count * 300) - 5

            if delay > 86400: 
                delay = 5 * 60
        else:
            count = 0
            delay = 5 * 60
    else:
        count = 0
        delay = 5 * 60

    try:
        sent_message = service.users().messages().send(userId='me', body={'raw': raw_message}).execute()

        otp = bcrypt.hashpw(otp.encode('utf-8'), SALT_KEY)
        if checkEmail is None:
            otp_model.create_otp(email, otp, count + 1)
        else:
            otp_model.update_otp(email, otp, count + 1)
        print(f"Sent message to {message['to']}. Message Id: {sent_message['id']}")
        return [True, delay]
    except Exception as e:
        print(f"An error occurred: {e}")
        return False
    

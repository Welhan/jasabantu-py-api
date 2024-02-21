from flask import Blueprint, Response, jsonify, request
from models.userModels import User
from models.otpModels import Otp
from models.mitraModels import Mitra
from config.constants import WA_ENGINE, SECRET_KEY, SALT_KEY, path_auth
from helpers.helpers import *
import bcrypt
import yagmail
import base64
from google.oauth2 import service_account
from googleapiclient.discovery import build
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
# import random
# import json
# import jwt
# import requests
# import time


user_bp = Blueprint('user_bp', __name__)
user_model = User()
otp_model = Otp()
mitra_model = Mitra()

#delimiter
regis_delimiter = ":"

# Untuk Contoh Auzthorization (nnt hapus)
@user_bp.route('/user_token', methods = ['POST'])
def user_token():
    auth = request.authorization

    if not auth or not auth.token:
        return jsonify({'message': 'Invalid credentials'}), 401
    
    token = decode(auth.token)

    data = request.get_json()
    delimiter = str(data.get('delimiter'))

    result = token. split(delimiter)

    data = {
        "param1" : result[0],
        'param2' : result[1]
    }
    
    return jsonify({"status": 'success', 'data': data}), 200

@user_bp.route('/getUser', methods=['GET'])
def getUser():
    getUser = user_model.get_users()

    if not getUser:
        return jsonify({"status": 'success', 'data': []}), 200
    else:
        data = []
        for row in getUser:
            row_dict = {
                "UniqueID": row[1],
                "Name": row[2],
                "Email": row[7],
                "Phone": row[7],
            }
            data.append(row_dict)

        response = {
            "status": "success",
            "data": data
        }
        return jsonify(response), 200
    
@user_bp.route('/check_phone', methods=['POST'])
def check_phone():
    data = request.get_json()
    phone = str(data.get('phone'))
    
    if not data or 'phone' not in data:
        return jsonify({"status" : "failed","message": "Data tidak lengkap"}), 400

    checkPhone = user_model.checkPhoneRegistered(phone)
    if checkPhone is None:
        return jsonify({"status" : "success","message": "Lanjutkan Registrasi"}), 200 
    else:
        return jsonify({"status" : "failed","message": "No.HP sudah terdaftar, silahkan login atau gunakan No.HP lain."}), 303 

# Keperluan Test ROT dan Encode
@user_bp.route('/test_rot', methods=['POST'])
def test_rot():
    data = request.get_json()
    param1 = data.get('param1')
    param2 = data.get('param2')
    delimiter = data.get('delimiter')
    res = str(param1)
    if param2 is not None and delimiter is not None:
        res = str(param1) + str(delimiter) + str(param2)
    
    result = encode(res)
    response = {
        "status": "success",
        "data": result
    }
    return jsonify(response), 200

@user_bp.route('/new_users', methods=['POST'])
def create_user():
    data = request.get_json()
    phone = str(data.get('phone'))
    type = str(data.get('type'))
    
    if not data or 'phone' not in data:
        return jsonify({"status" : "failed","message": "Data tidak lengkap"}), 202

    checkPhone = user_model.checkPhoneRegistered(phone)
    if checkPhone is None:
        type = "WA" if "type" not in data else type
        otp = generate_otp(phone, type)

        if(otp is True):
            return jsonify({"status" : "success","message": "OTP berhasil dikirim"}), 200 
        else:
            return jsonify({"status" : "failed","message": "OTP gagal dikirim"}), 400 
    else:
        return jsonify({"status" : "failed","message": "No.HP sudah terdaftar, silahkan login atau gunakan No.HP lain."}), 202
    
@user_bp.route('/users/otp', methods=['POST'])
def verifyOtp():
    auth = request.authorization

    if not auth or not auth.token:
        return jsonify({"status" : "failed",'message': 'Akses ditolak'}), 400
    
    result = decode(auth.token)
    result = result.split(regis_delimiter)

    if len(result) != 2:
        return jsonify({"status" : "failed",'message': 'Akses ditolak'}), 400
    
    data = request.get_json()
    phone = result[0]
    otp = result[1]
    
    getOtp = otp_model.check_otp(phone)
       
    if getOtp is not None:
        otp = checkOtp(otp, phone)
        if(otp is True):
            if not data or 'flag' not in data:
                return jsonify({"status" : "failed",'message': 'Akses ditolak'}), 400

            flag = str(data.get('flag')) # new_register || register_phone
            checkPhone = user_model.checkPhoneRegistered(phone)
            if checkPhone is None:
                otp_model.delete_otp(phone)
                if flag == "new_user":
                    UniqueID = generate_uniqueid()
                    user_model.create_user_by_phone(phone, UniqueID, 1)
                    token = generate_token(UniqueID)
                    oauth = auth_model.check_uniqueID(UniqueID)
                    if oauth is True :
                        update_oauth(UniqueID, token, "")
                    else : 
                        insert_oauth(UniqueID,token, "")
                    result = encode(UniqueID)
                    data = {
                        "id" : result,
                        "token" : token
                    }
                    response = {
                        "status": "success",
                        "message": "Kode OTP sesuai",
                        "data": data
                    }
                    return jsonify(response), 200
                elif flag == "register_phone":
                    response = {
                    "status" : "success",
                    "message" : "Kode OTP sesuai"
                    }
                    return jsonify(response), 200
                else:
                    return jsonify({"status" : "failed",'message': 'Akses ditolak'}), 400
            else:
                response = {
                    "status" : "success",
                    "message" : "Kode OTP sesuai"
                }
                return jsonify(response), 200
        else:
            response = {
                    "status" : "failed",
                    "message" : "Kode OTP tidak sesuai"
                }
            return jsonify(response), 400
    else:
        response = {
                    "status" : "failed",
                    "message" : "Kode OTP tidak sesuai"
                }
        return jsonify(response), 400

# Untuk Update Nama User Setelah Registrasi
@user_bp.route('/users/set_profile', methods=['PUT'])
def set_profile():

    auth = request.authorization

    if not auth or not auth.token:
        return jsonify({'message': 'Akses ditolak'}), 400

    result = decode(auth.token)

    result = result.split(regis_delimiter)
    if len(result) != 2:
        return jsonify({'message': 'Akses ditolak'}), 400

    uniqueid = decode(result[0])
    userdata = user_model.getUserByUniqueID(uniqueid)
    data = request.get_json()
    name = str(data.get('name')) 
    phone = ''
    email = ''

    if userdata is None:
        return jsonify({'message': 'Akses ditolak'}), 400  
    else:
        phone = userdata[6]     
        email = userdata[3]  
          
    if not data or 'name' not in data:
        return jsonify({"status" : "failed","message": "Data tidak lengkap"}), 202

    setProfile = user_model.setProfile(uniqueid, name, email,phone,1)
    if (setProfile is True):
        return jsonify({"status" : "success","message": "Set nama berhasil"}), 200
    else:
        return jsonify({"status" : "failed","message": "Set nama gagal"}), 400

    

# Untuk Set PIN
@user_bp.route('/users/set_pin', methods=['POST'])
def set_pin():
    auth = request.authorization

    if not auth or not auth.token:
        return jsonify({'message': 'Akses ditolak'}), 400

    result = decode(auth.token)

    result = result.split(':')
    if len(result) != 2:
        return jsonify({'message': 'Akses ditolak'}), 400

    uniqueid = decode(result[0])
    getPhone = user_model.getUserByUniqueID(uniqueid)[5]
    getOtp = otp_model.check_request_exist(getPhone)
    if getOtp is None :
        pin = result[1]    
        if len(pin) != 6 or not pin.isdigit():
            return jsonify({"status" : "failed","message": "Akses ditolak"}), 400
        
        checkUser = user_model.getUserByUniqueID(uniqueid)
        if len(checkUser) == 0:
            return jsonify({"status" : "failed","message": "PIN gagal disimpan"}), 400
        else:
            user_model.updatePin(uniqueid, bcrypt.hashpw(pin.encode('utf-8'), SALT_KEY))
            return jsonify({"status" : "success","message": "PIN berhasil disimpan"}), 200    
    else :
        return jsonify({"status" : "failed","message": "Akses ditolak"}), 400

# Untuk Update PIN
# @user_bp.route('/users/update_pin', methods=['PUT'])
# def update_pin():
#     auth = request.authorization

#     if not auth or not auth.token:
#         return jsonify({'message': 'Akses ditolak'}), 400

#     result = decode(auth.token)

#     result = result.split(':')
#     if len(result) != 2:
#         return jsonify({'message': 'Akses ditolak'}), 400

#     uniqueid = decode(result[0])
#     pin = result[1]    
#     if len(pin) != 6 or not pin.isdigit():
#         return jsonify({"status" : "failed","message": "Akses ditolak"}), 400
    
#     checkUser = user_model.getUserByUniqueID(uniqueid)
#     if len(checkUser) == 0:
#         return jsonify({"status" : "failed","message": "PIN gagal disimpan"}), 400
#     else:
#         user_model.updatePin(uniqueid, bcrypt.hashpw(pin.encode('utf-8'), SALT_KEY))
#         return jsonify({"status" : "success","message": "PIN berhasil disimpan"}), 200    
            
# Delete User menggunakan Soft Delete
@user_bp.route('/users/<int:user_id>', methods=['DELETE'])
def delete_user(user_id):
    user = user_model.get_user_by_id(user_id)
    if user:
        user_model.delete_user(user_id)
        return jsonify({"status" : "success","message": "Menghapus pengguna berhasil"})
    return jsonify({"status" : "failed","message": "Pengguna tidak ditemukan"}), 303

@user_bp.route('/users/set_phone', methods=['PUT'])
def set_phone():
    auth = request.authorization

    if not auth or not auth.token:
        return jsonify({'message': 'Akses ditolak'}), 400

    result = decode(auth.token)
    result = result.split(regis_delimiter)

    if len(result) != 2:
        return jsonify({'message': 'Akses ditolak'}), 400

    uniqueid = decode(result[0])
    email = result[1]

    checkEmail = user_model.getUserByUniqueID(uniqueid)

    if checkEmail is None or checkEmail[3] != email:
        return jsonify({'message': 'Akses ditolak'}), 400 
   
    data = request.get_json()
    phone = str(data.get('phone'))

    type = "WA" if "type" not in data else type
    otp = generate_otp(phone, type)

    if(otp is True):
        return jsonify({"status" : "success","message": "OTP berhasil dikirim"}), 200 
    else:
        return jsonify({"status" : "failed","message": "OTP gagal dikirim"}), 400 

@user_bp.route('/users/update_phone', methods=['PUT'])
def update_phone():
    auth = request.authorization

    if not auth or not auth.token:
        return jsonify({'message': 'Invalid credentials'}), 401
    
    result = decode(auth.token)
    result = result.split(regis_delimiter)

    if len(result) != 2:
        return jsonify({'message': 'Akses ditolak'}), 400

    uniqueid = decode(result[0])
    phone = result[1]

    userdata = user_model.getUserByUniqueID(uniqueid)
    
    if userdata is None:
        return jsonify({'message': 'Akses ditolak'}), 400
    else:
        name = userdata[2]
        email = userdata[3]
        phone = phone if phone is not None else userdata[6]
        active = userdata[8]

        setProfile = user_model.setProfile(uniqueid, name, email, phone, active)
        if (setProfile is True):
            return jsonify({"status" : "success","message": "Set profile berhasil"}), 200
        else:
            return jsonify({"status" : "failed","message": "Set profile gagal"}), 400

@user_bp.route('/users/set_email', methods=['PUT'])
def set_email():
    data = request.get_json()
    email = str(data.get('email'))

    if is_valid_email(email):
        if send_otp_email(email):
            return jsonify({"status" : "success","message": "Lakukan verifikasi email anda"}), 200
        else:
            return jsonify({"status" : "success","message": "Gagal mengirimkan verifikasi ke email anda. Silahkan hubungi admin"}), 202
    else:
        return jsonify({"status" : "failed","message": "Format Email Salah"}), 400
    
@user_bp.route('/users/otp_email', methods=['POST'])
def verifyOtpEmail():
    auth = request.authorization

    if not auth or not auth.token:
        return jsonify({"status" : "failed",'message': 'Akses ditolak'}), 400
    
    result = decode(auth.token)
    result = result.split(regis_delimiter)

    if len(result) != 3:
        return jsonify({"status" : "failed",'message': 'Akses ditolak'}), 400
    
    data = request.get_json()
    email = result[0]
    otp = result[1]
    uniqueid = result[2]
    
    getOtp = otp_model.check_otp(email)
       
    if getOtp is not None:
        otp = checkOtp(otp, email)
        if(otp is True):
            if not data or 'flag' not in data:
                return jsonify({"status" : "failed",'message': 'Akses ditolak'}), 400

            checkPhone = user_model.checkPhoneRegistered(email)
            if checkPhone is None:
                otp_model.delete_otp(email)
                userdata = user_model.getUserByUniqueID(uniqueid)
                if userdata is None:
                    return jsonify({'message': 'Akses ditolak'}), 400
                else:
                    name = userdata[2]
                    email = result[0]
                    phone = phone if phone is not None else userdata[6]
                    active = userdata[8]

                    setProfile = user_model.setProfile(uniqueid, name, email, phone, active)
                    if (setProfile is True):
                        return jsonify({"status" : "success","message": "Set profile berhasil"}), 200
                    else:
                        return jsonify({"status" : "failed","message": "Set profile gagal"}), 400
            else:
                response = {
                    "status" : "success",
                    "message" : "Kode OTP sesuai"
                }
                return jsonify(response), 200
        else:
            response = {
                    "status" : "failed",
                    "message" : "Kode OTP tidak sesuai"
                }
            return jsonify(response), 400
    else:
        response = {
                    "status" : "failed",
                    "message" : "Kode OTP tidak sesuai"
                }
        return jsonify(response), 400
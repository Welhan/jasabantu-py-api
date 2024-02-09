from flask import Blueprint, jsonify, request
from models.userModels import User
from models.otpModels import Otp
import random
from config.constants import WA_ENGINE, SECRET_KEY, SALT_KEY
from helpers.helpers import checkPin, generate_otp, checkOtp, generate_token, insert_oauth
from cryptography.fernet import Fernet
import json

import jwt
import requests
import time
import bcrypt
import base64


user_bp = Blueprint('user_bp', __name__)
user_model = User()
otp_model = Otp()
# key = b'010203'  # Ganti your_key_here dengan kunci Anda
    # key = Fernet.generate_key()

@user_bp.route('/users', methods=['GET'])
def get_users():
    number_to_encrypt = 256490
    # Ubah angka menjadi string sebelum dienkripsi
    data_to_encrypt = str(number_to_encrypt)
    
    key = b'01020304050607080910111213141516'
    key = base64.urlsafe_b64encode(key)

    print("New key:", key)
    cipher_suite = Fernet(key)
    
    # Lakukan enkripsi angka
    encrypted_data = cipher_suite.encrypt(data_to_encrypt.encode())
    
    # Buat objek JSON yang sesuai
    response = {
        "data" : encrypted_data.decode()  # Mengubah bytes menjadi string
    }
    
    # Mengembalikan response dalam bentuk JSON
    return json.dumps(response), 200
@user_bp.route('/users/<int:user_id>', methods=['GET'])
def get_user(user_id):
    user = user_model.get_user_by_id(user_id)
    if user:
        return jsonify({'user': user})
    return jsonify({"status" : "failed",'message': 'Pengguna tidak ditemukan'}), 404

@user_bp.route('/check_phone', methods=['POST'])
def check_phone():
    data = request.get_json()
    phone = str(data.get('phone'))
    print(phone)
    
    if not data or 'phone' not in data:
        return jsonify({"status" : "failed","message": "Data tidak lengkap"}), 400

    checkPhone = user_model.checkPhoneRegistered(phone)
    if checkPhone is None:
        return jsonify({"status" : "success","message": "Lanjutkan Registrasi"}), 200 
    else:
        return jsonify({"status" : "failed","message": "No.HP sudah terdaftar, silahkan login atau gunakan No.HP lain."}), 303 
    
@user_bp.route('/new_users', methods=['POST'])
def create_user():
    data = request.get_json()
    phone = str(data.get('phone'))
    type = str(data.get('type'))
    
    if not data or 'type' not in data or 'phone' not in data:
        return jsonify({"status" : "failed","message": "Data tidak lengkap"}), 400

    checkPhone = user_model.checkPhoneRegistered(phone)
    if checkPhone is None:
        otp = generate_otp(phone, type)
        if(otp is True):
            return jsonify({"status" : "success","message": "OTP berhasil dikirim"}), 200 
        else:
            return jsonify({"status" : "failed","message": "OTP gagal dikirim"}), 303 
    else:
        return jsonify({"status" : "failed","message": "No.HP sudah terdaftar, silahkan login atau gunakan No.HP lain."}), 303 


@user_bp.route('/users/otp', methods=['POST'])
def verifyOtp():
    data = request.get_json()
    if not data or 'phone' not in data or 'otp' not in data:
        return jsonify({'message': 'Akses ditolak'}), 400
    
    phone = str(data.get('phone'))
    otp = data.get('otp')
    getOtp = otp_model.check_otp(phone)    
    if getOtp is not None:
        otp = checkOtp(otp, phone)
        if(otp is True):
            checkPhone = user_model.checkPhoneRegistered(phone)
            if checkPhone is None:
                createUser = user_model.create_user_by_phone(phone)
                # otp_model.delete_otp(phone)
                UniqueID = str(random.randint(10000,99999)) + str(createUser)
                user_model.updateUniqueID(UniqueID, phone)
                
                token = generate_token(UniqueID)

                insert_oauth(UniqueID,token, "")

                data = {
                    "id" : UniqueID,
                    "token" : token
                }
                # key = Fernet.generate_key()
                # cipher_suite = Fernet(key)
                response = {
                    "status": "success",
                    "message": "Kode OTP sesuai",
                    "data": data
                }
                # json_data = json.dumps(response)
                # encrypted_data = cipher_suite.encrypt(json_data.encode())
                # key_string = key.decode()
                # encrypted_json = {
                #     "data": encrypted_data.decode(), 
                #     "key": key_string
                # }
                # encrypted_json_string = json.dumps(encrypted_json)
                return jsonify(response), 200
            else:
                UniqueID = user_model.getUserByPhone(phone)[1]
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
            return jsonify(response), 303
    else:
        response = {
                    "status" : "failed",
                    "message" : "Kode OTP tidak sesuai"
                }
        return jsonify(response), 303

# Untuk Update Nama User Setelah Registrasi
@user_bp.route('/users/set_profile', methods=['POST'])
def set_profile():
    data = request.get_json()
    uniqueid = str(data.get('uniqueid'))
    name = str(data.get('name'))

    if not data or 'name' not in data or 'uniqueid' not in data:
        return jsonify({"message": "Akses ditolak"}), 400
    setProfile = user_model.setProfile(uniqueid, name)
    if (setProfile is True):
        return jsonify({"status" : "success","message": "Pendaftaran berhasil"}), 200
    else:
        return jsonify({"status" : "failed","message": "Pendaftaran gagal"}), 303

# Untuk Set PIN
@user_bp.route('/users/set_pin', methods=['POST'])
def set_pin():
    data = request.get_json()
    uniqueid = data.get('uniqueid')
    pin = str(data.get('pin'))

    if not data or 'uniqueid' not in data or 'pin' not in data:
        return jsonify({"status" : "failed","message": "Akses ditolak"}), 400
    
    if len(pin) != 60:
        return jsonify({"status" : "failed","message": "Akses ditolak"}), 400
    checkUser = user_model.getUserByUniqueID(uniqueid)
    if len(checkUser) == 0:
        return jsonify({"status" : "failed","message": "PIN gagal disimpan"}), 400
    else:
        user_model.updatePin(uniqueid, pin)
        return jsonify({"status" : "success","message": "PIN berhasil disimpan"}), 200    


# Untuk Update PIN
@user_bp.route('/users/update_pin', methods=['POST'])
def update_pin():
    data = request.get_json()
    uniqueid = data.get('uniqueid')
    pin = str(data.get('pin'))

    if not data or 'uniqueid' not in data or 'pin' not in data:
        return jsonify({"status" : "failed","message": "Akses ditolak"}), 400
    
    if len(pin) != 60:
        return jsonify({"status" : "failed","message": "Akses ditolak"}), 400
    
    getUser = user_model.getUserByUniqueID(uniqueid)

    if getUser is None:
        return jsonify({"status" : "failed","message": "Akses ditolak"}), 400
    else :
        user_model.updatePin(getUser[0], pin)
        return jsonify({"status" : "success","message": "PIN berhasil disimpan"}), 200
            

@user_bp.route('/users/<int:user_id>', methods=['DELETE'])
def delete_user(user_id):
    user = user_model.get_user_by_id(user_id)
    if user:
        user_model.delete_user(user_id)
        return jsonify({"status" : "success","message": "Menghapus pengguna berhasil"})
    return jsonify({"status" : "failed","message": "Pengguna tidak ditemukan"}), 303


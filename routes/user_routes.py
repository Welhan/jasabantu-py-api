from flask import Blueprint, Response, jsonify, request
from models.userModels import User
from models.otpModels import Otp
from models.mitraModels import Mitra
from config.constants import WA_ENGINE, SECRET_KEY, SALT_KEY
from helpers.helpers import *
import bcrypt
import base64
# import random
# import json
# import jwt
# import requests
# import time


user_bp = Blueprint('user_bp', __name__)
user_model = User()
otp_model = Otp()
mitra_model = Mitra()
regis_delimiter = ":"

# Untuk Contoh Auzthorization (nnt hapus)
@user_bp.route('/user_token', methods = ['POST'])
def user_token():
    auth = request.authorization

    if not auth or not auth.token:
        return jsonify({'message': 'Invalid credentials'}), 401
    
    token = generate_decode(auth.token)

    result = token. split(':')

    data = {
        "uniqueID" : result[0],
        # 'name' : result[1]
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

@user_bp.route('/getUniqueID', methods=['GET'])
def getUniqueID():
    data = {
        "UniqueID" : generate_uniqueid()
    }
    response = {
        "status": "success",
        "data" : data
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

# Untuk Contoh ROT 
@user_bp.route('/checkROT', methods=['POST'])
def checkROT():
    # data = request.get_json()
    uniqueID = 123451
    name = "Welhan"
    phone = "6281296023051"

    hasil = str(uniqueID) + ":" + name + ":" + phone
    rotprocess = rot(hasil)
    unrotprocess = unrot(rotprocess)
    print(rotprocess, unrotprocess)
    result1 = base64.b64encode(rotprocess.encode()).decode()
    result2 = base64.b64encode(unrotprocess.encode()).decode()
    result3 = base64.b64decode(result1).decode()
    result3 = unrot(result3)
    print(result1, result2)
    response = {
        "1": hasil,
        "2": result1,
        "3": result2,
        "4" : result3
    }
    print (response)
    return jsonify(response), 200

# Keperluan Test ROT dan Encode
@user_bp.route('/test_rot', methods=['POST'])
def test_rot():
    data = request.get_json()
    phone = str(data.get('phone'))
    otp = str(data.get('otp'))

    if not data or 'phone' not in data and 'otp' not in data:
        return jsonify({"status" : "failed","message": "Akses ditolak"}), 400
    res = phone + ":"+ otp

    res = rot(res)

    result = generate_encode(res)
    # result = res
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

    result = generate_decode(auth.token)

    result = result.split(':')
    if len(result) != 2:
        return jsonify({"status" : "failed",'message': 'Akses ditolak'}), 400
    
    phone = result[0]
    otp = result[1]
    
    getOtp = otp_model.check_otp(phone)    
    if getOtp is not None:
        otp = checkOtp(otp, phone)
        if(otp is True):
            checkPhone = user_model.checkPhoneRegistered(phone)
            if checkPhone is None:
                otp_model.delete_otp(phone)
                UniqueID = generate_uniqueid()
                user_model.create_user_by_phone(phone, UniqueID)
                token = generate_token(UniqueID)

                insert_oauth(UniqueID,token, "") #pisah

                result = generate_encode(UniqueID)

                print(result)

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
            else:
                # verify otp untuk login
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

    result = generate_decode(auth.token)

    result = result.split(':')
    if len(result) != 2:
        return jsonify({'message': 'Akses ditolak'}), 400

    uniqueid = generate_decode(result[0])
    # name = result[1]

    data = request.get_json()
    name = str(data.get('name'))

    if not data or 'name' not in data:
        return jsonify({"status" : "failed","message": "Data tidak lengkap"}), 202

    setProfile = user_model.setProfile(uniqueid, name)
    if (setProfile is True):
        return jsonify({"status" : "success","message": "Pendaftaran berhasil"}), 200
    else:
        return jsonify({"status" : "failed","message": "Pendaftaran gagal"}), 400

# Untuk Set PIN
@user_bp.route('/users/set_pin', methods=['POST'])
def set_pin():
    auth = request.authorization

    if not auth or not auth.token:
        return jsonify({'message': 'Akses ditolak'}), 400

    result = generate_decode(auth.token)

    result = result.split(':')
    if len(result) != 2:
        return jsonify({'message': 'Akses ditolak'}), 400

    uniqueid = generate_decode(result[0])
    pin = result[1]
    
    if len(pin) != 6 or not pin.isdigit():
        return jsonify({"status" : "failed","message": "Akses ditolak"}), 400
    
    checkUser = user_model.getUserByUniqueID(uniqueid)
    if len(checkUser) == 0:
        return jsonify({"status" : "failed","message": "PIN gagal disimpan"}), 400
    else:
        user_model.updatePin(uniqueid, bcrypt.hashpw(pin.encode('utf-8'), SALT_KEY))
        return jsonify({"status" : "success","message": "PIN berhasil disimpan"}), 200    

# Untuk Update PIN
@user_bp.route('/users/update_pin', methods=['PUT'])
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
            
# Delete User menggunakan Soft Delete
@user_bp.route('/users/<int:user_id>', methods=['DELETE'])
def delete_user(user_id):
    user = user_model.get_user_by_id(user_id)
    if user:
        user_model.delete_user(user_id)
        return jsonify({"status" : "success","message": "Menghapus pengguna berhasil"})
    return jsonify({"status" : "failed","message": "Pengguna tidak ditemukan"}), 303




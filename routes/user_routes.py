from flask import Blueprint, jsonify, request
from models.userModels import User
from models.otpModels import Otp
import random
from config.constants import WA_ENGINE, SECRET_KEY
from helpers.helpers import checkPin, generate_otp
import requests
import time
import bcrypt
import random

user_bp = Blueprint('user_bp', __name__)
user_model = User()
otp_model = Otp()

@user_bp.route('/users', methods=['GET'])
def get_users():
    users = user_model.get_users()
    return jsonify({'users': users})

@user_bp.route('/users/<int:user_id>', methods=['GET'])
def get_user(user_id):
    user = user_model.get_user_by_id(user_id)
    if user:
        return jsonify({'user': user})
    return jsonify({"status" : "failed",'message': 'Pengguna tidak ditemukan'}), 404

@user_bp.route('/new_users', methods=['POST'])
def create_user():
    data = request.get_json()
    phone = str(data.get('phone'))
    type = str(data.get('type'))
    
    if not data or 'type' not in data or 'phone' not in data:
        return jsonify({"status" : "failed","message": "Data tidak lengkap"}), 400

    checkPhone = user_model.checkPhoneRegistered(phone)
    if checkPhone is None:
        otp = generate_otp()
        # otp = generate_otp()
        # user_model.create_user(name, username, phone)

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
                    otp_model.create_otp(phone, bcrypt.hashpw(generate_otp().encode('utf-8'),bcrypt.gensalt()), count + 1)
                else:
                    otp_model.update_otp(phone, bcrypt.hashpw(generate_otp().encode('utf-8'),bcrypt.gensalt()), count + 1)
                return jsonify({"status" : "success","message" : 'Login sukses'}), 200
            else:
                return jsonify({"status" : "failed","message": "Terjadi kesalahan, mohon coba lagi nanti."}), 422
        else: 
            return jsonify({"status" : "failed","message": "Terjadi kesalahan, mohon coba lagi nanti."}), 422
    else:
        return jsonify({"status" : "failed","message": "No.HP sudah terdaftar, silahkan login atau gunakan No.HP lain."}), 303 
    

# Untuk check PIN
@user_bp.route('/users/check_pin', methods=['POST'])
def check_pin():
    data = request.get_json()
    pin = str(data.get('pin'))
    uniqueid = str(data.get('uniqueid'))

    getPin = user_model.getUserByUniqueID(uniqueid)
    if bcrypt.checkpw(pin, getPin[4]):
        checkPin = checkPin(pin)
        if checkPin is False:
            return jsonify({"status" : "failed","message": "Akses ditolak"}), 400
        else:
            return jsonify({"status" : "success","message": "PIN cocok"}), 200
    else:
        return jsonify({"status" : "failed","message": "Akses ditolak"}), 400

# Untuk check OTP
@user_bp.route('/users/check_otp', methods=['POST'])
def check_otp():
    data = request.get_json()
    otp = str(data.get('otp'))
    phone = str(data.get('phone'))

    getOtp = otp_model.check_otp(phone)
    if bcrypt.checkpw(otp, getOtp[1]):
        checkOtp = checkOtp(otp)
        if checkPin is False:
            return jsonify({"status" : "failed","message": "Akses ditolak"}), 400
        else:
            return jsonify({"status" : "success","message": "PIN cocok"}), 200
    else:
        return jsonify({"status" : "failed","message": "Akses ditolak"}), 400


@user_bp.route('/users/otp', methods=['POST'])
def verifyOtp():
    data = request.get_json()
    phone = str(data.get('phone'))
    otp = str(data.get('otp'))
    if not data or 'phone' not in data or 'otp' not in data:
        return jsonify({'message': 'Akses ditolak'}), 400
    
    getOtp = otp_model.check_otp(phone)
    if getOtp is not None:
        if bcrypt.checkpw(otp, getOtp[1]):
        # if otp == getOtp[1]:
            checkPhone = user_model.checkPhoneRegistered(phone)
            if checkPhone is None:
                createUser = user_model.create_user(phone)
                otp_model.delete_otp(phone)
                uniqueID = random.randint(10000,99999)
                UniqueID = str(uniqueID) + createUser
                user_model.updateUniqueID(UniqueID)
                return jsonify({"status" : "success","message": "Pendaftaran berhasil"}), 200
            else:
                return jsonify({"status" : "failed","message": "No.HP sudah terdaftar, silahkan login atau gunakan No.HP lain."}), 303 
        else:
            return jsonify({"status" : "failed","message": "Kode OTP tidak sesuai"}), 303
    else:
        return jsonify({"status" : "failed","message": "Kode OTP tidak sesuai"}), 303

# Untuk Update Nama User Setelah Registrasi
@user_bp.route('/users/update_profile', methods=['POST'])
def profile_update():
    data = request.get_json()
    name = str(data.get('name'))
    phone = str(data.get('phone'))

    if not data or 'name' not in data or 'phone' not in data:
        return jsonify({"message": "Akses ditolak"}), 400
    
    
    

# Untuk Set PIN
@user_bp.route('/users/set_pin', methods=['POST'])
def set_pin():
    data = request.get_json()
    username = str(data.get('username'))
    pin = str(data.get('pin'))

    if not data or 'username' not in data or 'phone' not in data:
        return jsonify({"status" : "failed","message": "Akses ditolak"}), 400
    
    if len(pin) != 60:
        return jsonify({"status" : "failed","message": "Akses ditolak"}), 400
    
    checkUsername = user_model.checkUsername(username)

    if checkUsername is None:
        return jsonify({"status" : "failed","message": "Akses ditolak"}), 400
    else :
        checkPhone = user_model.getUserByUniqueID(checkUsername[1])
        if checkPhone is None :
            return jsonify({"status" : "failed","message": "Akses ditolak"}), 400
        else:
            user_model.updatePin(checkPhone[0], pin)
            return jsonify({"status" : "success","message": "PIN berhasil disimpan"}), 400    






# Untuk Update PIN
@user_bp.route('/users/update_pin', methods=['POST'])
def update_pin():
    data = request.get_json()
    uniqueid = str(data.get('uniqueid'))
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


    username@awddf72

    uniqueID

    uname#mjb

    uname#mjb
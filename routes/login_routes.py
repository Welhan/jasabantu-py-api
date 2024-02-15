from flask import Blueprint, jsonify, request
from models.userModels import User
from models.otpModels import Otp
from models.mitraModels import Mitra
import random
import bcrypt
from helpers.helpers import *


login_bp = Blueprint('login_bp', __name__)
user_model = User()
mitra_model = Mitra()
otp_model = Otp()
login_delimiter = ":"

@login_bp.route('/mitraLoginByEmail', methods=['POST'])
def mitraLoginByEmail():
    data = request.get_json()
    email = data.get('email')
    if not data and 'email' not in data:
        return jsonify({"status" : "failed","message": "Akses ditolak"}), 400
    
    checkLogin = mitra_model.getMitraLoginByEmail(email)

    if checkLogin is None:
        return jsonify({"status":'failed','message': 'Email tidak ditemukan!'}), 303
    else:
        return jsonify({"status" : "success","message": "Email ditemukan"}), 200 
    
@login_bp.route('/mitraLoginByPhone', methods=['POST'])
def mitraLoginByPhone():
    data = request.get_json()
    phone = data.get('phone')
    if not data and 'phone' not in data:
        return jsonify({"status" : "failed","message": "Akses ditolak"}), 400
    
    checkLogin = mitra_model.getMitraLoginByPhone(phone)

    if checkLogin is None:
        return jsonify({"status":'failed','message': 'Phone tidak ditemukan!'}), 303
    else:
        return jsonify({"status" : "success","message": "Phone ditemukan"}), 200 
    

@login_bp.route('/checkEmail', methods=['POST'])
def checkEmail():
    data = request.get_json()
    email = data.get('email')

    res = is_valid_email(email)
    print(res)
    return jsonify({"status" : "success","message": res}), 200 


@login_bp.route('/loginUser', methods=['POST'])
def loginByUser():
    data = request.get_json()
    user = data.get('user')
    type = str(data.get('type'))
    process = 3

    if not data or 'user' not in data:
        return jsonify({"status":'failed','message': 'Kolom wajib diisi.'}), 202
    
    if user.isdigit():
        checkRegistered = user_model.checkPhoneRegistered(user)
    elif is_valid_email(user) :
        checkRegistered =user_model.getUserByEmail(user)
    else:
        return jsonify({"status":'failed','message': 'Data pengguna tidak ditemukan'}), 202

    if checkRegistered is None:
        return jsonify({"status":'failed','message': 'Data pengguna tidak ditemukan'}), 202
    else: 
        if user.isdigit():   
            type = "WA" if "type" not in data else type
            otp = generate_otp(user, type)

            # tambah var process 1 = belum set name, 2 = belum set pin, 3 sudah semua

            if(otp is True):
                return jsonify({"status" : "success","message": "OTP berhasil dikirim", "process" : process}), 200 
            else:
                return jsonify({"status" : "failed","message": "OTP gagal dikirim"}), 202 
        elif is_valid_email(user) :
            return jsonify({"status" : "success","message": "Berhasil masuk!"}), 200 
        else:
            return jsonify({"status":'failed','message': 'Akses ditolak!'}), 202
        
        
    
@login_bp.route('/loginPinUser', methods=['POST'])
def loginPinUser():
    auth = request.authorization

    if not auth or not auth.token:
        return jsonify({'message': 'Akses ditolak'}), 202

    result = generate_decode(auth.token)

    result = result.split(login_delimiter)
    if len(result) != 2:
        return jsonify({'message': 'Akses Ditolak'}), 202
    
    user = result[0]
    pin = result[1]

    pinCheck = checkPin(user, pin)
    if(pinCheck is True):
        if(user.isalpha()):
            UniqueID = user_model.getUserByEmail(user)
        elif(user.isdigit()):
            UniqueID = user_model.getUserByPhone(user)

        data = {
            "id" : generate_encode(UniqueID[1]),
            "name" : UniqueID[2],
            "phone" : generate_encode(UniqueID[5])
        }
       
        return jsonify({"status" : "success","message" : 'PIN cocok', "data" : data}), 200
    else:
        return jsonify({"status" : "failed","message": "Akses ditolak"}), 202
    
@login_bp.route('/loginPinMitra', methods=['POST'])
def loginPinMitra():
    data = request.get_json()
    phone = data.get('phone')
    email = data.get('email')
    pin = data.get('pin')

    if not data and ('email' not in data or 'phone' not in data) and len(pin) != 60:
        return jsonify({"status" : "failed","message": "Akses ditolak"}), 400

    pinCheck = checkPin(phone,email,'', pin)
    if(pinCheck is True):
        if(email is not None):
            UniqueID = mitra_model.getMitraLoginByEmail(email)
        elif(phone is not None):
            UniqueID = mitra_model.getMitraLoginByPhone(phone)
        return jsonify({"status" : "success","message" : 'PIN cocok', "data" : UniqueID}), 200
    else:
        return jsonify({"status" : "failed","message": "Akses ditolak"}), 400

    

@login_bp.route('/loginByEmail', methods=['POST'])
def loginByEmail():
    data = request.get_json()
    email = data.get('email')
    cekEmail = user_model.getUserByEmail(email)

    if cekEmail is None:
        createUser = user_model.create_user_by_email(email)
        UniqueID = random.randint(10000,99999)
        UniqueID = str(UniqueID)
        UniqueID = UniqueID + str(createUser)
        user_model.updateUniqueID(UniqueID, '', email)
        return jsonify({"status" : "success","message": "Pendaftaran berhasil", "data" : UniqueID}), 200
    else:
        return jsonify({"status" : "success","message": "Email sudah terdaftar"}), 200







from flask import Blueprint, jsonify, request
from models.userModels import User
from models.otpModels import Otp
from models.mitraModels import Mitra
from models.authModels import Auth
import random
import bcrypt
from helpers.helpers import *

auth_bp = Blueprint('auth_bp', __name__)
user_model = User()
mitra_model = Mitra()
otp_model = Otp()
auth_model = Auth()
login_delimiter = ":"

@auth_bp.route('/checkApiStatus', methods=['GET'])
def checkStatus():
    return jsonify({"status" : True}), 200

@auth_bp.route('/mitraLoginByEmail', methods=['POST'])
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
    
@auth_bp.route('/mitraLoginByPhone', methods=['POST'])
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
    

@auth_bp.route('/checkEmail', methods=['POST'])
def checkEmail():
    data = request.get_json()
    email = data.get('email')

    res = is_valid_email(email)
    return jsonify({"status" : "success","message": res}), 200 


@auth_bp.route('/loginUser', methods=['POST'])
def loginByUser():
    data = request.get_json()
    user = data.get('user')
    type = str(data.get('type'))
    process = 3

    if not data or 'user' not in data:
        return jsonify({"status":'failed','message': 'Kolom wajib diisi.'}), 202
    
    if user.isdigit():
        checkRegistered = user_model.getUserByPhone(user)
    elif is_valid_email(user) :
        checkRegistered = user_model.getUserByEmail(user)
        if checkRegistered is None:
            createUser = user_model.create_user_by_email(user)
            UniqueID = random.randint(10000,99999)
            UniqueID = str(UniqueID)
            UniqueID = UniqueID + str(createUser)
            user_model.updateUniqueID(UniqueID, '', user)
            return jsonify({"status" : "success","message": "Pendaftaran berhasil", "data" : encode(UniqueID)}), 200
        else:
            uniqueID = checkRegistered[3]
    else:
        return jsonify({"status":'failed','message': 'Data pengguna tidak ditemukan'}), 202

    if checkRegistered is None:
        return jsonify({"status":'failed','message': 'Data pengguna tidak ditemukan'}), 202
    else: 
        uniqueID = checkRegistered[3]

    if checkRegistered[1] is None:
        process = 1
    elif checkRegistered[2] is None:
        process = 2

    if user.isdigit():   
        type = "WA" if "type" not in data else type
        otp = generate_otp(user, type)

        if(otp[0] is True):
            return jsonify({"status" : "success","message": "OTP berhasil dikirim", "process" : process, 'id' : encode(uniqueID), "delay": otp[1]}), 200 
        else:
            return jsonify({"status" : "failed","message": "OTP gagal dikirim"}), 202 
        
    elif is_valid_email(user) :
        return jsonify({"status" : "success","message": "Berhasil masuk!", "process" : process, 'id' : encode(uniqueID)}), 200 
    else:
        return jsonify({"status":'failed','message': 'Akses ditolak!'}), 202
      
    
@auth_bp.route('/loginPinUser', methods=['POST'])
def loginPinUser():
    auth = request.authorization

    if not auth or not auth.token:
        return jsonify({'message': 'Akses ditolak'}), 202

    result = decode(auth.token)
    result = result.split(login_delimiter)
    if len(result) != 2:
        return jsonify({'message': 'Akses Ditolak'}), 202
    
    user = result[0]
    pin = result[1]

    if(is_valid_email(user)):
        UniqueID = user_model.getUserByEmail(user)
    elif(user.isdigit()):
        UniqueID = user_model.getUserByPhone(user)
        
    if UniqueID is not None :
        uniqueID = UniqueID[3]
    else:
        return jsonify({"status" : "failed","message": "Akses ditolak!"}), 202

    pinCheck = checkPin(user, pin)
    if(pinCheck is True):
        token = generate_token(uniqueID)
        insert_oauth(uniqueID, token, "")

        data = {
            "id" : encode(UniqueID[1]),
            "name" : UniqueID[2],
            "phone" : encode(UniqueID[5]),
            "token" : token
        }
       
        return jsonify({"status" : "success","message" : 'PIN cocok', "data" : data}), 200
    else:
        Counter = user_model.checkCounterPin(uniqueID)[0]
        tryPIN = 1
        if Counter is not None:
            tryPIN = int(Counter) + 1
        
        user = user_model.counterPin(uniqueID, tryPIN)
        
        Counter = 3 - tryPIN
        if Counter == 0:
            user_model.setNonActiveUser(uniqueID)
            return jsonify({"status" : "failed","message": "Akun terblokir"}), 202
        return jsonify({"status" : "failed","message": "PIN tidak sesuai, anda memiliki " + str(Counter) + " kesempatan lagi"}), 202
    
@auth_bp.route('/loginPinMitra', methods=['POST'])
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

    

@auth_bp.route('/loginByEmail', methods=['POST'])
def loginByEmail():
    data = request.get_json()
    email = data.get('email')
    cekEmail = user_model.getUserByEmail(email)

    if cekEmail is None:
        createUser = user_model.create_user_by_email(email)
        UniqueID = generate_uniqueid()
        # UniqueID = random.randint(10000,99999)
        # UniqueID = str(UniqueID)
        # UniqueID = UniqueID + str(createUser)
        user_model.updateUniqueID(UniqueID, '', email)
        return jsonify({"status" : "success","message": "Pendaftaran berhasil", "data" : UniqueID}), 200
    else:
        return jsonify({"status" : "success","message": "Email sudah terdaftar"}), 200
    
@auth_bp.route('/logout', methods=['POST'])
def logout():
    auth = request.authorization

    if not auth or not auth.token:
        return jsonify({'message': 'Akses ditolak'}), 400
    result = decode(auth.token)
    result = result.split(':')
    if len(result) != 2:
        return jsonify({"status" : "failed",'message': 'Akses ditolak'}), 400
    uniqueid = result[0]
    logout = auth_model.logout(uniqueid)
    if logout is True :
        return jsonify({"status" : "success","message": "Logout berhasil!"}), 200
    else:
        return jsonify({"status" : "success","message": "Logout gagal"}), 202






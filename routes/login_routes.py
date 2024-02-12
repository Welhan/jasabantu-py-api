from flask import Blueprint, jsonify, request
from models.userModels import User
from models.otpModels import Otp
from models.mitraModels import Mitra
import random
import bcrypt
from helpers.helpers import checkPin, generate_otp, checkOtp


login_bp = Blueprint('login_bp', __name__)
user_model = User()
mitra_model = Mitra()
otp_model = Otp()

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
    

@login_bp.route('/loginByPhone', methods=['POST'])
def loginByPhone():
    data = request.get_json()
    phone = data.get('phone')
    if phone is None:
        return jsonify({"status":'failed','message': 'No.HP wajib diisi.'}), 404
    
    checkRegisteredPhone = user_model.checkPhoneRegistered(phone)

    if checkRegisteredPhone is None:
        return jsonify({"status":'failed','message': 'Nomor tidak ditemukan'}), 303
    else:    
        return jsonify({"status" : "success","message": "Nomor ditemukan"}), 200 
        
    
@login_bp.route('/loginPinUser', methods=['POST'])
def loginPinUser():
    data = request.get_json()
    phone = data.get('phone')
    email = data.get('email')
    pin = data.get('pin')

    if not data and ('email' not in data or 'phone' not in data) and len(pin) != 60:
        return jsonify({"status" : "failed","message": "Akses ditolak"}), 400

    pinCheck = checkPin(phone,email,'', pin)
    if(pinCheck is True):
        if(email is not None):
            UniqueID = user_model.getUserByEmail(email)
        elif(phone is not None):
            UniqueID = user_model.getUserByPhone(phone)
        return jsonify({"status" : "success","message" : 'PIN cocok', "data" : UniqueID}), 200
    else:
        return jsonify({"status" : "failed","message": "Akses ditolak"}), 400
    
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







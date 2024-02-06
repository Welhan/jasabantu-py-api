from flask import Blueprint, jsonify, request
from models.userModels import User
from models.otpModels import Otp
import random


from helpers.helpers import checkPin, generate_otp, checkOtp


login_bp = Blueprint('login_bp', __name__)
user_model = User()
otp_model = Otp()

@login_bp.route('/loginByPhone', methods=['POST'])
def loginByPhone():
    data = request.get_json()
    phone = data.get('phone')
    type = str(data.get('type'))
    if phone is None:
        return jsonify({"status":'failed','message': 'No.HP wajib diisi.'}), 404
    
    checkRegisteredPhone = user_model.checkPhoneRegistered(phone)

    if checkRegisteredPhone is None:
        return jsonify({"status":'failed','message': 'Nomor tidak ditemukan'}), 303
    else:    
        otp = generate_otp(phone, type)
        if(otp is True):
            return jsonify({"status" : "success","message": "OTP berhasil dikirim"}), 200 
        else:
            return jsonify({"status" : "failed","message": "OTP gagal dikirim"}), 303
        
    
@login_bp.route('/loginPin', methods=['POST'])
def loginPin():
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







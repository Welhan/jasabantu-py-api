from flask import Blueprint, jsonify, request
from models.userModels import User
import bcrypt


login_bp = Blueprint('login_bp', __name__)
user_model = User()

@login_bp.route('/loginByPhone', methods=['POST'])
def login():
    data = request.get_json()
    phone = data.get('phone')
    pin = data.get('pin')

    if phone is None:
        return jsonify({'message': 'No.HP wajib diisi.'}), 404
    
    checkRegisteredPhone = user_model.checkPhoneRegistered(phone)

    if checkRegisteredPhone is None:
        return jsonify({'message': 'Nomor tidak ditemukan'}), 200
    else:    
        getPin = user_model.checkPin(phone)
        if getPin is not None:
            if bcrypt.checkpw(pin, getPin[1]):
                data_user = user_model.getUserByPhone(phone)
                return jsonify({"status" : "success",'data': data_user,'message': 'Login berhasil.'}), 200
            else:  
                return jsonify({"status" : "failed",'message': 'PIN salah.'}), 202
        else:  
            return jsonify({"status" : "failed",'message': 'PIN salah.'}), 202   








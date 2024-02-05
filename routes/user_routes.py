from flask import Blueprint, jsonify, request
from models.userModels import User
from models.otpModels import Otp
import random
from config.constants import WA_ENGINE
import requests
import time
import bcrypt

user_bp = Blueprint('user_bp', __name__)
user_model = User()
otp_model = Otp()

def generate_otp():
    return random.randint(1,9999)

@user_bp.route('/users', methods=['GET'])
def get_users():
    users = user_model.get_users()
    return jsonify({'users': users})

@user_bp.route('/users/<int:user_id>', methods=['GET'])
def get_user(user_id):
    user = user_model.get_user_by_id(user_id)
    if user:
        return jsonify({'user': user})
    return jsonify({'message': 'User not found'}), 404

@user_bp.route('/new_users', methods=['POST'])
def create_user():
    data = request.get_json()
    username = str(data.get('username'))
    phone = str(data.get('phone'))

    if not data or 'username' not in data or 'phone' not in data:
        return jsonify({'message': 'Incomplete data provided'}), 400
    
    checkUsername = user_model.checkUsername(username)

    if checkUsername is None:
        checkPhone = user_model.checkPhoneRegistered(phone)
        if checkPhone is None:
            # otp = bcrypt.hashpw(generate_otp(),bcrypt.gensalt())
            otp = generate_otp()
            # user_model.create_user(name, username, phone)

            data = {
                "message" : "*" +str(otp)+"* adalah kode OTP untuk registrasi akun anda. Harap tidak membagikan atau memberitahukan kode ini kepada siapapun.",
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

                if delay > 86400: #jika sudah menjadi 1 hari, kembali menjadi 5 detik
                    delay = 5

            else:
                count = 0
                delay = 5

            # time.sleep(5)

            if checkOtpPhone is None:
                otp_model.create_otp(phone, otp, count + 1)
            else:
                otp_model.update_otp(phone, otp, count + 1)

            return jsonify({"message" : "OTP berhasil dikirim", "nextDelay" : delay}), 200

            response = requests.post(WA_ENGINE, data=data)

            # Memeriksa status respons
            if response.status_code == 200:
                # Data diterima dalam format JSON
                data = response.json()
                
                if checkOtpPhone is None:
                    otp_model.create_otp(phone, otp, count + 1)
                else:
                    otp_model.update_otp(phone, otp, count + 1)

                message = data["message"]
                new_message = message.replace("@c.us", "")
                return jsonify({"message" : new_message}), 200
            else:
                # Menampilkan pesan kesalahan jika permintaan tidak berhasil
                # return jsonify({"message" : })
                print("Failed to fetch data from API:", response.status_code)
        else:
            return jsonify({'message': 'Phone Already Registered'}), 303 
    else:
        return jsonify({'message': 'User Already Registered'}), 303
    
@user_bp.route('/users/otp', methods=['POST'])
def verifyOtp():
    data = request.get_json()
    name = str(data.get('name'))
    username = str(data.get('username'))
    phone = str(data.get('phone'))
    otp = str(data.get('otp'))

    if not data or 'name' not in data or 'username' not in data or 'phone' not in data or 'otp' not in data:
        return jsonify({'message': 'Access Denied'}), 400
    
    getOtp = otp_model.check_otp(phone)
    if getOtp is not None:
        # if bcrypt.checkpw(otp, getOtp[1]):
        if otp == getOtp[1]:
            checkUsername = user_model.checkUsername(username)
            checkPhone = user_model.checkPhoneRegistered(phone)
            if checkUsername is None and checkPhone is None:
                user_model.create_user(name,username,phone)
                otp_model.delete_otp(phone)
                return jsonify({'message': 'Berhasil melakukan registrasi'}), 200
            else:
                return jsonify({'message': 'User atau Phone sudah terdaftar'}), 303
        else:
            return jsonify({'message': 'Kode OTP tidak sesuai'}), 303
    else:
        return jsonify({'message': 'Kode OTP tidak sesuai'}), 303

# Untuk Update PIN
@user_bp.route('/users/update_pin', methods=['POST'])
def pin_update():
    data = request.get_json()
    username = str(data.get('username'))
    phone = str(data.get('phone'))

    if not data or 'username' not in data or 'phone' not in data:
        return jsonify({'message': 'Access Denied'}), 400
    
    checkUsername = user_model.checkUsername(username)

    if checkUsername is None:
        return jsonify({'message': 'Access Denied'}), 400
    
    

@user_bp.route('/users/<int:user_id>', methods=['DELETE'])
def delete_user(user_id):
    user = user_model.get_user_by_id(user_id)
    if user:
        user_model.delete_user(user_id)
        return jsonify({'message': 'User deleted successfully'})
    return jsonify({'message': 'User not found'}), 303

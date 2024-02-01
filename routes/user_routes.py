from flask import Blueprint, jsonify, request
from models.userModels import User
from models.otpModels import Otp
import random

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

@user_bp.route('/users', methods=['POST'])
def create_user():
    data = request.get_json()
    name = str(data.get('name'))
    username = str(data.get('username'))
    phone = str(data.get('phone'))

    if not data or 'name' not in data or 'username' not in data or 'phone' not in data:
        return jsonify({'message': 'Incomplete data provided'}), 400
    
    if not phone:
        return jsonify({'message': 'Phone is Required'}), 303
    
    checkUsername = user_model.checkUsername(username)

    if checkUsername is None:
        checkPhone = user_model.checkPhoneRegistered(phone)
        if checkPhone is None:
            otp = generate_otp()
            # user_model.create_user(name, username, phone)
            otp_model.create_otp(phone, otp)
            return jsonify({'otp': otp, 'message' : 'OTP Berhasil Digenerate'}), 200
        else:
            return jsonify({'message': 'Phone Already Registered'}), 303 
    else:
        return jsonify({'message': 'User Already Registered'}), 303
    

@user_bp.route('/users/<int:user_id>', methods=['DELETE'])
def delete_user(user_id):
    user = user_model.get_user_by_id(user_id)
    if user:
        user_model.delete_user(user_id)
        return jsonify({'message': 'User deleted successfully'})
    return jsonify({'message': 'User not found'}), 303

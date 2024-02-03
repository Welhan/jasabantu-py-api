from flask import Blueprint, jsonify, request
from models.userModels import User

login_bp = Blueprint('login_bp', __name__)
user_model = User()

@login_bp.route('/loginByPhone', methods=['POST'])
def registser():
    data = request.get_json()
    phone = data.get('phone')

    if phone is None:
        return jsonify({'message': 'Phone is Required'}), 404
    
    checkRegisteredPhone = user_model.checkPhoneRegistered(phone)

    if checkRegisteredPhone is not None:
        return jsonify({'message': 'Phone can Register'}), 200
    else:
        return jsonify({'message': 'Phone can not Register'}), 200


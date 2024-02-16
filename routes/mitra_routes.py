from flask import Blueprint, jsonify, request
from models.mitraModels import Mitra
from helpers.helpers import *

import bcrypt

mitra_model = Mitra()

mitra_bp = Blueprint('mitra_bp', __name__)

@mitra_bp.route('/getMitra', methods=['GET'])
def getMitra():    
    checkMitra = mitra_model.getMitra()
    data = []
    if checkMitra is not None :
        for row in checkMitra:
            row_dict = {
                "UniqueID": row[1],
                "Name": row[2],
                "Address": row[7],
                "CreatedDate": row[8],
            }
            data.append(row_dict)

    response = {
        "status": "success",
        "data": data
    }
    return jsonify(response), 200


@mitra_bp.route('/checkEmailMitra', methods=['POST'])
def checkEmailMitra():
    data = request.get_json()
    email = data.get('email')

    if not data and 'email' not in data:
        return jsonify({"status" : "failed","message": "Akses ditolak!"}), 400
    
    checkMitra = mitra_model.getMitraLogin(email)

    if checkMitra is None:
        return jsonify({"status":'success','message': 'Email tersedia!'}), 200
    else:
        return jsonify({"status":'failed','message': 'Email tidak tersedia!'}), 200

@mitra_bp.route('/checkPhoneMitra', methods=['POST'])
def checkPhoneMitra():
    data = request.get_json()
    phone = data.get('phone')


    
@mitra_bp.route('/registerMitra', methods=['POST'])
def registerMitra():
    auth = request.authorization
    print(auth, auth.token)
    if not auth or not auth.token:
        return jsonify({'message': 'Akses ditolak'}), 400
    dataMitra = generate_decode(auth.token)
    # data = request.get_json()
    # mitra = data.get('mitra')
    # dataMitra = generate_decode(mitra)
    dataMitra = dataMitra.split(":")
    if len(dataMitra) != 5 :
        return jsonify({"status" : "failed","message": "Registrasi mitra gagal!"}), 400
    name = dataMitra[0]
    email = dataMitra[1]
    phone = dataMitra[2]
    address = dataMitra[3]
    pin = bcrypt.hashpw(dataMitra[4].encode('utf-8'), SALT_KEY)
    uniqueid = generate_uniqueid()
    # return jsonify({"status":'success','message': dataMitra}), 200

    # if not data and 'nama' not in data and ('email' not in data or 'phone' not in data) and 'address' not in data and 'pin' not in data and 'pin' not in data:
    #     return jsonify({"status" : "failed","message": "Registrasi mitra gagal!"}), 400

    checkMitra = mitra_model.getMitraLogin(email)

    if checkMitra is None:
        checkMitra = mitra_model.registerMitra(uniqueid, name, email, phone, pin, address)    
        if checkMitra is True:
            return jsonify({"status":'success','message': 'Registrasi berhasil!'}), 200
    else:
        return jsonify({"status":'failed','message': 'Registrasi gagal!'}), 303
    
    
    





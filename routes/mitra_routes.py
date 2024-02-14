from flask import Blueprint, jsonify, request
from models.mitraModels import Mitra
from helpers.helpers import *

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
    
    
@mitra_bp.route('/registerMitra', methods=['POST'])
def registerMitra():
    data = request.get_json()
    if data.get('uniqueid') is None:
        UniqueID = generate_uniqueid()
    else:
        UniqueID = data.get('uniqueid')
    
    nama = data.get('nama')
    email = data.get('email')
    phone = data.get('phone')

    if not data and 'nama' not in data and ('email' not in data or 'phone' not in data):
        return jsonify({"status" : "failed","message": "Registrasi mitra gagal!"}), 400

    checkMitra = mitra_model.getMitraLogin(email)

    if checkMitra is None:
        checkMitra = mitra_model.registerMitra(UniqueID, nama, email, phone)    
        if checkMitra is True:
            return jsonify({"status":'success','message': 'Registrasi berhasil!'}), 200
    else:
        return jsonify({"status":'failed','message': 'Registrasi gagal!'}), 303
    
    
    





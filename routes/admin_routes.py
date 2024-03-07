from flask import Blueprint, jsonify, request
from models.adminModels import Admin
from helpers.helpers import *

import bcrypt
import base64
import requests

admin_model = Admin()

admin_bp = Blueprint('admin_bp', __name__)

admin_delimiter = "#"

@admin_bp.route('/loginAdmin', methods=['POST'])
def loginAdmin():
    auth = request.authorization
    if not auth or not auth.token:
        return jsonify({'message': 'Akses ditolak'}), 400
    dataLogin = decode(auth.token)
    dataLogin = dataLogin.split(admin_delimiter)
    if len(dataLogin) != 2 :
        return jsonify({"status" : "failed","message": "Akses ditolak"}), 400
    email = dataLogin[0]
    password = dataLogin[1]
    checkLogin = admin_model.getDataAdminByEmail(email)
    if checkLogin is not None:
        if bcrypt.checkpw(password.encode('utf-8'), checkLogin[3].encode('utf-8')) :
            updateLogin = admin_model.updateLogin(email)
            if updateLogin is True : 
                response = {
                    "status": 'success',
                    "session" : {
                        "email" : encode(email),
                        "name" : checkLogin[1]
                    },
                    "message": "Login berhasil!"
                }
                return jsonify(response), 200
            else : 
                return jsonify({"status":'failed','message': 'Login gagal!'}), 303
        else:
            return jsonify({"status":'failed','message': 'Login gagal!'}), 303
    else:
        return jsonify({"status":'failed','message': 'Login gagal!'}), 303
    

@admin_bp.route('/logoutAdmin', methods=['POST'])
def logoutAdmin():    
    auth = request.authorization
    if not auth or not auth.token:
        return jsonify({'message': 'Akses ditolak'}), 400
    email = decode(auth.token)
    checkLogin = admin_model.getDataAdminByEmail(email)
    if checkLogin is not None:
        updateLogout = admin_model.logoutAdmin(email)
        if updateLogout is True :
            return jsonify({"status":'success','message': 'Logout berhasil!'}), 200
        else:
            return jsonify({"status":'failed','message': 'Logout gagal!'}), 303
    else:
        return jsonify({"status":'failed','message': 'Logout gagal!'}), 303

@admin_bp.route('/getMitra', methods=['POST'])
def getMitra():
    auth = request.authorization
    if not auth or not auth.token:
        return jsonify({'message': 'Akses ditolak'}), 400
    email = decode(auth.token)
    checkAdmin = admin_model.getDataAdminByEmail(email)
    if checkAdmin is not None : 
        data = request.get_json()
        start = int(data.get('start'))
        length = int(data.get('length'))
        email = str(data.get('email'))
        name = str(data.get('name'))
        phone = str(data.get('phone'))
        summary = mitra_model.getTotalMitra()[0]
        checkMitra = mitra_model.getMitra(start, length, email, name, phone)
        data = []
        if checkMitra is not None :
            for row in checkMitra:
                row_dict = {
                    "UniqueID": str(row[0]),
                    "Phone": row[1],
                    "Name": row[2],
                    "Address": row[3],
                    "Email": row[4],
                    "CreatedDate": row[5],
                }
                data.append(row_dict)

        response = {
            "status": "success",
            "data": data,
            "summary": summary
        }
        return jsonify(response), 200
    else :
        return jsonify({"status" : "failed","message": "Akses ditolak"}), 400


@admin_bp.route('/checkEmailMitra', methods=['POST'])
def checkEmailMitra():
    auth = request.authorization
    if not auth or not auth.token:
        return jsonify({'message': 'Akses ditolak'}), 400
    dataMitra = decode(auth.token)
    dataMitra = dataMitra.split(admin_delimiter)
    if len(dataMitra) > 3 or len(dataMitra) < 2 :
        return jsonify({"status" : "failed","message": "Akses ditolak"}), 400
    email = dataMitra[0]
    mitraEmail = dataMitra[1]
    checkAdmin = admin_model.getDataAdminByEmail(email)
    if checkAdmin is not None : 
        checkMitra = mitra_model.getMitraLogin(mitraEmail, "")
        if len(dataMitra) == 3 :
            uniqueid = dataMitra[2]
            if checkMitra is None or checkMitra[2] == uniqueid :
                return jsonify({"status":'success','message': 'Email tersedia!'}), 200
            else:
                return jsonify({"status":'failed','message': 'Email tidak tersedia!'}), 200
        elif len(dataMitra) == 2:
            if checkMitra is None :
                return jsonify({"status":'success','message': 'Email tersedia!'}), 200
            else:
                return jsonify({"status":'failed','message': 'Email tidak tersedia!'}), 200
        else:
            return jsonify({"status":'failed','message': 'Email tidak tersedia!'}), 200
    else:
        return jsonify({"status" : "failed","message": "Akses ditolak"}), 400

@admin_bp.route('/checkPhoneMitra', methods=['POST'])
def checkPhoneMitra():
    auth = request.authorization
    if not auth or not auth.token:
        return jsonify({'message': 'Akses ditolak'}), 400
    dataMitra = decode(auth.token)
    dataMitra = dataMitra.split(admin_delimiter)
    if len(dataMitra) > 3 or len(dataMitra) < 2 :
        return jsonify({"status" : "failed","message": "Akses ditolak"}), 400
    email = dataMitra[0]
    phone = dataMitra[1]
    checkAdmin = admin_model.getDataAdminByEmail(email)
    if checkAdmin is not None : 
        checkMitra = mitra_model.getMitraLogin("", phone)
        if len(dataMitra) == 3 :
            uniqueid = dataMitra[2]
            if checkMitra is None or checkMitra[2] == uniqueid :
                return jsonify({"status":'success','message': 'No.HP tersedia!'}), 200
            else:
                return jsonify({"status":'failed','message': 'No.HP tidak tersedia!'}), 200
        elif len(dataMitra) == 2:
            if checkMitra is None :
                return jsonify({"status":'success','message': 'No.HP tersedia!'}), 200
            else:
                return jsonify({"status":'failed','message': 'No.HP tidak tersedia!'}), 200
        else:
            return jsonify({"status":'failed','message': 'No.HP tidak tersedia!'}), 200
    else:
        return jsonify({"status" : "failed","message": "Akses ditolak"}), 400


@admin_bp.route('/registerMitra', methods=['POST'])
def registerMitra():
    auth = request.authorization
    if not auth or not auth.token:
        return jsonify({'message': 'Akses ditolak'}), 400
    dataMitra = decode(auth.token)
    dataMitra = dataMitra.split(admin_delimiter)
    if len(dataMitra) != 6 :
        return jsonify({"status" : "failed","message": "Registrasi mitra gagal!"}), 400
    emailAdmin = dataMitra[0]
    name = dataMitra[1]
    email = dataMitra[2]
    phone = dataMitra[3]
    address = dataMitra[4]
    pin = bcrypt.hashpw(dataMitra[5].encode('utf-8'), SALT_KEY)
    uniqueid = generate_uniqueid()
    checkAdmin = admin_model.getDataAdminByEmail(emailAdmin)
    if checkAdmin is not None : 
        checkMitra = mitra_model.getMitraLogin(email)

        if checkMitra is None:
            checkMitra = mitra_model.registerMitra(uniqueid, name, email, phone, pin, address)    
            if checkMitra is True:
                return jsonify({"status":'success','message': 'Registrasi berhasil!'}), 200
        else:
            return jsonify({"status":'failed','message': 'Registrasi gagal!'}), 303
    else:
        return jsonify({'message': 'Akses ditolak'}), 400
    

@admin_bp.route('/getDataMitra', methods=['POST'])
def getDataMitra():
    auth = request.authorization
    if not auth or not auth.token:
        return jsonify({'message': 'Akses ditolak'}), 400
    dataMitra = decode(auth.token)
    dataMitra = dataMitra.split(admin_delimiter)
    if len(dataMitra) != 2 :
        return jsonify({"status" : "failed","message": "Akses ditolak"}), 400
    email = dataMitra[0]
    uniqueid = dataMitra[1]
    checkAdmin = admin_model.getDataAdminByEmail(email)
    if checkAdmin is not None : 
        dataMitra = mitra_model.getDataMitra(uniqueid) 
        # Name, Phone, Email, Address
        if dataMitra is not None:
            response = {
                "status":"success",
                "data": {
                    "Name" : dataMitra[0],
                    "Phone": dataMitra[1],
                    "Email": dataMitra[2],
                    "Address": dataMitra[3]
                }
            } 
            return jsonify(response), 200
        else:
            return jsonify({"status":'failed','message': 'Data kosong!'}), 303
    else :
        return jsonify({'message': 'Akses ditolak'}), 400
    
@admin_bp.route('/updateDataMitra', methods=['POST'])
def updateDataMitra():
    auth = request.authorization
    if not auth or not auth.token:
        return jsonify({'message': 'Akses ditolak'}), 400
    dataMitra = decode(auth.token)
    dataMitra = dataMitra.split(admin_delimiter)
    if len(dataMitra) != 6 :
        return jsonify({"status" : "failed","message": "Update data mitra gagal!"}), 400
    admin = dataMitra[0]
    uniqueid = dataMitra[1]
    name = dataMitra[2]
    email = dataMitra[3]
    phone = dataMitra[4]
    address = dataMitra[5]
    checkAdmin = admin_model.getDataAdminByEmail(admin)
    if checkAdmin is not None : 
        checkMitra = mitra_model.updateDataMitra(name, email, phone, address, uniqueid)    
        if checkMitra is True:
            return jsonify({"status":'success','message': 'Update data berhasil!'}), 200
        else:
            return jsonify({"status":'failed','message': 'Update data gagal!'}), 303
    else:
        return jsonify({'message': 'Akses ditolak'}), 400
    

@admin_bp.route('/newEncode', methods=['POST'])
def newEncode():
    data = request.get_json()
    param = data.get('param')
    result = encode(param)
    return jsonify({"status":'failed','message': result}), 200

@admin_bp.route('/newDecode', methods=['POST'])
def newDecode():
    data = request.get_json()
    param = data.get('param')
    result = decode(param)
    return jsonify({"status":'failed','message': result}), 200

@admin_bp.route('/test_base64', methods=['POST'])
def test_base64():
    data = request.get_json()
    param = data.get('param')
    result = base64.b64encode(param.encode()).decode()
    return jsonify({"status":'success','message': result}), 200



    




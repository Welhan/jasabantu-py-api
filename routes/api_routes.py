from flask import Blueprint, jsonify, request
import requests
from models.sysModel import Sys
from config.constants import API_VERSION, WA_ENGINE

api_bp = Blueprint('api_bp', __name__)
sysModel = Sys()

@api_bp.route('/checkApiStatus', methods=['GET'])
def checkStatus():
    result = sysModel.checkMaintenanceState()
    if result is None:
        return jsonify({"status" : False, "message": "Something went worng!"}), 202
    else:
        return jsonify({"status" : True, "maintenance": result[0][0], "version": API_VERSION}), 200
    
@api_bp.route('/checkWaStatus', methods=['GET'])
def checkWaStatus():
    url = WA_ENGINE + 'check-otp'
    response = requests.post(url)
    if response.status_code == 200:
        return jsonify({"status" : True}), 200
    return jsonify({"status" : False, "message": "Something went worng!"}), 202
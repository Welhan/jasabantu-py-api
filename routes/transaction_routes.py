from flask import Blueprint, jsonify, request
from midtransclient import Snap
import json
import requests

transaction_bp = Blueprint('transaction_bp', __name__)

# Inisialisasi Snap Midtrans dengan client key dan environment
snap = Snap(server_key='SB-Mid-server-0X2mrPZe0pWl6hDJym5vVgTu', is_production=False)
server_key = "U0ItTWlkLXNlcnZlci0wWDJtclBaZTBwV2w2aERKeW01dlZnVHU6cGFzc3dvcmQ="

@transaction_bp.route('/transaction/create-transaction', methods=['POST'])
def create_transaction():
    try:
        request_data = request.get_json()
        order_id = request_data.get('order_id')
        gross_amount = request_data.get('gross_amount')
        payment_type = request_data.get('payment_type')
        acquirer = request_data.get('acquirer')
        enabled_payments = request_data.get('enabled_payments')

        if not order_id or not gross_amount:
            return jsonify({"error": "order_id and gross_amount are required"}), 400

        try:
            gross_amount = int(gross_amount)
        except ValueError:
            return jsonify({"error": "gross_amount must be a number"}), 400
        
        # Data transaksi
        transaction_details = {
            "payment_type" : payment_type,
            "transaction_details" : {
                "order_id": order_id,
                "gross_amount": int(gross_amount),
            },
            "qris" : {
                "acquirer" : acquirer
            },
            "enabled_payments": [enabled_payments]    
        }
        print(transaction_details)
        transaction_json = json.dumps(transaction_details)

        print(transaction_json)
        snap_token = snap.create_transaction(transaction_json)
        payment_url = snap_token['redirect_url']

        return jsonify({"payment_url": payment_url}), 200

    except Exception as e:
        print(f"Error creating transaction: {e}")
        return jsonify({"error": "Failed to create transaction"}), 500

@transaction_bp.route('/transaction/payment-method', methods=['POST'])
def payment_method():
    try:
        # Data transaksi dari request
        request_data = request.get_json()
        snap_token = request_data.get('snap_token')

        # Mengambil informasi metode pembayaran dari respon transaksi
        payment_method = snap_token['payment_type']

        return jsonify({"payment_method": payment_method}), 200

    except Exception as e:
        print(f"Error checking payment method: {e}")
        return jsonify({"error": "Failed to check payment method"}), 500
    
@transaction_bp.route('/transaction/check', methods=['POST'])
def check_payment():
    data = request.get_json()
    order_id = str(data.get('order_id'))
    url = "https://api.sandbox.midtrans.com/v2/" + order_id + "/status" 
    headers = {
        "Content-Type": "application/json",
        "Authorization": "Basic " + server_key
    }
    response = requests.get(url, '', headers=headers)    
    if response.status_code == 200:
        response_data = response.json()
        status_code = response_data.get('status_code')
        status_message = response_data.get('status_message')
        transaction_status = response_data.get('transaction_status')
        settlement_time = response_data.get('settlement_time')
        msg = {
            "status_code": status_code,
            "status_message": status_message,
            "transaction_status": transaction_status,
            "settlement_time" : settlement_time
            }
        return jsonify(msg), response.status_code
    else:
        return jsonify({"status": "error", "message": "Gagal mengirim permintaan ke Midtrans"}), response.status_code



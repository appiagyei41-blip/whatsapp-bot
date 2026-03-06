#!/usr/bin/env python3
import os
import json
from flask import Flask, request, jsonify
import requests
from datetime import datetime

app = Flask(__name__)

TWILIO_ACCOUNT_SID = "AC7042020432dc0905c525977d48d25ade"
TWILIO_AUTH_TOKEN = "AC7042020432dc0905c525977d48d25ade"
TWILIO_WHATSAPP_NUMBER = TWILIO_WHATSAPP_NUMBER = "whatsapp:+14155238886"

def send_whatsapp_message(phone_number, message):
    try:
        if not phone_number.startswith('whatsapp:'):
            phone_number = f"whatsapp:{phone_number}"
        
        url = f"https://api.twilio.com/2010-04-01/Accounts/{TWILIO_ACCOUNT_SID}/Messages.json"
        
        data = {
            'From': TWILIO_WHATSAPP_NUMBER,
            'To': phone_number,
            'Body': message
        }
        
        response = requests.post(
            url,
            data=data,
            auth=(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN),
            timeout=10
        )
        
        print(f"Response status: {response.status_code}")
        print(f"Response: {response.text}")
        
        return response.status_code == 201
    except Exception as e:
        print(f"Error: {e}")
        return False

@app.route('/', methods=['GET'])
def home():
    return jsonify({'status': 'Bot is running!', 'version': '1.0'})

@app.route('/health', methods=['GET'])
def health():
    return jsonify({'status': 'healthy'})

@app.route('/test-message', methods=['POST'])
def test_message():
    try:
        data = request.json
        phone = data.get('whatsapp_number')
        
        if not phone:
            return jsonify({'error': 'Phone required'}), 400
        
        message = "🎉 WhatsApp Bot Test Message!\n\nYour bot is working! You will receive daily updates starting tomorrow at 8:00 AM."
        
        success = send_whatsapp_message(phone, message)
        
        return jsonify({'sent': success, 'phone': phone, 'message': message})
    except Exception as e:
        return jsonify({'error': str(e)}), 400

@app.route('/subscribe', methods=['POST'])
def subscribe():
    try:
        data = request.json
        return jsonify({'status': 'subscribed', 'code': 'TEST123'})
    except Exception as e:
        return jsonify({'error': str(e)}), 400

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=False)
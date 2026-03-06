#!/usr/bin/env python3
"""
WhatsApp Daily Updates Bot - Pre-configured for GitHub
Your credentials are already built in
"""

import os
import json
import time
import requests
from datetime import datetime
from flask import Flask, request, jsonify
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# YOUR CREDENTIALS (Already configured)
TWILIO_ACCOUNT_SID = "AC7042020432dc0905c525977d48d25ade"
TWILIO_AUTH_TOKEN = "AC7042020432dc0905c525977d48d25ade"
TWILIO_WHATSAPP_NUMBER = "whatsapp:+233506140644"

app = Flask(__name__)

class WhatsAppBot:
    def __init__(self):
        self.subscriptions = {}
        self.load_subscriptions()
    
    def load_subscriptions(self):
        try:
            if os.path.exists('subscriptions.json'):
                with open('subscriptions.json', 'r') as f:
                    self.subscriptions = json.load(f)
        except:
            pass
    
    def save_subscriptions(self):
        with open('subscriptions.json', 'w') as f:
            json.dump(self.subscriptions, f)
    
    def send_whatsapp_message(self, phone_number, message):
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
            
            return response.status_code == 201
        except Exception as e:
            logger.error(f"Error: {e}")
            return False
    
    def get_crypto_update(self):
        try:
            response = requests.get('https://api.coingecko.com/api/v3/simple/price?ids=bitcoin,ethereum&vs_currencies=usd&include_24hr_change=true', timeout=5)
            data = response.json()
            btc = data.get('bitcoin', {})
            eth = data.get('ethereum', {})
            return f"""
₿ CRYPTO UPDATE
Bitcoin: ${btc.get('usd', 'N/A'):,.0f}
Change: {btc.get('usd_24h_change', 0):+.2f}%
Ethereum: ${eth.get('usd', 'N/A'):,.0f}
Change: {eth.get('usd_24h_change', 0):+.2f}%
"""
        except:
            return "₿ Crypto update unavailable"
    
    def get_test_message(self):
        return """
🎉 WhatsApp Daily Updates Bot is WORKING!

Your bot is successfully connected to Twilio.

You will start receiving daily updates:
✅ Crypto prices
✅ Finance tips
✅ Global news
✅ Job opportunities
✅ Travel deals
✅ Clothing sales
✅ Product deals
✅ And more!

---
Powered by WhatsApp Daily Updates Bot
"""

bot = WhatsAppBot()

@app.route('/', methods=['GET'])
def home():
    return jsonify({'status': 'Bot is running!', 'message': 'WhatsApp Daily Updates Bot'})

@app.route('/health', methods=['GET'])
def health():
    return jsonify({'status': 'healthy', 'timestamp': datetime.now().isoformat()})

@app.route('/test-message', methods=['POST'])
def test_message():
    try:
        data = request.json
        phone = data.get('whatsapp_number')
        
        if not phone:
            return jsonify({'error': 'Phone number required'}), 400
        
        message = bot.get_test_message()
        success = bot.send_whatsapp_message(phone, message)
        
        return jsonify({'sent': success, 'phone': phone})
    except Exception as e:
        return jsonify({'error': str(e)}), 400

@app.route('/subscribe', methods=['POST'])
def subscribe():
    try:
        data = request.json
        code = 'CODE' + str(len(bot.subscriptions))
        
        bot.subscriptions[code] = {
            'phone': data.get('whatsapp_number'),
            'name': data.get('name'),
            'categories': data.get('categories', []),
            'frequency': data.get('frequency', 'daily'),
            'first_time': data.get('first_time', '08:00'),
            'active': True
        }
        
        bot.save_subscriptions()
        
        return jsonify({'activation_code': code, 'status': 'success'})
    except Exception as e:
        return jsonify({'error': str(e)}), 400

@app.route('/subscriptions', methods=['GET'])
def get_subscriptions():
    count = len([s for s in bot.subscriptions.values() if s.get('active')])
    return jsonify({'total_subscriptions': count, 'status': 'active'})

if __name__ == '__main__':
    logger.info("🚀 WhatsApp Bot Starting...")
    logger.info(f"Twilio Account: {TWILIO_ACCOUNT_SID}")
    logger.info(f"WhatsApp Number: {TWILIO_WHATSAPP_NUMBER}")
    app.run(host='0.0.0.0', port=5000, debug=False)

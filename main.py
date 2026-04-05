import requests
from flask import Flask, jsonify, request
import os

app = Flask(__name__)

# بيانات الموقع التركي (Takipcibase)
API_URL = "https://takipcibase.com/api/v2"
# الـ API Key هتحتاجه من حسابك في الموقع هناك
API_KEY = "YOUR_API_KEY_HERE" 

@app.route('/')
def home():
    return "Baraa Boost: API Connection is Ready!"

@app.route('/balance')
def get_balance():
    # كود بيجيب رصيدك من الموقع التركي
    payload = {
        'key': API_KEY,
        'action': 'balance'
    }
    try:
        response = requests.post(API_URL, data=payload)
        return jsonify(response.json())
    except Exception as e:
        return jsonify({"error": str(e)})

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
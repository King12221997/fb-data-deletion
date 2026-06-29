from flask import Flask, request, jsonify
import hmac, hashlib, json, base64, urllib.parse

app = Flask(__name__)
APP_SECRET = "your_app_secret_from_facebook_dashboard"

@app.route('/data_deletion_callback', methods=['POST'])
def data_deletion():
    signed = request.form.get('signed_request')
    if not signed:
        return jsonify({"error": "missing signed_request"}), 400
    sig, payload = signed.split('.', 1)
    sig = urllib.parse.unquote(sig)
    payload = urllib.parse.unquote(payload)
    expected = hmac.new(APP_SECRET.encode(), payload.encode(), hashlib.sha256).hexdigest()
    if sig != expected:
        return jsonify({"error": "invalid signature"}), 400
    data = json.loads(base64.urlsafe_b64decode(payload + '==').decode())
    user_id = data.get('user_id')
    # Delete user data here
    return jsonify({"url": "https://your-app.onrender.com/status/123", "confirmation_code": "abc123"})

@app.route('/')
def home():
    return "OK"

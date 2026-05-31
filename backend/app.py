from flask import Flask, jsonify, send_from_directory, request, session, redirect
from flask_cors import CORS
import os

app = Flask(__name__, static_folder='../frontend', static_url_path='')
CORS(app)
app.secret_key = "traffic123"

ADMIN_USERNAME = "admin"
ADMIN_PASSWORD = "traffic@123"

# ── MAIN PAGE ──
@app.route('/')
def index():
    return send_from_directory('../frontend', 'index.html')

# ── LOGIN PAGE ──
@app.route('/login')
def login_page():
    return send_from_directory('../frontend', 'login.html')

# ── ADMIN PAGE ──
@app.route('/admin')
def admin_page():
    if not session.get('admin'):
        return redirect('/login')
    return send_from_directory('../frontend', 'admin.html')

# ── LOGIN API ──
@app.route('/api/login', methods=['POST'])
def api_login():
    data = request.get_json()
    if data.get('username') == ADMIN_USERNAME and data.get('password') == ADMIN_PASSWORD:
        session['admin'] = True
        return jsonify({"success": True})
    return jsonify({"success": False, "error": "Wrong username or password!"})

# ── LOGOUT ──
@app.route('/api/logout')
def api_logout():
    session.pop('admin', None)
    return jsonify({"success": True})

# ── API ROUTES ──
@app.route('/api/summary')
def summary():
    return jsonify({
        "total_accidents": 1250,
        "total_deaths": 340,
        "total_injuries": 2100,
        "avg_per_day": 3.4
    })

@app.route('/api/by-cause')
def by_cause():
    return jsonify([
        {"cause": "Overspeeding",  "count": 380},
        {"cause": "Drunk Driving", "count": 210},
        {"cause": "Signal Jump",   "count": 175},
        {"cause": "Wrong Lane",    "count": 140},
        {"cause": "Distracted",    "count": 345}
    ])

@app.route('/api/by-location')
def by_location():
    return jsonify([
        {"location": "Chennai",    "count": 320},
        {"location": "Coimbatore", "count": 185},
        {"location": "Madurai",    "count": 160},
        {"location": "Salem",      "count": 130},
        {"location": "Trichy",     "count": 110}
    ])

@app.route('/api/by-month')
def by_month():
    return jsonify([
        {"month": "Jan", "count": 95},
        {"month": "Feb", "count": 88},
        {"month": "Mar", "count": 102},
        {"month": "Apr", "count": 115},
        {"month": "May", "count": 98},
        {"month": "Jun", "count": 120},
        {"month": "Jul", "count": 135},
        {"month": "Aug", "count": 128},
        {"month": "Sep", "count": 110},
        {"month": "Oct", "count": 95},
        {"month": "Nov", "count": 88},
        {"month": "Dec", "count": 126}
    ])

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=True)
from flask import Flask, jsonify, send_from_directory, request, session
from flask_cors import CORS
import os
import numpy as np

app = Flask(__name__,
    static_folder=os.path.join(os.path.dirname(__file__), '..', 'frontend'),
    static_url_path='')
CORS(app)
app.secret_key = "traffic123"

ADMIN_USERNAME = "admin"
ADMIN_PASSWORD = "traffic@123"

@app.route('/')
def index():
    frontend = os.path.join(os.path.dirname(__file__), '..', 'frontend')
    return send_from_directory(frontend, 'index.html')

@app.route('/admin')
def admin_page():
    frontend = os.path.join(os.path.dirname(__file__), '..', 'frontend')
    return send_from_directory(frontend, 'admin.html')

@app.route('/login')
def login_page():
    frontend = os.path.join(os.path.dirname(__file__), '..', 'frontend')
    return send_from_directory(frontend, 'login.html')

@app.route('/api/login', methods=['POST'])
def login():
    data = request.get_json()
    if data['username'] == ADMIN_USERNAME and data['password'] == ADMIN_PASSWORD:
        session['admin'] = True
        return jsonify({"success": True})
    return jsonify({"success": False, "msg": "Wrong credentials!"})

@app.route('/api/logout')
def logout():
    session.pop('admin', None)
    return jsonify({"success": True})

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
        {"cause": "Overspeeding", "count": 380},
        {"cause": "Drunk Driving", "count": 210},
        {"cause": "Signal Jump", "count": 175},
        {"cause": "Wrong Lane", "count": 140},
        {"cause": "Distracted", "count": 345}
    ])

@app.route('/api/by-location')
def by_location():
    return jsonify([
        {"location": "Chennai", "count": 320},
        {"location": "Bengaluru", "count": 275},
        {"location": "Coimbatore", "count": 185},
        {"location": "Madurai", "count": 160},
        {"location": "Salem", "count": 130},
        {"location": "Trichy", "count": 110},
        {"location": "Erode", "count": 95}
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

@app.route('/api/by-year')
def by_year():
    return jsonify([
        {"year": "2020", "accidents": 850, "deaths": 210, "injuries": 1400},
        {"year": "2021", "accidents": 920, "deaths": 245, "injuries": 1580},
        {"year": "2022", "accidents": 1050, "deaths": 280, "injuries": 1750},
        {"year": "2023", "accidents": 1180, "deaths": 310, "injuries": 1950},
        {"year": "2024", "accidents": 1250, "deaths": 340, "injuries": 2100},
        {"year": "2025", "accidents": 980, "deaths": 265, "injuries": 1620},
    ])

@app.route('/api/predict')
def predict():
    years = [2020, 2021, 2022, 2023, 2024, 2025]
    accidents = [850, 920, 1050, 1180, 1250, 980]

    x = np.array(years, dtype=float)
    y = np.array(accidents, dtype=float)

    x_mean = np.mean(x)
    y_mean = np.mean(y)
    slope = np.sum((x - x_mean) * (y - y_mean)) / np.sum((x - x_mean) ** 2)
    intercept = y_mean - slope * x_mean

    future_years = [2026, 2027, 2028]
    predictions = [max(0, round(slope * yr + intercept)) for yr in future_years]

    trend = "increasing" if slope > 0 else "decreasing"
    risk = "HIGH" if predictions[0] > 1200 else "MEDIUM" if predictions[0] > 900 else "LOW"

    return jsonify({
        "past": [{"year": str(y), "accidents": int(a)} for y, a in zip(years, accidents)],
        "future": [{"year": str(y), "predicted": int(p)} for y, p in zip(future_years, predictions)],
        "trend": trend,
        "risk": risk,
        "slope": round(float(slope), 2),
        "insight": f"Every year accidents {'increase' if slope > 0 else 'decrease'} by ~{abs(round(slope))} on average.",
        "prediction_2026": predictions[0],
        "prediction_2027": predictions[1],
        "prediction_2028": predictions[2]
    })

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=True)
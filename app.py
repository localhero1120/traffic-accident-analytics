from flask import Flask, jsonify, send_from_directory
from flask_cors import CORS
import os

# ✅ Path fix
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
FRONTEND_DIR = os.path.join(BASE_DIR, 'frontend')

app = Flask(__name__, static_folder=FRONTEND_DIR, static_url_path='')
CORS(app)

@app.route('/')
def index():
    return send_from_directory(FRONTEND_DIR, 'index.html')

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
        {"location": "Coimbatore", "count": 185},
        {"location": "Madurai", "count": 160},
        {"location": "Salem", "count": 130},
        {"location": "Trichy", "count": 110}
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

@app.route('/api/predict')
def predict():
    past = [
        {"year": 2020, "accidents": 850},
        {"year": 2021, "accidents": 930},
        {"year": 2022, "accidents": 1050},
        {"year": 2023, "accidents": 1165},
        {"year": 2024, "accidents": 1240},
        {"year": 2025, "accidents": 970}
    ]
    accidents = [p["accidents"] for p in past]
    n = len(accidents)
    slope = round((accidents[-1] - accidents[0]) / (n - 1))
    last = accidents[-1]
    p26 = last + slope
    p27 = p26 + slope
    p28 = p27 + slope
    trend = "INCREASING" if slope > 0 else "DECREASING"
    risk = "HIGH" if p26 > 1500 else "MEDIUM" if p26 > 1000 else "LOW"
    return jsonify({
        "past": past,
        "future": [
            {"year": 2026, "predicted": p26},
            {"year": 2027, "predicted": p27},
            {"year": 2028, "predicted": p28}
        ],
        "prediction_2026": p26,
        "prediction_2027": p27,
        "prediction_2028": p28,
        "trend": trend,
        "risk": risk,
        "insight": f"Yearly trend: ~{abs(slope)} accidents per year."
    })

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=True)
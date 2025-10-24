from flask import Flask, render_template, jsonify, request
import os
import logging
import requests
from datetime import datetime

app = Flask(__name__)

# Configuration
UPLOAD_FOLDER = 'static/images/uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# Extended CROP_DATA with 20 crops
CROP_DATA = {
    "wheat": {"season": "rabi", "best_state": "Punjab", "water": "450-600mm", "temperature": "10-15°C"},
    "rice": {"season": "kharif", "best_state": "West Bengal", "water": "1000-1500mm", "temperature": "20-35°C"},
    "corn": {"season": "kharif", "best_state": "Karnataka", "water": "500-700mm", "temperature": "20-27°C"},
    "sugarcane": {"season": "whole_year", "best_state": "Uttar Pradesh", "water": "1500-2500mm", "temperature": "20-30°C"},
    "cotton": {"season": "kharif", "best_state": "Gujarat", "water": "600-1000mm", "temperature": "25-35°C"},
    "soybean": {"season": "kharif", "best_state": "Madhya Pradesh", "water": "450-750mm", "temperature": "20-30°C"},
    "mustard": {"season": "rabi", "best_state": "Rajasthan", "water": "300-500mm", "temperature": "10-25°C"},
    "groundnut": {"season": "kharif", "best_state": "Gujarat", "water": "500-750mm", "temperature": "20-35°C"},
    "potato": {"season": "rabi", "best_state": "Uttar Pradesh", "water": "500-700mm", "temperature": "15-20°C"},
    "tomato": {"season": "year_round", "best_state": "Andhra Pradesh", "water": "600-800mm", "temperature": "20-25°C"},
    "onion": {"season": "rabi", "best_state": "Maharashtra", "water": "600-800mm", "temperature": "13-24°C"},
    "chilli": {"season": "kharif", "best_state": "Andhra Pradesh", "water": "700-1200mm", "temperature": "20-30°C"},
    "brinjal": {"season": "year_round", "best_state": "West Bengal", "water": "600-800mm", "temperature": "20-35°C"},
    "cabbage": {"season": "rabi", "best_state": "Punjab", "water": "500-700mm", "temperature": "15-20°C"},
    "cauliflower": {"season": "rabi", "best_state": "Uttar Pradesh", "water": "500-700mm", "temperature": "15-20°C"},
    "carrot": {"season": "rabi", "best_state": "Punjab", "water": "500-700mm", "temperature": "15-20°C"},
    "beetroot": {"season": "rabi", "best_state": "Punjab", "water": "500-700mm", "temperature": "15-20°C"},
    "radish": {"season": "rabi", "best_state": "Uttar Pradesh", "water": "400-600mm", "temperature": "15-25°C"},
    "bittergourd": {"season": "kharif", "best_state": "West Bengal", "water": "600-800mm", "temperature": "25-35°C"},
    "papaya": {"season": "year_round", "best_state": "Karnataka", "water": "700-1000mm", "temperature": "25-30°C"}
}

# Logging setup
logging.basicConfig(level=logging.INFO)

# Status endpoint
@app.route('/status')
def status():
    return jsonify({
        "status": "healthy",
        "timestamp": datetime.now().isoformat(),
        "models": {
            "huggingface_model": False,
            "crop_recommendation_model": True,
            "chat_model": False
        },
        "apis": {
            "weather": "connected" if test_weather_api() else "disconnected"
        }
    })

def test_weather_api():
    """Test if Open-Meteo API is working"""
    try:
        url = "https://api.open-meteo.com/v1/forecast"
        params = {
            "latitude": 27.1767,
            "longitude": 78.0081,
            "current": "temperature_2m,relative_humidity_2m,weather_code",
            "forecast_days": 1
        }
        response = requests.get(url, params=params, timeout=5)
        return response.status_code == 200
    except Exception as e:
        logging.error(f"Open-Meteo API test failed: {e}")
        return False

# Main route
@app.route('/')
def index():
    return render_template('index.html')

# Crop Recommendation
@app.route('/api/recommend', methods=['POST'])
def recommend_crop():
    data = request.json
    soil = data.get('soil', '').lower()
    season = data.get('season', '').lower()

    logging.info(f"Received soil: {soil}, season: {season}")  # Debug log

    # Rule-based crop mapping based on soil and season
    if 'clay' in soil:
        if 'kharif' in season:
            crop = 'rice'
        elif 'rabi' in season:
            crop = 'wheat'
        else:
            crop = 'sugarcane'
    elif 'sandy' in soil:
        if 'kharif' in season:
            if 'dry' in soil:
                crop = 'groundnut'
            else:
                crop = 'cotton'
        elif 'rabi' in season:
            crop = 'potato'
        else:
            crop = 'radish'
    elif 'loamy' in soil:
        if 'kharif' in season:
            crop = 'corn'
        elif 'rabi' in season:
            crop = 'wheat'
        else:
            crop = 'tomato'
    elif 'black' in soil or 'regur' in soil:
        if 'kharif' in season:
            crop = 'cotton'
        else:
            crop = 'soybean'
    elif 'red' in soil:
        if 'kharif' in season:
            crop = 'chilli'
        else:
            crop = 'carrot'
    else:
        if 'kharif' in season:
            crop = 'corn'
        elif 'rabi' in season:
            crop = 'mustard'
        else:
            crop = 'brinjal'

    # Ensure crop exists in CROP_DATA
    if crop not in CROP_DATA:
        logging.error(f"Crop {crop} not found in CROP_DATA")
        crop = "corn"  # Fallback

    return jsonify({
        "crop": crop,
        "details": CROP_DATA[crop],
        "confidence": 0.85
    })

# Disease Detection
@app.route('/api/detect', methods=['POST'])
def detect_disease():
    return jsonify({
        "disease": "Rust",
        "confidence": 0.78,
        "solution": "Apply fungicide treatment",
        "severity": "medium"
    })

@app.route('/api/weather')
def get_weather():
    try:
        city_input = request.args.get('city', 'Agra')
        logging.info(f"Raw city received: '{city_input}'")  # Debug log

        # Normalize input to title case for consistency
        city = city_input.strip()

        # Case-insensitive mapping using .lower() for keys
        cities = {
            'agra': (27.1767, 78.0081),
            'delhi': (28.7041, 77.1025),
            'mumbai': (19.0760, 72.8777),
            'bengaluru': (12.9716, 77.5946),
            'bangalore': (12.9716, 77.5946),  # Alias
            'chennai': (13.0827, 80.2707),
            'kolkata': (22.5726, 88.3639),
            'hyderabad': (17.3850, 78.4867),
            'pune': (18.5204, 73.8567)
        }

        lat, lon = cities.get(city.lower(), (27.1767, 78.0081))

        if city.lower() not in cities:
            logging.warning(f"City '{city}' not found in mapping, using Agra as fallback")

        url = "https://api.open-meteo.com/v1/forecast"
        params = {
            "latitude": lat,
            "longitude": lon,
            "current": "temperature_2m,relative_humidity_2m,weather_code",
            "daily": "weather_code,temperature_2m_max,temperature_2m_min",
            "forecast_days": 2,
            "timezone": "Asia/Kolkata"
        }

        response = requests.get(url, params=params, timeout=10)
        response.raise_for_status()
        data = response.json()

        weather_conditions = {
            0: "Clear", 1: "Mostly clear", 2: "Partly cloudy", 3: "Overcast",
            45: "Fog", 48: "Depositing rime fog", 51: "Light drizzle",
            53: "Moderate drizzle", 55: "Dense drizzle", 56: "Light freezing drizzle",
            57: "Dense freezing drizzle", 61: "Slight rain", 63: "Moderate rain",
            65: "Heavy rain", 66: "Light freezing rain", 67: "Heavy freezing rain",
            71: "Slight snow fall", 73: "Moderate snow fall", 75: "Heavy snow fall",
            77: "Snow grains", 80: "Slight rain showers", 81: "Moderate rain showers",
            82: "Violent rain showers", 85: "Slight snow showers", 86: "Heavy snow showers",
            95: "Thunderstorm", 96: "Thunderstorm with slight hail", 99: "Thunderstorm with heavy hail"
        }

        current = data['current']
        daily = data['daily']

        condition_code = current['weather_code']
        condition = weather_conditions.get(condition_code, "Unknown")

        return jsonify({
            "city": city,
            "temperature": round(current['temperature_2m']),
            "condition": condition,
            "humidity": current['relative_humidity_2m'],
            "forecast": [
                {
                    "day": "Today",
                    "temp": f"{round(daily['temperature_2m_max'][0])}°C",
                    "condition": weather_conditions.get(daily['weather_code'][0], "Unknown")
                },
                {
                    "day": "Tomorrow",
                    "temp": f"{round(daily['temperature_2m_max'][1])}°C",
                    "condition": weather_conditions.get(daily['weather_code'][1], "Unknown")
                }
            ],
            "source": "Open-Meteo.com",
            "last_updated": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        })

    except requests.exceptions.RequestException as e:
        logging.error(f"Open-Meteo API request failed: {str(e)}")
        return jsonify({
            "city": city_input,
            "temperature": 32,
            "condition": "Sunny",
            "forecast": [
                {"day": "Today", "temp": "32°C", "condition": "Sunny"},
                {"day": "Tomorrow", "temp": "33°C", "condition": "Sunny"}
            ],
            "source": "Mock fallback"
        })
    except Exception as e:
        logging.error(f"Weather API error: {str(e)}")
        return jsonify({"error": "Failed to process weather data"}), 500


@app.route('/api/mandi')
def get_mandi_prices():
    try:
        # AGMARKNET API endpoint
        url = "https://api.data.gov.in/resource/9ef84268-d588-465a-a308-a864a43d0070"
        
        # Your actual API key
        api_key = "579b464db66ec23bdd000001018aaa2a4b0345f24ad9a36130ef558d "  # ← Replace with your actual API key
        
        # Top 10 cities with their major mandi markets
        city_market_map = {
            "Agra": "Agra",
            "Delhi": "Azadpur",
            "Mumbai": "Mumbai",
            "Kolkata": "Kolkata",
            "Chennai": "Koyambedu",
            "Bengaluru": "Bangalore",
            "Hyderabad": "Hyderabad",
            "Pune": "Pune",
            "Lucknow": "Lucknow",
            "Jaipur": "Jaipur"
        }
        
        # These states correspond to the cities above
        city_state_map = {
            "Agra": "Uttar Pradesh",
            "Delhi": "Delhi",
            "Mumbai": "Maharashtra",
            "Kolkata": "West Bengal",
            "Chennai": "Tamil Nadu",
            "Bengaluru": "Karnataka",
            "Hyderabad": "Telangana",
            "Pune": "Maharashtra",
            "Lucknow": "Uttar Pradesh",
            "Jaipur": "Rajasthan"
        }
        
        all_commodities = []
        
        for city, market in city_market_map.items():
            try:
                params = {
                    "api-key": api_key,
                    "format": "json",
                    "offset": 0,
                    "limit": 5,
                    "filters[market]": market,
                    "filters[state]": city_state_map[city]
                }
                
                response = requests.get(url, params=params, timeout=10)
                
                if response.status_code == 200:
                    data = response.json()
                    records = data.get('records', [])
                    
                    # Take first few records for each city
                    for item in records[:2]:  # 2 commodities per city
                        all_commodities.append({
                            "name": item.get('commodity', 'Unknown'),
                            "price": str(item.get('modal_price', 'N/A')),
                            "unit": "per quintal",
                            "city": city,
                            "market": market,
                            "variety": item.get('variety', 'Common')
                        })
                
            except Exception as e:
                logging.error(f"Failed to fetch data for {city}: {str(e)}")
                continue  # Continue with next city
        
        if all_commodities:
            return jsonify({
                "commodities": all_commodities,
                "location": "Top 10 Indian Cities",
                "source": "AGMARKNET",
                "update_time": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "total_cities": 10,
                "cities_covered": list(city_market_map.keys())
            })
        else:
            # Fallback if all API calls fail
            logging.warning("All AGMARKNET requests failed, using static fallback")
            return jsonify({
                "commodities": [
                    {"name": "Wheat", "price": "2200", "unit": "per quintal", "city": "Agra"},
                    {"name": "Rice", "price": "3100", "unit": "per quintal", "city": "Delhi"},
                    {"name": "Onion", "price": "1800", "unit": "per quintal", "city": "Mumbai"},
                    {"name": "Potato", "price": "1200", "unit": "per quintal", "city": "Kolkata"}
                ],
                "location": "Top 10 Indian Cities",
                "source": "Mock fallback",
                "update_time": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            })
            
    except Exception as e:
        logging.error(f"Critical error in mandi price API: {str(e)}")
        return jsonify({
            "commodities": [
                {"name": "Wheat", "price": "2200", "unit": "per quintal", "city": "Agra"},
                {"name": "Rice", "price": "3100", "unit": "per quintal", "city": "Delhi"},
                {"name": "Onion", "price": "1800", "unit": "per quintal", "city": "Mumbai"},
                {"name": "Potato", "price": "1200", "unit": "per quintal", "city": "Kolkata"}
            ],
            "location": "Top 10 Indian Cities",
            "source": "Fallback",
            "update_time": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        })

# Fertilizer Recommendation
@app.route('/api/fertilizer', methods=['POST'])
def fertilizer_recommendation():
    data = request.json
    crop = data.get('crop', '').lower()
    
    recommendations = {
        'wheat': 'Apply 120:60:40 NPK kg/ha with 2/3 N as basal and 1/3 at tillering',
        'rice': 'Apply 100:50:50 NPK kg/ha with split application of nitrogen in three doses',
        'maize': 'Use 120:60:40 NPK kg/ha with 20-10-10 at sowing and 10-20-20 before tasseling',
        'sugarcane': 'Apply 200:100:100 NPK kg/ha in 4-5 splits throughout the growing season',
        'cotton': 'Use 100:60:60 NPK kg/ha with nitrogen applied in 4 splits from planting to flowering',
        'soybean': 'Apply 25:50:25 NPK kg/ha with phosphorus as basal and nitrogen in two splits',
        'mustard': 'Use 80:40:40 NPK kg/ha with half nitrogen at sowing and half at branching stage',
        'groundnut': 'Apply 25:50:25 NPK kg/ha with emphasis on phosphorus for root development',
        'potato': 'Use 120:240:120 NPK kg/ha with half as basal and half as top dressing at 30 days',
        'tomato': 'Apply 150:100:50 NPK kg/ha with nitrogen in three splits during growth stages',
        'onion': 'Use 100:80:50 NPK kg/ha with zinc sulphate 50 kg/ha as basal for bulb development',
        'chilli': 'Apply 90:60:90 NPK kg/ha with nitrogen in three splits at 30, 60, and 90 days',
        'brinjal': 'Use 100:50:30 NPK kg/ha with half nitrogen as basal and half at flowering stage',
        'cabbage': 'Apply 135:135:135 NPK kg/ha with half as basal and half at 30-45 days after planting',
        'cauliflower': 'Use 135:135:135 NPK kg/ha in hills or 100:100:50 NPK kg/ha in plains',
        'carrot': 'Apply 135:135:135 NPK kg/ha with zinc sulphate 25 kg/ha as basal for root quality',
        'beetroot': 'Use 120:160:100 NPK kg/ha with half nitrogen as basal and half at 30 days',
        'radish': 'Apply 50:100:50 NPK kg/ha with half nitrogen as basal and half at 30 days',
        'bittergourd': 'Use 100:120:120 NPK g/pit with 10g nitrogen at 30 days after sowing',
        'papaya': 'Apply 300:200:200 NPK g/plant/year in 3-4 splits during growing season'
    }
    
    return jsonify({
        "recommendation": recommendations.get(crop, "Standard NPK 100:50:50 kg/ha"),
        "method": "Split application recommended for optimal nutrient uptake and reduced losses"
    })

# AI Chat
@app.route('/api/chat', methods=['POST'])
def ai_chat():
    data = request.json
    message = data.get('message', '').lower()
    if 'weather' in message:
        reply = "I can provide weather for Agra, Delhi, Mumbai, and more. Use the weather tab!"
    else:
        reply = "How can I help with farming today?"
    return jsonify({"reply": reply})

# Static files
@app.route('/static/<path:filename>')
def static_files(filename):
    return app.send_static_file(filename)

@app.route('/manifest.json')
def manifest():
    return app.send_static_file('manifest.json')

@app.route('/service-worker.js')
def service_worker():
    return app.send_static_file('service-worker.js')

# Health check
@app.route('/health')
def health():
    return jsonify({"status": "healthy", "version": "2.0"})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 5000)), debug=True)

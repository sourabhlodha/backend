from flask import Flask, jsonify, request
from flask_cors import CORS, cross_origin

import requests

app = Flask(__name__)
cors = CORS(app)

app.config['CORS_HEADERS'] = 'Content-Type'


@app.route("/")
@cross_origin()
def home():
    return "Hello, World!"

API_KEY = 'fe3816a10421d9ca3879ad3a56c40947'
BASE_URL = 'http://api.openweathermap.org/data/2.5/weather'

@app.route('/weather', methods=['GET'])
@cross_origin()
def get_weather():
    user_location = request.args.get('zipcode')
    cities = request.args.getlist('city')

    if not user_location and not cities:
        return jsonify({'error': 'At least one of location or cities parameter is required'}), 400

    weather_data = {}

    # Fetch weather for user's location
    if user_location:
        user_weather = fetch_weather_by_location(user_location)
        if 'error' in user_weather:
            pass
        else:
            weather_data['user_location'] = user_weather

    # Fetch weather for chosen cities
    if cities:
        city_weathers = {}
        for city in cities:
            city_weather = fetch_weather_by_location(city)
            if 'error' in city_weather:
                pass
            else:
                city_weathers[city] = city_weather
        weather_data['chosen_cities'] = city_weathers

    return jsonify(weather_data), 200

def fetch_weather_by_location(location):
    params = {
        'q': location,
        'appid': API_KEY,
        'units': 'metric'  # Change units as needed (metric, imperial, standard)
    }

    try:
        response = requests.get(BASE_URL, params=params)
        data = response.json()
        if response.status_code == 200:
            return data
        else:
            return {'error': data['message']}
    except Exception as e:
        return {'error': str(e)}

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000, debug=True)

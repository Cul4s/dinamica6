from flask import Flask, jsonify
import requests
import redis
import json

app_a = Flask(__name__)


r = redis.Redis(host='localhost', port=6379, db=0, decode_responses=True)

API_B_URL = "http://localhost:5001/weather"

def get_recommendation(temp):
    if temp > 30:
        return "Tá Calor! Tome água e use protetor solar."
    elif 15 <= temp <= 30:
        return "Hoje tá tranquilo..."
    else:
        return "Tá frio! Bota blusa!"

@app_a.route('/recommendation/<city>')
def get_recommendation_for_city(city):

    city_key = city.lower().replace(" ", "")
    cached_data = r.get(city_key)

    if cached_data:
       
        weather_info = json.loads(cached_data)
        cache_status = "hit"
    else:
        try:
         
            response = requests.get(f"{API_B_URL}/{city}")
            response.raise_for_status() 
            weather_info = response.json()
            
         
            r.setex(city_key, 60, json.dumps(weather_info))
            cache_status = "miss"
        except requests.exceptions.RequestException as e:
            return jsonify({
                "error": "Erro ao consultar serviço de clima",
                "details": str(e)
            }), 500

 
    return jsonify({
        "cidade": weather_info["Cidade"],
        "temperatura": weather_info["Temperatura"],
        "recomendacao": get_recommendation(weather_info["Temperatura"]),
        "cache": cache_status
    })

if __name__ == '__main__':
    app_a.run(port=5000, debug=True)
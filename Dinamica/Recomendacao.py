from flask import Flask, jsonify
import requests

app_a = Flask(__name__)

API_B_URL = "http://localhost:5001/weather"

def get_recommendation(temp):
    if temp > 30:
        return "Ta Calor! Tome bastante água e passe o Protetor Solar."
    elif 15 <= temp <= 30:
        return "Hoje ta tranquilo..."
    else:
        return "Ta frio! Bota Blusa!!!"

@app_a.route('/recommendation/<city>', methods=['GET'])
def get_recommendation_for_city(city):
    try:
        response = requests.get(f"{API_B_URL}/{city}")
        weather_info = response.json()
        
        temp = weather_info['Temperatura']
        
        recommendation = get_recommendation(temp)
        
        return jsonify({
            "Cidade": weather_info['Cidade'],
            "Clima": temp,
            "Unidade": weather_info['Unidade'],
            "Recomendacao": recommendation
        })
    except requests.exceptions.RequestException as e:
        return jsonify({
            "error": "Não foi possível obter dados do clima",
            "details": str(e)
        }), 500

if __name__ == '__main__':
    app_a.run(port=5000, debug=True)
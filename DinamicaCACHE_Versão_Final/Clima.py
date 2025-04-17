from flask import Flask, jsonify
app_b = Flask(__name__)


weather_data = {
    "curitiba": {"Cidade": "Curitiba", "Temperatura": 17, "Unidade": "Celsius"},
    "lapa": {"Cidade": "Lapa", "Temperatura": 22, "Unidade": "Celsius"},
    "itaperucu": {"Cidade": "Itaperuçu", "Temperatura": 27, "Unidade": "Celsius"},
    "araucaria": {"Cidade": "Araucaria", "Temperatura": 24, "Unidade": "Celsius"},
}

@app_b.route('/weather/<city>', methods=["GET"])
def get_weather(city):
    city_lower = city.lower()
    if city_lower in weather_data:
        return jsonify(weather_data[city_lower])
    else:
        return jsonify({"error": "Cidade não encontrada"}), 404

if __name__ == '__main__':
    app_b.run(port=5001, debug=True)
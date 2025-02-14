from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # Разрешаем запросы от любых источников (можно настроить по необходимости)

# Хранилище данных (имитация БД)
clients = {}
recommendations = {}

@app.route("/api/clients", methods=["GET"])
def get_clients():
    return jsonify({"clients": [{"user_id": uid} for uid in clients.keys()]})

@app.route("/api/update_recommendation", methods=["POST"])
def update_recommendation():
    data = request.get_json()
    user_id = data.get("user_id")
    recommendation = data.get("recommendation")
    
    if not user_id or not recommendation:
        return jsonify({"error": "Missing user_id or recommendation"}), 400
    
    recommendations[user_id] = recommendation
    return jsonify({"message": "Recommendation updated successfully"})

@app.route("/api/get_recommendation/<user_id>", methods=["GET"])
def get_recommendation(user_id):
    return jsonify({"recommendation": recommendations.get(user_id, "No recommendation yet")})

@app.route("/")
def home():
    return "Web App is running!", 200

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000)

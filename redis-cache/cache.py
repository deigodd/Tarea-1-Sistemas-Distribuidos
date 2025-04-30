from flask import Flask, request, jsonify
import redis
from pymongo import MongoClient
import os
import json  # Importa json para serialización y deserialización

app = Flask(__name__)

# Redis config
redis_client = redis.Redis(host='redis', port=6379, decode_responses=True)

# Mongo config
try:
    mongo_client = MongoClient('mongodb://admin:admin123@mongo:27017/')
    # Verificar la conexión a la base de datos
    mongo_client.admin.command('ping')  # Esto verifica si MongoDB está accesible
    print("Conexión a MongoDB exitosa.")
except Exception as e:
    print(f"Error al conectar con MongoDB: {e}")
    raise

db = mongo_client['waze_alertas']
collection = db['alertas']

@app.route('/alerts', methods=['GET'])
def get_alerts():
    alert_type = request.args.get('type')
    city = request.args.get('city')

    print(f"Received request for type: {alert_type}, city: {city}")

    if not alert_type or not city:
        return jsonify({"error": "Faltan parámetros 'type' o 'city'"}), 400

    key = f"alert:{alert_type}:{city}"
    cached = redis_client.get(key)

    if cached:
        # Deserializar los datos desde JSON
        return jsonify({"source": "cache", "data": json.loads(cached)})

    # Buscar en Mongo
    result = collection.find_one({"type": alert_type, "city": city}, {"_id": 0})

    if result:
        # Serializar el resultado de Mongo a JSON y guardarlo en Redis
        redis_client.set(key, json.dumps(result))  # TTL de 120 segundos
        return jsonify({"source": "mongo", "data": result})
    else:
        return jsonify({"error": "No se encontraron datos"}), 404

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)

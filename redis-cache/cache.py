import redis

redis_client = redis.Redis(host='127.0.0.1', port=6379, decode_responses=True)
try:
    redis_client.ping()
    print("Conexión exitosa a Redis")
except redis.exceptions.ConnectionError as e:
    print("No se pudo conectar a Redis:", e)

import redis
import random
import time
import logging
from datetime import datetime
import os

if not os.path.exists('request'):
    os.makedirs('request')

# Configuración de logs
logging.basicConfig(
    filename='request/request_wazer_logs.txt',
    level=logging.INFO,
    format='%(asctime)s - %(message)s'
)

redis_client = redis.Redis(host='redis', port=6379, decode_responses=True)

TYPES = ['HAZARD', 'ROAD_CLOSED', 'POLICE']
CITIES = [
    'Santiago', 'Maipú', 'Providencia', 'Estación Central', 'Quinta Normal',
    'Cerro Navia', 'Recoleta', 'Pudahuel', 'Peñalolén', 'Ñuñoa'
]

hit_count = 0
miss_count = 0
total_requests = 0
cached_keys = set()
non_cached_keys = set()

# Política de ingreso: ¿debería cachearse este tipo de alerta y ciudad?
def should_cache(alert_type, city):
    # Cacheamos solo alertas HAZARD o si la ciudad es clave
    return alert_type == 'HAZARD' or city in ['Santiago', 'Maipú', 'Providencia', 'Ñuñoa', 'Peñalolén']

# Política de TTL: más corto para alertas críticas
def get_ttl(alert_type):
    if alert_type in ['ROAD_CLOSED', 'POLICE']:
        return 10  # 10 segundos para ROAD_CLOSED o POLICE
    return 30  # 30 segundos para HAZARD

def main():
    global hit_count, miss_count, total_requests

    start_time = time.time()
    duration = 30  # duración total reducida a 30 segundos

    while time.time() - start_time < duration:
        alert_type = random.choice(TYPES)
        city = random.choice(CITIES)

        key = f"alert:{alert_type}:{city}"
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        data = redis_client.get(key)

        total_requests += 1

        if data:
            hit_count += 1
            cached_keys.add(key)
            log_message = f"[CACHE HIT] {alert_type} in {city} at {current_time}: {data}"
            print(log_message)
            logging.info(log_message)
        else:
            miss_count += 1
            non_cached_keys.add(key)
            log_message = f"[CACHE MISS] {alert_type} in {city} at {current_time}, fetching from database..."
            print(log_message)
            logging.info(log_message)

            data = f"Data for {alert_type} in {city}"

            if should_cache(alert_type, city):
                ttl = get_ttl(alert_type)
                redis_client.setex(key, ttl, data)
                log_message = f"[CACHE STORE] {alert_type} in {city} at {current_time}: {data} | TTL: {ttl}s"
                print(log_message)
                logging.info(log_message)

        if total_requests % 10 == 0:
            hit_rate = (hit_count / total_requests) * 100
            miss_rate = (miss_count / total_requests) * 100
            stats_message = (
                f"Total Requests: {total_requests} | Hits: {hit_count} | Misses: {miss_count} | "
                f"Hit Rate: {hit_rate:.2f}% | Miss Rate: {miss_rate:.2f}%\n"
                f"Currently Cached Keys ({len(cached_keys)}): {list(cached_keys)}\n"
                f"Non-Cached Keys ({len(non_cached_keys)}): {list(non_cached_keys)}"
            )
            print(stats_message)
            logging.info(stats_message)

        time.sleep(0.3)  # consultas cada 300ms (más rápido)

    final_stats_message = (
        f"Final Stats after {duration} seconds: Total Requests: {total_requests} | Hits: {hit_count} | Misses: {miss_count} | "
        f"Hit Rate: {(hit_count / total_requests) * 100:.2f}% | Miss Rate: {(miss_count / total_requests) * 100:.2f}%\n"
        f"Final Cached Keys ({len(cached_keys)}): {list(cached_keys)}\n"
        f"Final Non-Cached Keys ({len(non_cached_keys)}): {list(non_cached_keys)}"
    )
    print(final_stats_message)
    logging.info(final_stats_message)

if __name__ == "__main__":
    main()

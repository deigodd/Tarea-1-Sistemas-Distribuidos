import random
import time
import logging
import os
import requests
from datetime import datetime

if not os.path.exists('request'):
    os.makedirs('request')

# Configuración de logs
logging.basicConfig(
    filename='request/request_wazer_logs.txt', 
    level=logging.INFO,  
    format='%(asctime)s - %(message)s'  
)

TYPES = ['HAZARD', 'ROAD_CLOSED', 'POLICE']
CITIES = [
    'Santiago', 'Maipú', 'Providencia', 'Estación Central', 'Quinta Normal',
    'Cerro Navia', 'Recoleta', 'Pudahuel', 'Peñalolén', 'Ñuñoa'
]

hit_count = 0
miss_count = 0
total_requests = 0

# Dirección del backend Flask (servicio 'cache' en docker-compose)
BACKEND_URL = "http://redis-cache:5000/alerts"

def main():
    global hit_count, miss_count, total_requests

    start_time = time.time()
    duration = 60  # segundos

    while time.time() - start_time < duration:
        alert_type = random.choice(TYPES)
        city = random.choice(CITIES)

        params = {"type": alert_type, "city": city}

        try:
            response = requests.get(BACKEND_URL, params=params)
            if response.status_code == 200:
                result = response.json()
                source = result.get("source", "unknown")
                total_requests += 1
                current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

                if source == "cache":
                    hit_count += 1
                    log = f"[CACHE HIT] {alert_type} in {city} at {current_time}"
                else:
                    miss_count += 1
                    log = f"[CACHE MISS] {alert_type} in {city} at {current_time}"

                print(log)
                logging.info(log)

                if total_requests % 10 == 0:
                    hit_rate = (hit_count / total_requests) * 100
                    miss_rate = (miss_count / total_requests) * 100
                    stats = f"Total Requests: {total_requests} | Hits: {hit_count} | Misses: {miss_count} | Hit Rate: {hit_rate:.2f}% | Miss Rate: {miss_rate:.2f}%"
                    print(stats)
                    logging.info(stats)
            else:
                logging.warning(f"❌ Error {response.status_code} for {alert_type} in {city}")
        except Exception as e:
            logging.error(f"💥 Exception during request: {e}")

        time.sleep(1)

    final_stats = f"Final Stats after 1 minute: Total Requests: {total_requests} | Hits: {hit_count} | Misses: {miss_count} | Hit Rate: {(hit_count / total_requests) * 100:.2f}% | Miss Rate: {(miss_count / total_requests) * 100:.2f}%"
    print(final_stats)
    logging.info(final_stats)

if __name__ == "__main__":
    main()

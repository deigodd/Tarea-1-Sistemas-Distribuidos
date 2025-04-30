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

hit_count = 0
miss_count = 0
total_requests = 0

# Dirección del backend Flask (servicio 'cache' en docker-compose)
BACKEND_URL = "http://redis-cache:5000/alerts"
ALL_IDS_URL = "http://redis-cache:5000/alerts/ids"  # Asegúrate de tener este endpoint

def fetch_random_ids(sample_size=100):
    try:
        response = requests.get(ALL_IDS_URL)
        if response.status_code == 200:
            all_ids = response.json().get("ids", [])
            return random.sample(all_ids, sample_size)  # Selecciona 100 ids aleatorios
        else:
            logging.error(f"❌ Error fetching IDs: {response.status_code}")
            return []
    except Exception as e:
        logging.error(f"💥 Exception fetching IDs: {e}")
        return []

def main():
    global hit_count, miss_count, total_requests

    # Paso 1: obtener 100 IDs aleatorios
    selected_ids = fetch_random_ids(100)
    if not selected_ids:
        print("No se pudieron obtener los IDs.")
        return
    print (f"IDs seleccionados: {selected_ids}")
    start_time = time.time()
    duration = 60  # segundos

    while time.time() - start_time < duration:
        _id = random.choice(selected_ids)
        params = {"id": _id}  # Asegúrate de que el backend acepte 'id' como parámetro

        try:
            response = requests.get(BACKEND_URL, params=params)
            if response.status_code == 200:
                result = response.json()
                source = result.get("source", "unknown")
                total_requests += 1
                current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

                if source == "cache":
                    hit_count += 1
                    log = f"[CACHE HIT] id={_id} at {current_time}"
                else:
                    miss_count += 1
                    log = f"[CACHE MISS] id={_id} at {current_time}"

                print(log)
                logging.info(log)

                if total_requests % 10 == 0:
                    hit_rate = (hit_count / total_requests) * 100
                    miss_rate = (miss_count / total_requests) * 100
                    stats = f"Total Requests: {total_requests} | Hits: {hit_count} | Misses: {miss_count} | Hit Rate: {hit_rate:.2f}% | Miss Rate: {miss_rate:.2f}%"
                    print(stats)
                    logging.info(stats)
            else:
                logging.warning(f"❌ Error {response.status_code} for id={_id}")
        except Exception as e:
            logging.error(f"💥 Exception during request: {e}")

        time.sleep(1)

    final_stats = f"Final Stats after 1 minute: Total Requests: {total_requests} | Hits: {hit_count} | Misses: {miss_count} | Hit Rate: {(hit_count / total_requests) * 100:.2f}% | Miss Rate: {(miss_count / total_requests) * 100:.2f}%"
    print(final_stats)
    logging.info(final_stats)

if __name__ == "__main__":
    main()

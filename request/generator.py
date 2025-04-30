import random
import time
import logging
import os
import requests
from datetime import datetime
from collections import defaultdict
import numpy as np  # Asegúrate de tener numpy instalado: pip install numpy

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
id_access_count = defaultdict(int)

# URLs del backend
BACKEND_URL = "http://redis-cache:5000/alerts"
ALL_IDS_URL = "http://redis-cache:5000/alerts/ids"

# Condicional para cambiar la distribución
CONDITIONAL_DISTRIBUTION = 1

def fetch_random_ids(sample_size=100):
    try:
        response = requests.get(ALL_IDS_URL)
        if response.status_code == 200:
            all_ids = response.json().get("ids", [])
            return random.sample(all_ids, sample_size)
        else:
            logging.error(f"❌ Error fetching IDs: {response.status_code}")
            return []
    except Exception as e:
        logging.error(f"💥 Exception fetching IDs: {e}")
        return []

def generate_requests_plan(selected_ids, min_repeats=1, max_repeats=3, target_length=60):
    requests_plan = []
    random.shuffle(selected_ids)  # <--- Esto aleatoriza el orden
    while len(requests_plan) < target_length:
        for _id in selected_ids:
            n = random.randint(min_repeats, max_repeats)
            requests_plan.extend([_id] * n)
            if len(requests_plan) >= target_length:
                break
    return requests_plan[:target_length]


def main():
    global hit_count, miss_count, total_requests

    # Obtener 100 IDs aleatorios
    selected_ids = fetch_random_ids(1000)
    if not selected_ids:
        print("No se pudieron obtener los IDs.")
        return
    print(f"✅ IDs seleccionados: {selected_ids}")

    # Bucle indefinido con generación de nuevos planes
    while True:
        requests_plan = generate_requests_plan(selected_ids, min_repeats=1, max_repeats=3, target_length=60)
        if CONDITIONAL_DISTRIBUTION == 1:
        # Generar el tiempo de espera usando distribución uniforme
            for _id in requests_plan:
                id_access_count[_id] += 1
                total_requests += 1

                params = {"id": _id}

                try:
                    response = requests.get(BACKEND_URL, params=params)
                    if response.status_code == 200:
                        result = response.json()
                        source = result.get("source", "unknown")
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

                # Tiempo de espera usando distribución uniforme entre 0.1 y 1 segundo
                wait_time = random.uniform(0.1, 1)  # Genera un tiempo de espera entre 0.1 y 1 segundo
                time.sleep(wait_time)  # Sleep en segundos
        else:
            # Generar el tiempo de espera usando distribución exponencial (media = 0.5s)
            for _id in requests_plan:
                id_access_count[_id] += 1
                total_requests += 1

                params = {"id": _id}

                try:
                    response = requests.get(BACKEND_URL, params=params)
                    if response.status_code == 200:
                        result = response.json()
                        source = result.get("source", "unknown")
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

                # Tiempo de espera usando distribución exponencial (media = 0.5s)
                wait_time = np.random.exponential(scale=0.5)
                time.sleep(wait_time)


        # Al finalizar el plan, mostrar resumen y continuar
        print("\n🔄 Generando nuevo ciclo de peticiones...\n")
        logging.info("🔄 Generando nuevo ciclo de peticiones...")

        # Puedes agregar un pequeño delay si quieres entre ciclos
        time.sleep(2)

if __name__ == "__main__":
    main()

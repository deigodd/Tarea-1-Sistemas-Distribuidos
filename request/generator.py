import redis
import random
import time
import logging
from datetime import datetime
import os

if not os.path.exists('request'):
    os.makedirs('request')

# conf para los logs
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

def main():
    global hit_count, miss_count, total_requests

    start_time = time.time()  
    duration = 60  

    while time.time() - start_time < duration:
        alert_type = random.choice(TYPES)
        city = random.choice(CITIES)

        key = f"alert:{alert_type}:{city}"

        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S") 
        data = redis_client.get(key)

        total_requests += 1  

        if data:
            # contador de hits
            hit_count += 1  
            log_message = f"[CACHE HIT] {alert_type} in {city} at {current_time}: {data}"
            print(log_message)
            logging.info(log_message)
        else:
            # contador de misses
            miss_count += 1 
            log_message = f"[CACHE MISS] {alert_type} in {city} at {current_time}, fetching from database..."
            print(log_message)
            logging.info(log_message)

            data = f"Data for {alert_type} in {city}"
            redis_client.setex(key, 120, data)  
            log_message = f"[CACHE STORE] {alert_type} in {city} at {current_time}: {data}"
            print(log_message)
            logging.info(log_message)

        if total_requests % 10 == 0:
            hit_rate = (hit_count / total_requests) * 100
            miss_rate = (miss_count / total_requests) * 100
            stats_message = f"Total Requests: {total_requests} | Hits: {hit_count} | Misses: {miss_count} | Hit Rate: {hit_rate:.2f}% | Miss Rate: {miss_rate:.2f}%"
            print(stats_message)
            logging.info(stats_message)

        time.sleep(1)  

    # Logs para dps hacer metricas
    final_stats_message = f"Final Stats after 1 minute: Total Requests: {total_requests} | Hits: {hit_count} | Misses: {miss_count} | Hit Rate: {(hit_count / total_requests) * 100:.2f}% | Miss Rate: {(miss_count / total_requests) * 100:.2f}%"
    print(final_stats_message)
    logging.info(final_stats_message)

if __name__ == "__main__":
    main()

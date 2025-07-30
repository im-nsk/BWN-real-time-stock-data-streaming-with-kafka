from kafka import KafkaProducer
import requests
import json
import time
from utils.config_loader import load_config

config = load_config()

producer = KafkaProducer(
    bootstrap_servers = config["kafka"]["bootstrap_server"],
    value_serializer = lambda v: json.dumps(v).encode("utf-8")
)

def fetch_stock_data(API_URL):
    batch_id = 0
    while True and batch_id <= 100: # 1 For quick testing
        response = requests.get(API_URL)
        if response.status_code == 200:
            stock_data = response.json()
            producer.send(kafka_topic, value=stock_data)
            batch_id += 1
            print(f"📩 Sent: {stock_data}")
            time.sleep(30)


if __name__ == "__main__":

    function = 'TIME_SERIES_INTRADAY'
    outputsize = 'full'
    api_base_url = config["api"]["base_url"]
    api_key = config["api"]["api_key"]
    stock_symbol = config["api"]["symbols"]
    kafka_topic = config["kafka"]["kafka_topic"]
    interval = config["api"]["interval"]
    print("Producer started")
    for sym in stock_symbol:
        api_url = f'{api_base_url}function={function}&symbol={sym}&interval={interval}&outputsize={outputsize}&adjusted=true&apikey={api_key}'
        print(f"Producing stock data to Kafka topic: {kafka_topic}")

        fetch_stock_data(api_url)
    time.sleep(30)
from kafka import KafkaConsumer
import json
import time
import boto3
import io
import pandas as pd
import pyarrow as pa
import pyarrow.parquet as pq
from utils.config_loader import load_config

config = load_config()

consumer = KafkaConsumer(
    config["kafka"]["kafka_topic"],
    bootstrap_servers='localhost:9092',
    value_deserializer=lambda v: json.loads(v.decode('utf-8'))
)

s3_client = boto3.client("s3",
    aws_access_key_id=config["aws"]["access_key_id"],
    aws_secret_access_key=config["aws"]["secret_access_key"],
    region_name = config["aws"]["region"]   
)

def load_to_s3(data, batch_id, s3_src_bucket, s3_prefix):
    if not data:
        return 
    
    df = pd.DataFrame(data)
    file_key = f"{s3_prefix}/stock_batch_{batch_id}_{int(time.time())}.parquet"

    # convert df to parquet in memory
    pa_table = pa.Table.from_pandas(df)
    buffer = io.BytesIO()
    pq.write_table(pa_table, buffer)
    buffer.seek(0)

    # upload to the s3
    s3_client.upload_fileobj(buffer, s3_src_bucket, file_key)

def consume_and_upload(s3_src_bucket, s3_prefix):
    buffer = []
    batch_id = 0
    batch_size = 20  # 1 For quick testing

    for message in consumer:
        buffer.append(message.value)
        print(f"✅ Received: message")

        if len(buffer) >= batch_size:
            batch_id += 1
            print(f"⬆️ Uploading batch {batch_id} with {len(buffer)} messages to S3...")
            load_to_s3(buffer, batch_id, s3_src_bucket, s3_prefix)
            buffer.clear()

if __name__ == "__main__":

    s3_src_bucket = config["aws"]["s3_src_bucket"]
    s3_prefix = config["aws"]["s3_src_prefix"]

    print(f"🔁 Listening to Kafka topic: {config['kafka']['kafka_topic']}")
    
    consume_and_upload(s3_src_bucket, s3_prefix)





# 📈 Stock Data Streaming with Kafka & S3 (Local Setup)

## 🚀 Project Overview

This project simulates **real-time stock price data streaming** using **Apache Kafka (locally installed)**. It fetches intraday stock data from a public API, publishes it to a Kafka topic, and consumes the messages to upload them as **Parquet files** into an **Amazon S3** bucket using `boto3`.

---

## 🧰 Tech Stack

- **Language:** Python
- **Streaming Platform:** Apache Kafka (Local)
- **Cloud Storage:** AWS S3
- **Libraries:**
  - `kafka-python`
  - `requests`
  - `boto3`
  - `pandas`
  - `pyarrow`

---

## 📦 Project Structure

```
01-stock-data-streaming-kafka/
├── producer.py                  # Streams stock data to Kafka
├── consumer.py                  # Consumes Kafka messages and writes to S3
├── utils/
│   └── config_loader.py         # Loads config from JSON
├── config/
│   └── config.json              # API, Kafka, and AWS configurations
└── README.md                    # Project documentation
```

---

## ⚙️ Configuration

All parameters are handled through `config/config.json`. Example:

```json
{
  "api": {
    "base_url": "https://www.alphavantage.co/query?",
    "api_key": "your_api_key",
    "symbols": ["AAPL", "MSFT"],
    "interval": "5min"
  },
  "kafka": {
    "bootstrap_server": "localhost:9092",
    "kafka_topic": "stock-prices"
  },
  "aws": {
    "access_key_id": "your_key",
    "secret_access_key": "your_secret",
    "region": "ap-south-1",
    "s3_src_bucket": "stock-data-bucket",
    "s3_src_prefix": "stream/"
  }
}
```

---

## 🚀 Kafka Producer

**What it does:**

- Builds API URL for each stock symbol
- Fetches intraday stock data using Alpha Vantage API
- Sends JSON response to Kafka topic: `stock-prices`
- Limits to 2 batches per symbol (for testing/demo)
- Sends one record every 30 seconds

> ✅ Uses `kafka-python` to serialize and push data

---

## 🛁 Kafka Consumer

**What it does:**

- Listens to `stock-prices` Kafka topic
- Buffers records up to 1000 messages
- Converts the batch to a Parquet file using PyArrow
- Uploads to AWS S3 (`stock_batch_<id>_<timestamp>.parquet`)

---

## 📁 Sample Output Structure in S3

```
s3://stock-data-bucket/stream/stock_batch_1_1722243172.parquet
```

---

## 🥺 Sample Data Format (from Producer)

```json
{
  "Meta Data": {
    "1. Information": "Intraday (5min) prices",
    "2. Symbol": "AAPL"
  },
  "Time Series (5min)": {
    "2025-07-29 11:30:00": {
      "1. open": "196.83",
      "2. high": "197.39",
      "3. low": "196.75",
      "4. close": "197.32",
      "5. volume": "1034623"
    }
  }
}
```

---

## ▶️ How to Run (Local Environment)

### ✅ Prerequisites

- Apache Kafka and Zookeeper running locally
  - You can start them using:
    ```bash
    bin/zookeeper-server-start.sh config/zookeeper.properties
    bin/kafka-server-start.sh config/server.properties
    ```
- Create the Kafka topic:
  ```bash
  bin/kafka-topics.sh --create --topic stock-prices --bootstrap-server localhost:9092 --partitions 1 --replication-factor 1
  ```
- Python 3.x environment
- Install dependencies:
  ```bash
  pip install kafka-python boto3 requests pandas pyarrow
  ```

### 🏃 Run the Producer

```bash
python producer.py
```

### 🏃 Run the Consumer

```bash
python consumer.py
```

---

## 🧐 Notes & Learnings

- Shows how to implement a real-time pipeline using Kafka
- Hands-on with streaming, batch buffering, and cloud storage
- PyArrow is used for efficient Parquet writing in-memory

---

## 🌱 Future Enhancements

- Normalize nested JSON (e.g., flatten `Time Series`)
- Add schema validation before uploading
- Enhance retry logic and exception handling
- Integrate with Athena/QuickSight for querying

---


```mermaid
flowchart LR
    A[Stock Data Generator<br>Python Script] -->|Simulated JSON Messages| B[Kafka Topic<br>(stock-prices)]
    B --> C[Kafka Consumer<br>(Python Script)]
    C --> D[Data Processor<br>Transformation / Filtering]
    D --> E[Local Storage<br>(CSV/Log File)]

    subgraph "Local Setup"
        B
        C
        D
        E
    end

    style A fill:#ffedcc,stroke:#333,stroke-width:1px
    style B fill:#cce5ff,stroke:#333,stroke-width:1px
    style C fill:#e6ccff,stroke:#333,stroke-width:1px
    style D fill:#d4edda,stroke:#333,stroke-width:1px
    style E fill:#f8d7da,stroke:#333,stroke-width:1px
```


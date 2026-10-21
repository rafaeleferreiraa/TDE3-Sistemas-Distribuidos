import os
import json
import sqlite3
from kafka import KafkaConsumer
from dotenv import load_dotenv
from fraud_detector import FraudDetector

load_dotenv()

BOOTSTRAP_SERVERS = os.getenv("KAFKA_BOOTSTRAP_SERVERS", "localhost:9092")
TOPIC = os.getenv("KAFKA_TOPIC", "transactions")
DB_PATH = os.getenv("DB_PATH", "database/transactions.db")

def init_db():
    os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
    schema_path = os.path.join(os.path.dirname(__file__), "../database/schema.sql")
    
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    with open(schema_path, "r") as f:
        cursor.executescript(f.read())
    conn.commit()
    conn.close()

def save_to_db(tx: dict, fraud_type: str):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO transactions (transaction_id, client_id, amount, city, timestamp, fraud_type)
        VALUES (?, ?, ?, ?, ?, ?)
    ''', (tx['transaction_id'], tx['client_id'], tx['amount'], tx['city'], tx['timestamp'], fraud_type))
    conn.commit()
    conn.close()

def run_consumer():
    init_db()
    detector = FraudDetector()

    consumer = KafkaConsumer(
        TOPIC,
        bootstrap_servers=[BOOTSTRAP_SERVERS],
        value_deserializer=lambda m: json.loads(m.decode('utf-8')),
        auto_offset_reset='latest'
    )

    print(f"📥 Consumidor escutando o tópico '{TOPIC}' e gravando em '{DB_PATH}'...")

    for msg in consumer:
        tx = msg.value
        fraud_type = detector.process_transaction(tx)
        save_to_db(tx, fraud_type)

        if fraud_type != "OK":
            print(f"\033[91m[ALERTA DE FRAUDE - {fraud_type}]\033[0m Cliente: {tx['client_id']} | R${tx['amount']} | Cidade: {tx['city']}")
        else:
            print(f"[OK] ID: {tx['transaction_id']} | Cliente: {tx['client_id']} | R${tx['amount']}")

if __name__ == "__main__":
    run_consumer()
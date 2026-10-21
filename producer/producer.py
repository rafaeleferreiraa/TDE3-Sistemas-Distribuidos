import os
import json
import time
from kafka import KafkaProducer
from dotenv import load_dotenv
from transaction_generator import generate_transaction

load_dotenv()

BOOTSTRAP_SERVERS = os.getenv("KAFKA_BOOTSTRAP_SERVERS", "localhost:9092")
TOPIC = os.getenv("KAFKA_TOPIC", "transactions")

def run_producer():
    producer = KafkaProducer(
        bootstrap_servers=[BOOTSTRAP_SERVERS],
        value_serializer=lambda v: json.dumps(v).encode('utf-8')
    )

    print(f"🚀 Producer iniciado. Enviando mensagens a cada 3s para o tópico '{TOPIC}'...")

    try:
        while True:
            tx = generate_transaction()
            producer.send(TOPIC, value=tx)
            print(f"[PRODUCER] Transação enviada: {tx['transaction_id']} | Cliente: {tx['client_id']} | Valor: R${tx['amount']} | Cidade: {tx['city']}")
            time.sleep(3)
    except KeyboardInterrupt:
        print("\n🛑 Producer encerrado.")
    finally:
        producer.close()

if __name__ == "__main__":
    run_producer()
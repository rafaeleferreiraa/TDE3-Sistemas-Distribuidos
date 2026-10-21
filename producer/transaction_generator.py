import random
import time
from uuid import uuid4

CLIENT_IDS = [f"cli_{i:03d}" for i in range(1, 6)]
CITIES = ["São Paulo", "Rio de Janeiro", "Curitiba", "Belo Horizonte", "Salvador"]

def generate_transaction() -> dict:
    """Gera uma transação aleatória contendo os campos do padrão estipulado."""
    return {
        "transaction_id": str(uuid4()),
        "client_id": random.choice(CLIENT_IDS),
        "amount": round(random.uniform(10.0, 15000.0), 2),
        "city": random.choice(CITIES),
        "timestamp": int(time.time())
    }
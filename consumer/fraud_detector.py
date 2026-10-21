from collections import defaultdict

class FraudDetector:
    def __init__(self):
        # Histórico em memória: {client_id: [transacao_1, transacao_2, ...]}
        self.history = defaultdict(list)

    def process_transaction(self, tx: dict) -> str:
        client_id = tx['client_id']
        current_time = tx['timestamp']
        frauds = []

        # Limpa histórico antigo (mantém apenas os últimos 10 minutos = 600 segundos)
        self.history[client_id] = [
            t for t in self.history[client_id]
            if current_time - t['timestamp'] <= 600
        ]

        # Case Alto Valor: amount >= 10000
        if tx['amount'] >= 10000:
            frauds.append("ALTO_VALOR")

        # Adiciona transação atual ao histórico do cliente
        self.history[client_id].append(tx)
        client_txs = self.history[client_id]

        # Case Tempo: 4 transações em menos de 60 segundos
        txs_last_60s = [t for t in client_txs if current_time - t['timestamp'] < 60]
        if len(txs_last_60s) >= 4:
            frauds.append("TEMPO_60s")

        # Case GEO: 2 cidades diferentes no período de 10 minutos
        cities_last_10m = set(t['city'] for t in client_txs)
        if len(cities_last_10m) >= 2:
            frauds.append("GEO_10m")

        return ",".join(frauds) if frauds else "OK"
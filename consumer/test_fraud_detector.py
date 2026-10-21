from fraud_detector import FraudDetector

def test_alto_valor():
    detector = FraudDetector()
    tx = {"transaction_id": "1", "client_id": "c1", "amount": 10000.0, "city": "SP", "timestamp": 1000}
    assert detector.process_transaction(tx) == "ALTO_VALOR"

def test_tempo_60s():
    detector = FraudDetector()
    c_id = "c2"
    
    # 3 transações normais em 30s
    for i in range(3):
        detector.process_transaction({"transaction_id": str(i), "client_id": c_id, "amount": 10.0, "city": "SP", "timestamp": 1000 + i})
    
    # 4ª transação dentro dos 60s
    tx4 = {"transaction_id": "3", "client_id": c_id, "amount": 10.0, "city": "SP", "timestamp": 1010}
    result = detector.process_transaction(tx4)
    assert "TEMPO_60s" in result

def test_geo_10m():
    detector = FraudDetector()
    c_id = "c3"
    
    detector.process_transaction({"transaction_id": "1", "client_id": c_id, "amount": 50.0, "city": "São Paulo", "timestamp": 1000})
    tx2 = {"transaction_id": "2", "client_id": c_id, "amount": 50.0, "city": "Rio de Janeiro", "timestamp": 1200}
    
    result = detector.process_transaction(tx2)
    assert "GEO_10m" in result
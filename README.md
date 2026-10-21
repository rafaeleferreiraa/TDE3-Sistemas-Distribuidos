# 🚨 TDE 03 - Sistema de Detecção de Fraudes em Tempo Real com Apache Kafka

Projeto desenvolvido para a disciplina de Sistemas Distribuídos / Processamento em Tempo Real (TDE 03). O objetivo é simular o fluxo de transações financeiras e aplicar regras de negócio em tempo real para identificação de possíveis fraudes utilizando o **Apache Kafka** e **Python**.

---

## 📐 Arquitetura da Solução

O sistema é dividido em três componentes principais desacoplados:

1. **Producer (Produtor):** Simula e envia transações aleatórias em formato JSON para o tópico `transactions` do Kafka a cada 3 segundos.
2. **Kafka Broker:** Atua como o barramento de mensagens para streaming de dados em tempo real.
3. **Consumer (Consumidor):** Consome as mensagens do Kafka em tempo real, avalia o histórico recente do cliente em memória para identificar padrões suspeitos e persiste todas as transações (com ou sem flag de fraude) em um banco de dados SQLite.

## 🛠️ Tecnologias Utilizadas

- **Linguagem:** Python 3.10+
- **Mensageria:** Apache Kafka & Zookeeper (via Docker)
- **Banco de Dados:** SQLite
- **Biblioteca Kafka:** `kafka-python`
- **Testes Unitários:** `pytest`

---

## 📝 Padrão da Transação (JSON)

Todas as transações enviadas e processadas seguem a seguinte estrutura de dados:

```json
{
  "transaction_id": "a3b8c910-1234-5678-9abc-def123456789",
  "client_id": "cli_002",
  "amount": 12500.50,
  "city": "São Paulo",
  "timestamp": 1729532400
}
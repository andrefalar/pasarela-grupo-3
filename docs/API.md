# API Documentation

## Message Broker — `http://<broker-ip>:8001`

Receives payment requests from the shop and queues them.

### POST /queue
Enqueue a payment. Both field formats are accepted and equivalent:

```json
{ "sender_id": "ACC-001", "receiver_id": "ACC-002", "amount": 150000.0 }
```
```json
{ "from": "ACC-001", "to": "ACC-002", "amount": 150000.0 }
```

**Response `201`:**
```json
{ "id": "f7c3a1e2-..." }
```

### GET /queue/next
Dequeue the next pending payment (consumed by the pasarela). Returns `null` if empty.

```json
{ "id": "f7c3a1e2-...", "sender_id": "ACC-001", "receiver_id": "ACC-002", "amount": 150000.0 }
```

---

## Pasarela — `http://<pasarela-ip>:8002`

Polls the broker every second and forwards each item to the bank.

**Payload sent to bank (`POST {BANK_URL}`):**
```json
{
  "transaction_id": "f7c3a1e2-...",
  "sender_id": "ACC-001",
  "receiver_id": "ACC-002",
  "amount": 150000.0
}
```

---

## LAN Deployment

Each team runs their service on their own machine. Set the URLs via environment variables before starting:

```bash
# On the pasarela machine
set BROKER_URL=http://<broker-machine-ip>:8001
set BANK_URL=http://<bank-machine-ip>:9000/transfers

uvicorn pasarela.main:app --host 0.0.0.0 --port 8002
```

```bash
# On the broker machine
uvicorn broker.main:app --host 0.0.0.0 --port 8001
```

`--host 0.0.0.0` makes the service reachable from other machines on the LAN.

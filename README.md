# pasarela-grupo-3
Parcial de Arquisoft

Two FastAPI microservices:

- **broker/** — receives payments from the shop, queues them.
- **pasarela/** — polls the broker every second, reformats, and forwards to the bank.

See [docs/API.md](docs/API.md) for endpoint details.

## Run (LAN deployment)

```bash
pip install -r requirements.txt
```

**Broker machine:**
```bash
uvicorn broker.main:app --host 0.0.0.0 --port 8001
```

**Pasarela machine:**
```bash
set BROKER_URL=http://<broker-ip>:8001
set BANK_URL=http://<bank-ip>:9000/transfers
uvicorn pasarela.main:app --host 0.0.0.0 --port 8002
```

Replace `<broker-ip>` and `<bank-ip>` with the actual LAN IP addresses.

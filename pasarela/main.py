import asyncio
import os
from contextlib import asynccontextmanager

import httpx
from fastapi import FastAPI

BROKER_URL = os.environ.get("BROKER_URL", "http://localhost:8001")
BANK_URL = os.environ.get("BANK_URL", "http://localhost:9000/transfers")


async def poll_and_forward():
    while True:
        try:
            async with httpx.AsyncClient() as client:
                resp = await client.get(f"{BROKER_URL}/queue/next")
                item = resp.json()
                if item:
                    bank_payload = {
                        "sender_id": item["sender_id"],
                        "receiver_id": item["receiver_id"],
                        "amount": item["amount"],
                        "transaction_id": item["id"],
                    }
                    await client.post(BANK_URL, json=bank_payload)
        except Exception:
            pass
        await asyncio.sleep(1)


@asynccontextmanager
async def lifespan(app: FastAPI):
    task = asyncio.create_task(poll_and_forward())
    yield
    task.cancel()


app = FastAPI(title="Pasarela", lifespan=lifespan)

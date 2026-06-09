from collections import deque
from uuid import uuid4

from fastapi import FastAPI
from pydantic import BaseModel, model_validator

app = FastAPI(title="Message Broker")

_queue: deque = deque()


class Payment(BaseModel):
    sender_id: str = ""
    receiver_id: str = ""
    amount: float

    @model_validator(mode="before")
    @classmethod
    def normalize(cls, data):
        # Accept both "from"/"to" and "sender_id"/"receiver_id"
        if "from" in data and not data.get("sender_id"):
            data["sender_id"] = data.pop("from")
        if "to" in data and not data.get("receiver_id"):
            data["receiver_id"] = data.pop("to")
        return data


@app.post("/queue", status_code=201)
def enqueue(payment: Payment):
    item = {
        "id": str(uuid4()),
        "sender_id": payment.sender_id,
        "receiver_id": payment.receiver_id,
        "amount": payment.amount,
    }
    _queue.append(item)
    return {"id": item["id"]}


@app.get("/queue/next")
def dequeue():
    if _queue:
        return _queue.popleft()
    return None

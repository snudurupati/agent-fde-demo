from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
import uvicorn

app = FastAPI(title = "Enterprise CRM API")

# --- DATABASE MOCK ---
orders_db = {
    "ORD-123": {"status": "shipped", "customer": "Sreeram", "total": 150.00},
}

# --- PYDANTIC MODELS (TYpe Safety) ---
class OrderResponse(BaseModel):
    order_id: str
    status: str
    total: float

class RefundRequest(BaseModel):
    order_id: str
    reason: str

class RefundResponse(BaseModel):
    order_id: str
    amount: float

# --- ENDPOINTS ---
@app.get("/orders/{order_id}", response_model=OrderResponse)

async def get_order(order_id: str):
    """Retrieve an order by ID"""
    order = orders_db.get(order_id)
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")
    return OrderResponse(order_id=order, **order

@app.post("/refunds", response_model=RefundResponse)
async def process_refund(refund_request: RefundRequest):
    """Process a refund request"""
    order = orders_db.get(refund_request.order_id)
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")
    return RefundResponse(success=True, message=f"Refunded {request.reason}")

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)  
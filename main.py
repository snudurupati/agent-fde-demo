from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
from typing import Optional, List
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
    success: bool
    message: str
    refunded_amount: float

# --- ENDPOINTS ---
@app.get("/orders/{order_id}", response_model=OrderResponse)
async def get_order(order_id: str):
    """Retrieves order details. Used by the Agent to check status."""
    order = orders_db.get(order_id)
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")
    return OrderResponse(order_id=order_id, **order)

@app.post("/refunds", response_model=RefundResponse)
async def process_refund(request: RefundRequest):
    """Processes a refund. The Agent calls this to take action."""
    if request.order_id not in orders_db:
        raise HTTPException(status_code=404, detail="Order not found")
    
    # Simulate business logic
    order = orders_db[request.order_id]

    return RefundResponse(
        success=True, 
        message=f"Refunded {request.reason}",
        refunded_amount=order['total'] # We fulfill the promise here
    )

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
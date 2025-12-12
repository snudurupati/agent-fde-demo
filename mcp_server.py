from mcp.server.fastmcp import FastMCP

# 1. Initialize FastMCP
# This automatically creates the FastAPI app and SSE endpoint internally.
mcp = FastMCP("enterprise-crm")

# --- DATABASE MOCK ---
orders_db = {
    "ORD-123": {"status": "shipped", "customer": "Sreeram", "total": 150.00},
}

# --- 2. DEFINE TOOLS ---
# ZERO GLUE CODE: We just write Python functions with Type Hints.
# FastMCP inspects 'order_id: str' and builds the tool definition automatically.

@mcp.tool()
def get_order(order_id: str) -> str:
    """Get the status and details of an order by ID."""
    order = orders_db.get(order_id)
    if not order:
        return "Order not found."
    return str(order)

@mcp.tool()
def process_refund(order_id: str, reason: str) -> str:
    """Issue a refund. Requires order ID and a reason."""
    if order_id not in orders_db:
        return "Order not found."
    return f"Refund processed for {order_id}. Reason: {reason}"

# --- 3. RUN ---
if __name__ == "__main__":
    # This single line runs the Uvicorn server on port 8000
    mcp.run(transport='sse')
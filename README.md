Markdown

# Agentic FDE Demo: Secure AI-to-Enterprise Integration

## Overview
This project is a hands-on demonstration of a "Forward Deployed Engineer (FDE)" architecture. It showcases how to bridge the gap between a deterministic Enterprise System (using **FastAPI** and **Pydantic**) and a probabilistic AI Agent (using **OpenAI Function Calling**).

This architecture mimics a real-world scenario where an AI platform needs to securely query and act upon data residing in a legacy enterprise database.

### Key Technologies
| Component | Technology | Purpose in Architecture |
| :--- | :--- | :--- |
| **Enterprise API** | FastAPI (Python) | The asynchronous, non-blocking backend server hosting the business logic. |
| **Data Validation** | Pydantic | Enforces strict data contracts (schema) for inputs and outputs, preventing data corruption. |
| **The Brain** | OpenAI (GPT-4o) | Acts as the reasoning engine to decide *which* tool to call and *what* arguments to use. |
| **The Glue** | Python (`requests`) | The runtime environment that executes the AI's decision by making the actual HTTP call. |

---

## Architecture Diagram

This diagram illustrates the complete request flow. The user's intention is translated by the LLM into a structured tool call, which is then executed by the Python runtime against the FastAPI server.

```mermaid
sequenceDiagram
    participant U as 👤 User
    participant A as 🤖 Python Agent Runtime
    participant L as 🧠 OpenAI LLM
    participant S as 🏢 Enterprise API (FastAPI)
    participant D as 🗄️ Database (Mock)

    U->>A: "Check status of order ORD-123"
    Note over A,L: The Agent is the Orchestrator

    A->>L: Send Prompt + Tool Definitions (JSON Schema)
    L-->>A: Response: Call "get_order" with {"order_id": "ORD-123"}
    Note over A: Agent parses JSON, prepares HTTP request

    A->>S: GET /orders/ORD-123 (HTTP)
    Note over S: Pydantic Validates Request

    S->>D: Query Order Data
    D-->>S: Return Raw Data
    Note over S: Pydantic Validates Response Schema

    S-->>A: Return Structured JSON Response
    A-->>U: Final Answer based on API data
Prerequisites
Python 3.10+: Ensure Python is installed and accessible via terminal.

OpenAI API Key: You need a valid API key from platform.openai.com.

Setup & Installation (Do This First)
Clone or Create Project Folder

Bash

mkdir agent-fde-demo
cd agent-fde-demo
Create and Activate Virtual Environment

Bash

# Create venv
python3 -m venv venv

# Activate it (Mac/Linux)
source venv/bin/activate
# Activate it (Windows)
# .\venv\Scripts\activate
Install Dependencies

Bash

pip install fastapi uvicorn pydantic openai requests
Set OpenAI API Key

Mac/Linux:

Bash

export OPENAI_API_KEY="sk-your-actual-key-goes-here"
Windows (PowerShell):

PowerShell

$env:OPENAI_API_KEY = "sk-your-actual-key-goes-here"
Running the Demo (The "FDE" Experience)
This demo requires two separate terminal windows running simultaneously to simulate a real Client/Server architecture.

🖥️ Terminal 1: The Enterprise Server (FastAPI)
This represents the backend system with business rules and a database.

Make sure your virtual environment is active (source venv/bin/activate).

Run the server:

Bash

python main.py
Success Confirmation: You should see logs starting with:

Plaintext

INFO:     Started server process [12345]
INFO:     Uvicorn running on [http://0.0.0.0:8000](http://0.0.0.0:8000) (Press CTRL+C to quit)
Leave this terminal window open. Do not close it.

💡 Pro Tip: Open your browser to http://localhost:8000/docs to see the auto-generated Swagger UI. You can test your endpoints manually right from the browser!

🤖 Terminal 2: The AI Agent (Client)
This represents the Agentic AI application that will talk to the server.

Open a new terminal window.

Navigate to the same folder:

Bash

cd agent-fde-demo
Activate the same virtual environment:

Bash

source venv/bin/activate
Ensure your API Key is set in this window too (repeat step 4 from Setup if needed).

Run the agent script:

Bash

python agent.py
Expected Output
If the architecture is working correctly, you will see the full "ReAct" loop in action in Terminal 2:

Plaintext

👤 User: Can you check the status of order ORD-123?
🤖 LLM Thought: I need to call get_order
🔌 Executing API Call: get_order with args {'order_id': 'ORD-123'}
✅ API Result: {'order_id': 'ORD-123', 'status': 'shipped', 'total': 150.0}
Simultaneously, in Terminal 1 (The Server), you will see the incoming request logged:

Plaintext

INFO:     127.0.0.1:58493 - "GET /orders/ORD-123 HTTP/1.1" 200 OK
Key Files
main.py: The FastAPI application. This defines the API endpoints, the mocked database, and the Pydantic data models that serve as the strict contract.

agent.py: The Python client that connects to OpenAI. It defines the Tools (JSON schema) and contains the glue code (requests.get/post) to execute the LLM's instructions against the local API.
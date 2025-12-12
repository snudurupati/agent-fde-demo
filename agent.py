from openai import OpenAI
import json
import os
from dotenv import load_dotenv
import requests

# Load environment variables from a .env file
load_dotenv()

openai_api_key = os.getenv("OPENAI_API_KEY")
client = OpenAI(api_key=openai_api_key)

# --- CONFIGURATION ---
# Try changing this to "junior-agent-secret" to see the Refund fail!
API_TOKEN = os.getenv("API_TOKEN")

# Base Headers that include the Security Token
HEADERS = {
    "Authorization": f"Bearer {API_TOKEN}",
    "Content-Type": "application/json"
}


# 1. Define the Tools (The Schema)
# We now include BOTH "get_order" and "process_refund"
tools = [
    {
        "type": "function",
        "function": {
            "name": "get_order",
            "description": "Get order status and details",
            "parameters": {
                "type": "object",
                "properties": {
                    "order_id": {"type": "string"}
                },
                "required": ["order_id"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "process_refund",
            "description": "Issue a refund for a customer order. Requires a reason.",
            "parameters": {
                "type": "object",
                "properties": {
                    "order_id": {"type": "string"},
                    "reason": {"type": "string"}
                },
                "required": ["order_id", "reason"]
            }
        }
    }
]

# 2. Define the Execution Logic (The "Glue" Code)
def execute_tool_call(tool_call):
    fn_name = tool_call.function.name
    args = json.loads(tool_call.function.arguments)
    
    print(f"🔌 Executing API Call: {fn_name} with args {args}")

    try:
        if fn_name == "get_order":
            # Pass HEADERS here
            response = requests.get(
                f"http://localhost:8000/orders/{args.get('order_id')}",
                headers=HEADERS 
            )
        
        elif fn_name == "process_refund":
            # Pass HEADERS here
            response = requests.post(
                f"http://localhost:8000/refunds", 
                json=args,
                headers=HEADERS
            )
        
        # Handle Security Errors nicely for the LLM
        if response.status_code == 401:
            return "Error: Authentication Failed. Check your token."
        if response.status_code == 403:
            return "Error: Permission Denied. You do not have the scope to perform this action."
            
        return response.json()
            
    except Exception as e:
        return str(e)

# 3. The Agent Loop
def run_agent(user_query):
    print(f"👤 User: {user_query}")
    
    # Step A: Ask LLM what to do
    messages = [{"role": "user", "content": user_query}]
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=messages,
        tools=tools,
        tool_choice="auto" 
    )
    
    # Step B: Check if LLM wants to use a tool
    message = response.choices[0].message
    if message.tool_calls:
        tool_call = message.tool_calls[0]
        print(f"🤖 LLM Thought: I need to call {tool_call.function.name}")
        
        # Step C: Execute the tool (Hit the API)
        api_result = execute_tool_call(tool_call)
        print(f"✅ API Result: {api_result}")
    else:
        print("🤖 LLM Response:", message.content)

# Test Run
if __name__ == "__main__":
    run_agent("Can you check the status of order ORD-123?")
    print("-" * 20)
    run_agent("I need a refund for ORD-123 because it arrived damaged.")

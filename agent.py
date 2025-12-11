from openai import OpenAI
import json

client = OpenAI(api_key="")

#1. Define Tools (The "Schema")
tools = [
    {
        "type": "function",
        "function": {
            "name": "get_order",
            "description": "Get order details by ID",
            "parameters": {
                "type": "object",
                "properties": {
                    "order_id": {
                        "type": "string",
                        "description": "Order ID to retrieve"
                    }
                },
                "required": ["order_id"]
            }
        }
    }
]

#2. Run the Agent Loop
def run_agent(query):
    messages = [{"role": "users", "content": query}]
    response = client.chat.completions.create(
        model="gpt-4o",
        messages=messages,
        tools=tools
    )

    tool_calls = response.choices[0].message.tool_calls[0]
    print(f"🤖 Agent decided to call: {tool_calls.function.name}")
    print(f"📄 With arguments: {tool_calls.function.arguments}")

    #3. Execute the tool
    run_agent("where is my order ORD-123?")
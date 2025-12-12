import asyncio
from mcp.client.sse import sse_client
from mcp.client.session import ClientSession

async def run_agent():
    print("🔌 Connecting to MCP Server...")

    # FIX: We unpack the tuple (read, write) here
    # Previously: as streams -> streams.read (Error)
    # Now:        as (read, write) -> read (Correct)
    async with sse_client("http://localhost:8000/sse") as (read, write):
        
        async with ClientSession(read, write) as session:
            
            # 1. Handshake
            await session.initialize()
            
            # 2. List Tools
            tools = await session.list_tools()
            print(f"✅ Discovered {len(tools.tools)} tools:")
            for t in tools.tools:
                print(f"   - {t.name}: {t.description}")
            
            # 3. Call Tool Test
            print("\n🧪 Executing 'process_refund'...")
            
            result = await session.call_tool(
                "process_refund", 
                arguments={"order_id": "ORD-123", "reason": "damaged"}
            )
            
            print(f"🎉 Server Response: {result.content[0].text}")

if __name__ == "__main__":
    asyncio.run(run_agent())
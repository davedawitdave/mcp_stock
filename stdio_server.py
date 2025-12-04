import asyncio
import base64
from typing import Any, Sequence

from mcp.server import Server
from mcp.server.stdio import stdio_server
import mcp.types as types

# Import only the specific logic requested
from tools_market import (
    get_crypto_price,
    list_common_tickers
)

# Initialize the Server (Main SDK)
app = Server("crypto-market-stdio-server")

# 1. Define the Tools Handler
@app.list_tools()
async def list_tools() -> list[types.Tool]:
    return [
        types.Tool(
            name="get_crypto_price",
            description="Get price for a specific crypto ticker (e.g., 'btc-bitcoin').",
            inputSchema={
                "type": "object",
                "properties": {
                    "ticker": {"type": "string", "description": "CoinPaprika ID (e.g., btc-bitcoin)"}
                },
                "required": ["ticker"]
            }
        ),
        types.Tool(
            name="list_common_tickers",
            description="Get a list of commonly tracked cryptocurrency tickers.",
            inputSchema={"type": "object", "properties": {}}
        ),
    ]

# 2. Define the Execution Handler
@app.call_tool()
async def call_tool(name: str, arguments: Any) -> Sequence[types.TextContent | types.ImageContent | types.EmbeddedResource]:
    try:
        if name == "get_crypto_price":
            # Arguments are passed as a dictionary
            result = await get_crypto_price(arguments["ticker"])
            return [types.TextContent(type="text", text=result)]

        elif name == "list_common_tickers":
            result = await list_common_tickers()
            return [types.TextContent(type="text", text=result)]

        else:
            raise ValueError(f"Unknown tool: {name}")

    except Exception as e:
        return [types.TextContent(type="text", text=f"Error executing tool {name}: {str(e)}")]

async def main():
    # Run the server using stdin/stdout streams
    async with stdio_server() as (read_stream, write_stream):
        await app.run(
            read_stream,
            write_stream,
            app.create_initialization_options()
        )

if __name__ == "__main__":
    asyncio.run(main())
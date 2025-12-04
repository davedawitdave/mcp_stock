from fastmcp import FastMCP
from typing import List
import argparse
from tools_market import (
    get_crypto_price, compare_cryptos, search_cryptocurrency,
    list_common_tickers, get_market_overview, visualize_crypto_comparison
)

mcp = FastMCP(name="crypto-market-http-server")

# register tools
mcp.tool()(get_crypto_price)
mcp.tool()(compare_cryptos)
mcp.tool()(search_cryptocurrency)
mcp.tool()(list_common_tickers)
mcp.tool()(get_market_overview)
mcp.tool()(visualize_crypto_comparison)

#add prompts below
# --- New Tool for System Instruction ---
@mcp.prompt()
async def get_system_instruction() -> str:
    """
    Returns the system instruction/persona for the LLM using this server.
    
    This instruction dictates the model's role when interpreting and utilizing the other tools.
    """
    return (
        "You are a specialized cryptocurrency market analyst. Your primary goal is to use "
        "the provided tools to fetch real-time and historical data on crypto assets. "
        "When responding to user queries, prioritize the use of tool outputs and provide "
        "concise, data-driven analysis and insights."
    )

# --- Tool Stubs (Based on server_http.py imports) ---
# NOTE: These stubs replace the previous yfinance logic to align with the new imports.
# You will need to fill in the actual logic for these functions.



@mcp.prompt()
async def get_market_overview() -> str:
    """Provides a high-level summary of the overall cryptocurrency market sentiment and daily trends."""
    return "Stub: Providing high-level market overview..."
@mcp.prompt
def market_planner_prompt():
    """
    You are a crypto budgeting planner.

    When the user describes a budget plan:
    1. Identify the coin (e.g., btc, eth, sol).
    2. Identify their budget in USD.
    3. Convert coin name to CoinPaprika symbol format.
    4. Call `market_planner` with:
       - symbol: formatted coin
       - budget: extracted number

    If either budget or coin is missing:
    - Ask for clarification.
    """


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--host", default="0.0.0.0")
    parser.add_argument("--port", type=int, default=8000)
    args = parser.parse_args()

    print("Server running for MCP clients only.")
    print("Connect using an MCP client (Cursor, Windsurf, Zed).")
    print(f"Endpoint: http://{args.host}:{args.port}/mcp")

    mcp.run(
        transport="streamable-http",    # or "streamable-http"
        host=args.host,
        port=args.port,
    )

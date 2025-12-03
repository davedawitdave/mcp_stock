from fastmcp import FastMCP
from tools_market import (
    get_crypto_price, compare_cryptos, search_cryptocurrency,
    list_common_tickers, get_market_overview, visualize_crypto_comparison,
    get_system_instruction # Register the new instruction tool
)

# Initialize the FastMCP server for stdio transport and update the name
mcp = FastMCP("crypto-market-stdio-server")

# Register the comprehensive set of crypto market tools and the instruction
# register tools
mcp.tool()(get_crypto_price)
mcp.tool()(compare_cryptos)
mcp.tool()(search_cryptocurrency)
mcp.tool()(list_common_tickers)
mcp.tool()(get_market_overview)
mcp.tool()(visualize_crypto_comparison)

if __name__ == "__main__":
    print("Crypto Market Stdio Server running. Waiting for client input on stdin...")
    mcp.run()
    # Note: No explicit host/port needed for stdio
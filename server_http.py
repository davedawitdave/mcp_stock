from fastmcp import FastMCP
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

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--host", default="0.0.0.0")
    parser.add_argument("--port", type=int, default=8000)
    args = parser.parse_args()

    print("Server running for MCP clients only.")
    print("Connect using an MCP client (Cursor, Windsurf, Zed).")
    print(f"Endpoint: http://{args.host}:{args.port}/mcp")

    mcp.run(
        transport="http",    # or "streamable-http"
        host=args.host,
        port=args.port,
    )

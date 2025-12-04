# Crypto Market MCP Server

A minimal Model Context Protocol (MCP) project exposing cryptocurrency tools using both HTTP and STDIO transports. Designed for easy local testing and future expansion.

---

## Features

* HTTP MCP server for browser-based or remote tools.
* STDIO MCP server for fast local agent integration.
* Market data tools: price lookup, comparison, search, overview, and visualization.
* Compatible with FastMCP ≥ 2.13.2.
* Works with MCP Inspector for GUI interaction.

---

## Project Structure

```
mcp_stock/
│
├── http_server.py
├── stdio_server.py
├── tools_market.py
├── requirements.txt
└── README.md
```

---

## Installation

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

Required packages include:

* fastmcp>=2.13.2
* requests
* pandas
* matplotlib

---

## Running the HTTP MCP Server

```bash
python http_server.py
```

Default endpoint:

```
http://localhost:8000/mcp
```

You can now connect using MCP Inspector.

---

## Using MCP Inspector

Start Inspector:

```bash
npx @modelcontextprotocol/inspector http://localhost:8000/mcp
```

Inspector lets you:

* View available tools.
* Trigger tool calls with JSON inputs.
* Use prompts for natural-language queries.
* Preview generated charts.

---

## Running the STDIO MCP Server

```bash
python stdio_server.py
```

STDIO mode is used by MCP clients or agent frameworks that communicate through stdin/stdout.
It does not have a web UI.

---

## Tools in `tools_market.py`

* **get_system_instruction** – Returns system persona definition.
* **get_crypto_price(ticker)** – Fetch the latest price.
* **compare_cryptos(tickers)** – Compare multiple assets.
* **search_cryptocurrency(query)** – Fuzzy asset lookup.
* **list_common_tickers** – Common crypto symbols.
* **get_market_overview** – Global crypto market summary.
* **visualize_crypto_comparison(tickers)** – Matplotlib comparison chart (visible inside Inspector on HTTP).


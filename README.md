```markdown
# Crypto Market MCP Server

This project exposes a set of cryptocurrency analysis and visualization tools through the Model Context Protocol (MCP).  
It features a clean, single-directory structure and provides two transport methods—HTTP and STDIO—for integration with AI agents.

---

## Key Features

- HTTP MCP Server — Tools exposed over a standard HTTP endpoint.  
- STDIO MCP Server — Tools exposed over stdin/stdout for fast local integration.  
- Crypto market tools — Price lookup, comparison, search, market overview, and chart visualization.  
- Compatible with FastMCP version 2.13.2 or higher.  
- Web Visualization (Inspector UI) available through a command line tool.

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

````

---

## 1. Installation

### Create and activate virtual environment

```bash
python3 -m venv .venv
source .venv/bin/activate
````

### Install dependencies

```bash
pip install -r requirements.txt
```

Required packages include:

* fastmcp>=2.13.2
* requests
* matplotlib
* pandas

---

# 2. Running with Cursor

This project is compatible with the Cursor AI IDE, which can automatically detect and execute MCP servers.

### Step 1 — Open the project in Cursor

1. Launch Cursor
2. Select "Open Folder"
3. Choose the `mcp_stock/` directory

### Step 2 — Run the MCP server inside Cursor

1. Open the file `http_server.py`
2. Press:

```
Ctrl + Shift + R
```

or use the "Run" button in the editor.

Cursor will launch the HTTP server and register it as an MCP provider.

### Expected terminal output

```
Server running on http://0.0.0.0:8000/mcp
Registered as MCP provider: Crypto Market Tools
```

### Optional — Use a custom port

You can configure the run command:

```bash
python http_server.py --port 9000
```

---

## MCP Inspector (Web UI)

To inspect and interact with your tools using a web browser:

```bash
npx @modelcontextprotocol/inspector http://localhost:8000/mcp
```

This interface allows you to view tool schemas, call tools, inspect JSON output, and preview generated charts.

---

## 3. Running the STDIO MCP Server

For local integrations with AI agents or systems expecting STDIO-based MCP:

```bash
python stdio_server.py
```

Note: The STDIO server does not provide a web UI.

---

## 4. Tools Provided in tools_market.py

### get_system_instruction

Returns the system persona: "cryptocurrency market analyst".

### get_crypto_price(ticker)

Fetches the latest price for a specific cryptocurrency.

### compare_cryptos(tickers)

Generates a structured comparison of multiple crypto assets.

### search_cryptocurrency(query)

Performs fuzzy search for cryptocurrency names or tickers.

### list_common_tickers

Returns a list of commonly referenced assets such as BTC, ETH, and SOL.

### get_market_overview

Provides general market statistics and sentiment.

### visualize_crypto_comparison(tickers)

Generates a comparative visualization using Matplotlib.
When running over HTTP, this chart can be inspected through the MCP Inspector UI.

---

```
```

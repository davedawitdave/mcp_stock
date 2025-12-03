import requests
import matplotlib.pyplot as plt
import matplotlib
matplotlib.use('Agg')
from typing import List, Dict, Optional
#from mcp.server.fastmcp import tool
from datetime import datetime
import os

COINPAPRIKA_BASE = "https://api.coinpaprika.com/v1"

class CryptoMarketData:
    """A class to interact with CoinPaprika API for cryptocurrency market data."""
    
    def __init__(self):
        self.base_url = COINPAPRIKA_BASE
    
    def get_market_data(self, ticker: str) -> Dict:
        """
        Fetch real-time market data from CoinPaprika.
        
        Args:
            ticker (str): Cryptocurrency ticker (e.g., 'btc-bitcoin')
            
        Returns:
            Dict: Market data including price, volume, market cap, etc.
        """
        url = f"{self.base_url}/tickers/{ticker}"
        response = requests.get(url, timeout=10)
        
        if response.status_code != 200:
            return {"error": "Failed to fetch data", "status": response.status_code}
        
        return response.json()
    
    def get_formatted_price(self, ticker: str) -> Optional[Dict]:
        """Get formatted price information for a cryptocurrency."""
        data = self.get_market_data(ticker)
        
        if "error" in data:
            return data
        
        quotes = data.get("quotes", {}).get("USD", {})
        
        return {
            "name": data.get("name"),
            "symbol": data.get("symbol"),
            "rank": data.get("rank"),
            "price": quotes.get('price', 0),
            "volume_24h": quotes.get('volume_24h', 0),
            "market_cap": quotes.get('market_cap', 0),
            "percent_change_24h": quotes.get('percent_change_24h', 0),
            "percent_change_7d": quotes.get('percent_change_7d', 0),
            "ath_price": quotes.get('ath_price', 0),
            "last_updated": data.get("last_updated")
        }
    
    def search_crypto(self, search_term: str) -> List[Dict]:
        """Search for cryptocurrencies by name or symbol."""
        url = f"{self.base_url}/coins"
        response = requests.get(url, timeout=10)
        
        if response.status_code != 200:
            return [{"error": "Failed to fetch cryptocurrency list"}]
        
        all_cryptos = response.json()
        search_lower = search_term.lower()
        
        results = [
            crypto for crypto in all_cryptos
            if search_lower in crypto.get("name", "").lower() 
            or search_lower in crypto.get("symbol", "").lower()
        ]
        
        return results[:10]
    
    def create_comparison_chart(self, tickers: List[str], output_path: str = "crypto_comparison.png") -> str:
        """
        Create a visualization chart comparing multiple cryptocurrencies.
        
        Args:
            tickers: List of cryptocurrency tickers
            output_path: Path to save the chart image
            
        Returns:
            Path to the saved chart or error message
        """
        comparison_data = []
        
        for ticker in tickers:
            data = self.get_formatted_price(ticker)
            if data and "error" not in data:
                comparison_data.append(data)
        
        if not comparison_data:
            return "Error: No valid data retrieved for any ticker"
        
        # Create figure with subplots
        fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, figsize=(16, 12))
        fig.suptitle('Cryptocurrency Comparison Dashboard', fontsize=20, fontweight='bold')
        
        names = [coin['name'] for coin in comparison_data]
        symbols = [coin['symbol'] for coin in comparison_data]
        prices = [coin['price'] for coin in comparison_data]
        market_caps = [coin['market_cap'] / 1e9 for coin in comparison_data]
        volumes = [coin['volume_24h'] / 1e9 for coin in comparison_data]
        changes_24h = [coin['percent_change_24h'] for coin in comparison_data]
        
        # Chart 1: Current Prices
        colors_price = ['#2ecc71' if p > 0 else '#e74c3c' for p in prices]
        bars1 = ax1.bar(symbols, prices, color=colors_price, alpha=0.7, edgecolor='black')
        ax1.set_title('Current Prices (USD)', fontsize=14, fontweight='bold')
        ax1.set_ylabel('Price (USD)', fontsize=12)
        ax1.set_xlabel('Cryptocurrency', fontsize=12)
        ax1.grid(axis='y', alpha=0.3)
        
        for bar, price in zip(bars1, prices):
            height = bar.get_height()
            ax1.text(bar.get_x() + bar.get_width()/2., height,
                    f'${price:,.2f}',
                    ha='center', va='bottom', fontsize=10, fontweight='bold')
        
        # Chart 2: Market Cap
        colors_cap = plt.cm.viridis([i/len(market_caps) for i in range(len(market_caps))])
        bars2 = ax2.bar(symbols, market_caps, color=colors_cap, alpha=0.7, edgecolor='black')
        ax2.set_title('Market Capitalization (Billions USD)', fontsize=14, fontweight='bold')
        ax2.set_ylabel('Market Cap (Billions)', fontsize=12)
        ax2.set_xlabel('Cryptocurrency', fontsize=12)
        ax2.grid(axis='y', alpha=0.3)
        
        for bar, cap in zip(bars2, market_caps):
            height = bar.get_height()
            ax2.text(bar.get_x() + bar.get_width()/2., height,
                    f'${cap:.2f}B',
                    ha='center', va='bottom', fontsize=10, fontweight='bold')
        
        # Chart 3: 24h Trading Volume
        colors_vol = plt.cm.plasma([i/len(volumes) for i in range(len(volumes))])
        bars3 = ax3.bar(symbols, volumes, color=colors_vol, alpha=0.7, edgecolor='black')
        ax3.set_title('24h Trading Volume (Billions USD)', fontsize=14, fontweight='bold')
        ax3.set_ylabel('Volume (Billions)', fontsize=12)
        ax3.set_xlabel('Cryptocurrency', fontsize=12)
        ax3.grid(axis='y', alpha=0.3)
        
        for bar, vol in zip(bars3, volumes):
            height = bar.get_height()
            ax3.text(bar.get_x() + bar.get_width()/2., height,
                    f'${vol:.2f}B',
                    ha='center', va='bottom', fontsize=10, fontweight='bold')
        
        # Chart 4: 24h Price Change Percentage
        colors_change = ['#27ae60' if c > 0 else '#c0392b' for c in changes_24h]
        bars4 = ax4.bar(symbols, changes_24h, color=colors_change, alpha=0.7, edgecolor='black')
        ax4.set_title('24h Price Change (%)', fontsize=14, fontweight='bold')
        ax4.set_ylabel('Change (%)', fontsize=12)
        ax4.set_xlabel('Cryptocurrency', fontsize=12)
        ax4.axhline(y=0, color='black', linestyle='-', linewidth=0.8)
        ax4.grid(axis='y', alpha=0.3)
        
        for bar, change in zip(bars4, changes_24h):
            height = bar.get_height()
            va = 'bottom' if change > 0 else 'top'
            ax4.text(bar.get_x() + bar.get_width()/2., height,
                    f'{change:+.2f}%',
                    ha='center', va=va, fontsize=10, fontweight='bold')
        
        plt.tight_layout()
        plt.savefig(output_path, dpi=300, bbox_inches='tight')
        plt.close()
        
        return os.path.abspath(output_path)


# Initialize the crypto data handler
crypto_handler = CryptoMarketData()


# MCP Tool Definitions

async def get_crypto_price(ticker: str) -> str:
    """
    Get detailed price information for a cryptocurrency.
    
    Args:
        ticker: Cryptocurrency ticker (e.g., 'btc-bitcoin', 'eth-ethereum')
    
    Returns:
        Formatted price information including market cap, volume, and price changes
    """
    data = crypto_handler.get_formatted_price(ticker)
    
    if "error" in data:
        return f"Error: {data['error']}"
    
    output = [
        f"\n{'='*60}",
        f"  {data['name']} ({data['symbol']}) - Rank #{data['rank']}",
        f"{'='*60}",
        f"  Current Price:        ${data['price']:,.2f}",
        f"  Market Cap:           ${data['market_cap']:,.0f}",
        f"  24h Volume:           ${data['volume_24h']:,.0f}",
        f"  All-Time High:        ${data['ath_price']:,.2f}",
        f"\n  Price Changes:",
        f"    24 Hours:           {data['percent_change_24h']:+.2f}%",
        f"    7 Days:             {data['percent_change_7d']:+.2f}%",
        f"\n  Last Updated:         {data['last_updated']}",
        f"{'='*60}\n"
    ]
    
    return "\n".join(output)


async def compare_cryptos(tickers: List[str]) -> str:
    """
    Compare multiple cryptocurrencies side by side.
    
    Args:
        tickers: List of cryptocurrency tickers (e.g., ['btc-bitcoin', 'eth-ethereum'])
    
    Returns:
        Comparison table of cryptocurrencies
    """
    if not tickers:
        return "Error: No tickers provided"
    
    output = [
        f"\n{'='*80}",
        f"  CRYPTOCURRENCY COMPARISON",
        f"{'='*80}\n"
    ]
    
    comparison_data = []
    
    for ticker in tickers:
        data = crypto_handler.get_formatted_price(ticker)
        if data and "error" not in data:
            comparison_data.append(data)
    
    if not comparison_data:
        return "Error: No valid data retrieved for any ticker"
    
    # Header
    output.append(f"{'Name':<15} | {'Price':>15} | {'24h Change':>12} | {'Market Cap':>18}")
    output.append("-" * 80)
    
    # Data rows
    for coin in comparison_data:
        name = coin['name'][:14]
        price = f"${coin['price']:,.2f}"
        change_24h = f"{coin['percent_change_24h']:+.2f}%"
        market_cap = f"${coin['market_cap']:,.0f}"
        
        output.append(f"{name:<15} | {price:>15} | {change_24h:>12} | {market_cap:>18}")
    
    output.append("=" * 80 + "\n")
    
    return "\n".join(output)

async def search_cryptocurrency(search_term: str) -> str:
    """
    Search for cryptocurrencies by name or symbol.
    
    Args:
        search_term: Name or symbol to search for (e.g., 'bitcoin', 'BTC')
    
    Returns:
        List of matching cryptocurrencies with their tickers
    """
    results = crypto_handler.search_crypto(search_term)
    
    # Handle API errors
    if isinstance(results, list) and len(results) > 0 and isinstance(results[0], dict) and "error" in results[0]:
        return f"Error: {results[0]['error']}"
    
    if not results:
        return f"No cryptocurrencies found matching '{search_term}'"
    
    output = [
        f"\n{'='*70}",
        f"  SEARCH RESULTS FOR: '{search_term}'",
        f"{'='*70}\n"
    ]
    
    for i, crypto in enumerate(results, 1):
        name = crypto.get('name', 'N/A')
        symbol = crypto.get('symbol', 'N/A')
        ticker = crypto.get('id', 'N/A')
        is_active = "Active" if crypto.get('is_active', False) else "Inactive"
        
        output.append(f"  {i}. {name} ({symbol}) - {is_active}")
        output.append(f"     Ticker: {ticker}\n")
    
    output.append("=" * 70 + "\n")
    
    return "\n".join(output)

async def list_common_tickers() -> str:
    """
    Get a list of commonly tracked cryptocurrency tickers.
    
    Returns:
        List of popular cryptocurrency tickers
    """
    common = [
        ("Bitcoin", "btc-bitcoin"),
        ("Ethereum", "eth-ethereum"),
        ("Cardano", "ada-cardano"),
        ("XRP", "xrp-xrp"),
        ("Solana", "sol-solana"),
        ("Polkadot", "dot-polkadot"),
        ("Dogecoin", "doge-dogecoin"),
        ("Polygon", "matic-polygon")
    ]
    
    output = [
        f"\n{'='*60}",
        f"  COMMON CRYPTOCURRENCY TICKERS",
        f"{'='*60}\n"
    ]
    
    for name, ticker in common:
        output.append(f"  {name:<15} -> {ticker}")
    
    output.append("\n" + "=" * 60 + "\n")
    
    return "\n".join(output)


async def get_market_overview(tickers: List[str] = None) -> str:
    """
    Get a comprehensive market overview for top cryptocurrencies.
    
    Args:
        tickers: Optional list of tickers. If not provided, uses common tickers.
    
    Returns:
        Complete market overview with prices and trends
    """
    if not tickers:
        tickers = ["btc-bitcoin", "eth-ethereum", "ada-cardano", "xrp-xrp"]
    
    output = [
        f"\n{'='*90}",
        f"  CRYPTOCURRENCY MARKET OVERVIEW",
        f"{'='*90}\n"
    ]
    
    total_market_cap = 0
    
    for ticker in tickers:
        data = crypto_handler.get_formatted_price(ticker)
        
        if data and "error" not in data:
            total_market_cap += data['market_cap']
            
            trend = "UP" if data['percent_change_24h'] > 0 else "DOWN"
            
            output.append(f"{trend} {data['name']} ({data['symbol']})")
            output.append(f"   Price: ${data['price']:,.2f} | 24h: {data['percent_change_24h']:+.2f}% | Cap: ${data['market_cap']:,.0f}")
            output.append("")
    
    output.append("-" * 90)
    output.append(f"Total Market Cap (selected): ${total_market_cap:,.0f}")
    output.append("=" * 90 + "\n")
    
    return "\n".join(output)

async def visualize_crypto_comparison(tickers: List[str], output_filename: str = "crypto_comparison.png") -> str:
    """
    Create a visual comparison chart for multiple cryptocurrencies.
    
    Args:
        tickers: List of cryptocurrency tickers to compare (e.g., ['btc-bitcoin', 'eth-ethereum'])
        output_filename: Name of the output image file (default: 'crypto_comparison.png')
    
    Returns:
        Path to the generated chart image or error message
    """
    if not tickers:
        return "Error: No tickers provided for visualization"
    
    if len(tickers) < 2:
        return "Error: At least 2 tickers required for comparison"
    
    result = crypto_handler.create_comparison_chart(tickers, output_filename)
    
    if "Error" in result:
        return result
    
    output = [
        f"\n{'='*70}",
        f"  VISUALIZATION GENERATED SUCCESSFULLY",
        f"{'='*70}\n",
        f"  Chart saved to: {result}",
        f"  Cryptocurrencies compared: {len(tickers)}",
        f"  Tickers: {', '.join(tickers)}",
        f"\n  Charts included:",
        f"    1. Current Prices (USD)",
        f"    2. Market Capitalization",
        f"    3. 24h Trading Volume",
        f"    4. 24h Price Change Percentage",
        f"\n{'='*70}\n"
    ]
    
    return "\n".join(output)

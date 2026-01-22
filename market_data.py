import yfinance as yf
import requests
from datetime import datetime

def get_stock_prices(tickers):
    """
    Fetch real-time stock/ETF prices
    Returns: dict with ticker: {price, change_pct, name}
    """
    prices = {}
    
    for ticker in tickers:
        try:
            stock = yf.Ticker(ticker)
            info = stock.info
            
            current_price = info.get('regularMarketPrice', 0)
            prev_close = info.get('previousClose', current_price)
            change_pct = ((current_price - prev_close) / prev_close * 100) if prev_close else 0
            
            prices[ticker] = {
                'price': current_price,
                'change_pct': change_pct,
                'name': info.get('shortName', ticker),
                'currency': info.get('currency', 'USD')
            }
        except Exception as e:
            print(f"Error fetching {ticker}: {e}")
            prices[ticker] = {
                'price': 0,
                'change_pct': 0,
                'name': ticker,
                'currency': 'USD'
            }
    
    return prices


def get_crypto_prices(symbols):
    """
    Fetch real-time crypto prices from CoinGecko (FREE API)
    symbols: list like ['bitcoin', 'ethereum', 'solana']
    Returns: dict with symbol: {price, change_24h, name}
    """
    prices = {}
    
    try:
        # CoinGecko free API
        ids = ','.join(symbols)
        url = f"https://api.coingecko.com/api/v3/simple/price?ids={ids}&vs_currencies=usd&include_24hr_change=true"
        
        response = requests.get(url)
        data = response.json()
        
        name_map = {
            'bitcoin': 'Bitcoin',
            'ethereum': 'Ethereum',
            'solana': 'Solana',
            'raydium': 'Raydium',
            'jupiter-exchange-solana': 'Jupiter'
        }
        
        for symbol in symbols:
            if symbol in data:
                prices[symbol] = {
                    'price': data[symbol]['usd'],
                    'change_24h': data[symbol].get('usd_24h_change', 0),
                    'name': name_map.get(symbol, symbol.title())
                }
            else:
                prices[symbol] = {
                    'price': 0,
                    'change_24h': 0,
                    'name': name_map.get(symbol, symbol.title())
                }
    
    except Exception as e:
        print(f"Error fetching crypto prices: {e}")
        for symbol in symbols:
            prices[symbol] = {'price': 0, 'change_24h': 0, 'name': symbol}
    
    return prices


def calculate_portfolio_value(holdings, stock_prices, crypto_prices):
    """
    Calculate total portfolio value and breakdown
    
    holdings = {
        'stocks': {'VTI': 10, 'BND': 5},
        'crypto': {'bitcoin': 0.1, 'solana': 50}
    }
    """
    
    total_value = 0
    breakdown = {
        'traditional': 0,
        'crypto': 0,
        'details': []
    }
    
    # Calculate stocks
    if 'stocks' in holdings:
        for ticker, shares in holdings['stocks'].items():
            if ticker in stock_prices:
                value = shares * stock_prices[ticker]['price']
                total_value += value
                breakdown['traditional'] += value
                
                breakdown['details'].append({
                    'asset': stock_prices[ticker]['name'],
                    'ticker': ticker,
                    'amount': shares,
                    'price': stock_prices[ticker]['price'],
                    'value': value,
                    'change': stock_prices[ticker]['change_pct'],
                    'type': 'stock'
                })
    
    # Calculate crypto
    if 'crypto' in holdings:
        for symbol, amount in holdings['crypto'].items():
            if symbol in crypto_prices:
                value = amount * crypto_prices[symbol]['price']
                total_value += value
                breakdown['crypto'] += value
                
                breakdown['details'].append({
                    'asset': crypto_prices[symbol]['name'],
                    'ticker': symbol.upper(),
                    'amount': amount,
                    'price': crypto_prices[symbol]['price'],
                    'value': value,
                    'change': crypto_prices[symbol]['change_24h'],
                    'type': 'crypto'
                })
    
    breakdown['total'] = total_value
    
    return breakdown


# Test the functions
if __name__ == "__main__":
    print("Testing Market Data Fetcher...\n")
    
    # Test stocks
    print("Fetching stock prices...")
    stock_tickers = ['VTI', 'BND', 'VXUS', 'VNQ', 'GLD']
    stocks = get_stock_prices(stock_tickers)
    
    for ticker, data in stocks.items():
        print(f"{ticker}: ${data['price']:.2f} ({data['change_pct']:+.2f}%)")
    
    print("\nFetching crypto prices...")
    crypto_symbols = ['bitcoin', 'ethereum', 'solana', 'raydium', 'jupiter-exchange-solana']
    crypto = get_crypto_prices(crypto_symbols)
    
    for symbol, data in crypto.items():
        print(f"{data['name']}: ${data['price']:.2f} ({data['change_24h']:+.2f}%)")
    
    print("\nTesting portfolio calculation...")
    test_holdings = {
        'stocks': {
            'VTI': 10,
            'BND': 5
        },
        'crypto': {
            'bitcoin': 0.1,
            'solana': 50
        }
    }
    
    portfolio = calculate_portfolio_value(test_holdings, stocks, crypto)
    print(f"\nTotal Portfolio Value: ${portfolio['total']:,.2f}")
    print(f"Traditional: ${portfolio['traditional']:,.2f}")
    print(f"Crypto: ${portfolio['crypto']:,.2f}")
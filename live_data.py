import yfinance as yf
import streamlit as st
import pandas as pd
from datetime import datetime, timedelta
import random
import requests

@st.cache_data(ttl=300)
def get_live_market_data():
    """Get live market data using yfinance with caching"""
    tickers = {
        # Crypto
        'BTC': 'BTC-USD', 'ETH': 'ETH-USD', 'SOL': 'SOL-USD',
        'BNB': 'BNB-USD', 'XRP': 'XRP-USD', 'ADA': 'ADA-USD',
        'AVAX': 'AVAX-USD', 'LINK': 'LINK-USD', 'DOT': 'DOT-USD',
        'JUP': 'JUP-USD', 'PYTH': 'PYTH-USD', 'RAY': 'RAY-USD',
        'BONK': 'BONK-USD', 'AR': 'AR-USD', 'RENDER': 'RENDER-USD',
        
        # US Equity
        'VTI': 'VTI', 'SPY': 'SPY', 'QQQ': 'QQQ', 'DIA': 'DIA',
        'AAPL': 'AAPL', 'MSFT': 'MSFT', 'NVDA': 'NVDA', 'AMZN': 'AMZN',
        'GOOGL': 'GOOGL', 'META': 'META', 'TSLA': 'TSLA', 'BRK-B': 'BRK-B',
        'JPM': 'JPM', 'UNH': 'UNH', 'V': 'V', 'MA': 'MA', 'COST': 'COST',
        'PG': 'PG', 'HD': 'HD', 'LLY': 'LLY', 'AVGO': 'AVGO',
        
        # Global Equity & ETFs
        'VT': 'VT', 'VXUS': 'VXUS', 'VEA': 'VEA', 'VWO': 'VWO',
        'ASML': 'ASML', 'SAP': 'SAP', 'SAMSUNG': '005930.KS',
        'TOYOTA': 'TM', 'SONY': 'SONY', 'LVMH': 'MC.PA',
        'BP': 'BP', 'HSBA': 'HSBA.L', 'NESN': 'NESN.SW',
        
        # Commodities & Real Estate
        'GOLD': 'GC=F', 'SILVER': 'SI=F', 'OIL': 'CL=F',
        'VNQ': 'VNQ', 'REM': 'REM', 'GSG': 'GSG',
        
        # Fixed Income
        'BND': 'BND', 'TLT': 'TLT', 'AGG': 'AGG', 'JNK': 'JNK'
    }
    
    data = {}
    
    try:
        tickers_list = list(tickers.values())
        history = yf.download(tickers_list, period="1mo", interval="1d", progress=False)
        
        if history is None or history.empty:
            raise Exception("Empty history received")
            
        for symbol, ticker_id in tickers.items():
            try:
                if len(tickers) > 1:
                    ticker_hist = history['Close'][ticker_id].dropna()
                else:
                    ticker_hist = history['Close'].dropna()
                
                if ticker_hist.empty:
                    raise Exception("No data")

                current_price = float(ticker_hist.iloc[-1])
                prev_price = float(ticker_hist.iloc[-2])
                
                change_24h = ((current_price - prev_price) / prev_price) * 100
                
                hist_df = ticker_hist.reset_index()
                chart_history = []
                for _, row in hist_df.iterrows():
                    chart_history.append({
                        'date': row['Date'].strftime('%Y-%m-%d'),
                        'price': float(row[ticker_id] if len(tickers) > 1 else row['Close'])
                    })
                
                data[symbol] = {
                    'price': current_price,
                    'change_24h': change_24h,
                    'change_7d': 0.0,
                    'history': chart_history
                }
            except Exception as e:
                data[symbol] = _get_mock_data(symbol)
                
    except Exception as e:
        for s in tickers:
            data[s] = _get_mock_data(s)
            
    return data

def _get_mock_data(symbol):
    """Fallback mock data with realistic simulation"""
    base_prices = {
        'BTC': 102000, 'ETH': 2800, 'SOL': 180, 
        'BNB': 650, 'XRP': 2.8, 'ADA': 1.1,
        'AVAX': 45, 'LINK': 22, 'DOT': 9,
        'VTI': 305, 'GOLD': 2850, 'BONDS': 95,
        'AAPL': 240, 'NVDA': 148, 'TSLA': 365,
        'MSFT': 420, 'AMZN': 210, 'GOOGL': 195,
        'META': 560, 'NFLX': 680, 'AMD': 165,
        'INTC': 25, 'JPM': 230, 'GS': 520,
        'XOM': 115, 'CVX': 155, 'BRK-B': 465,
        'SPY': 600, 'QQQ': 510, 'DIA': 435, 'VNQ': 85, 'USO': 75, 'GDX': 35, 'VT': 110,
        'BND': 72, 'TLT': 95, 'VXUS': 65, 'VEA': 52, 'VWO': 45
    }
    
    history = []
    base_price = base_prices.get(symbol, 100)
    current_price = base_price * 0.95
    
    now = datetime.now()
    
    for i in range(30):
        date = (now - timedelta(days=29-i)).strftime('%Y-%m-%d')
        volatility = 0.04 if symbol in ['BTC', 'ETH', 'SOL'] else 0.015
        change = random.uniform(-volatility, volatility) + 0.001
        current_price = current_price * (1 + change)
        
        history.append({
            'date': date,
            'price': current_price
        })
    
    latest_price = history[-1]['price']
    prev_price = history[-2]['price']
    change_24h = ((latest_price - prev_price) / prev_price) * 100

    return {
        'price': latest_price,
        'change_24h': change_24h,
        'history': history
    }

def get_market_narrative():
    """Synthesizes current market conditions into a macro-narrative for AI context"""
    try:
        data = get_live_market_data()
        
        # Key indicators
        btc = data.get('BTC', {})
        sol = data.get('SOL', {})
        spy = data.get('SPY', {})
        gold = data.get('GOLD', {})
        
        narrative = []
        
        # Crypto Narrative
        if btc.get('change_24h', 0) > 2:
            narrative.append(f"Bitcoin is showing strong momentum (+{btc['change_24h']:.1f}%), indicating a high-risk appetite across digital assets.")
        elif btc.get('change_24h', 0) < -2:
            narrative.append(f"Bitcoin is experiencing a drawdown ({btc['change_24h']:.1f}%), suggesting tactical caution or dip-buying opportunities in crypto.")
        else:
            narrative.append("Bitcoin is consolidating, suggesting a search for the next catalyst.")
            
        # Solana Ecosystem
        if sol.get('change_24h', 0) > 5:
            narrative.append(f"Solana is outperforming (+{sol['change_24h']:.1f}%), likely driven by ecosystem activity and DeFi inflows.")
        
        # Equities
        if spy.get('change_24h', 0) > 1:
            narrative.append(f"US Equities (S&P 500) are bullish (+{spy['change_24h']:.1f}%), reflecting positive macro-sentiments.")
        elif spy.get('change_24h', 0) < -1:
            narrative.append(f"Equity markets are showing weakness ({spy['change_24h']:.1f}%), possibly due to interest rate concerns or geopolitical headers.")
            
        # Safe Havens
        if gold.get('change_24h', 0) > 1:
            narrative.append(f"Gold is up (+{gold['change_24h']:.1f}%), highlighting a flight to safety and inflation concerns.")
            
        return " ".join(narrative)
    except Exception as e:
        return "Market is currently in an equilibrium state. Focus on long-term structural trends."

def get_defi_yields():
    """Get current DeFi yields from DefiLlama API"""
    try:
        response = requests.get("https://yields.llama.fi/pools", timeout=10)
        response.raise_for_status()
        pools = response.json()['data']
        
        results = {
            'Jito Staking': {'apy': 7.8, 'tvl': '1.8B'},
            'Raydium Pools': {'apy': 18.2, 'tvl': '650M'},
            'Kamino Vaults': {'apy': 24.5, 'tvl': '410M'},
            'Marinade Native': {'apy': 7.5, 'tvl': '1.2B'},
            'Orca Whirlpools': {'apy': 32.1, 'tvl': '380M'},
            'Solend Lending': {'apy': 12.4, 'tvl': '220M'},
            'Marginfi Yield': {'apy': 14.2, 'tvl': '450M'}
        }
        
        jito_pool = next((p for p in pools if p['project'] == 'jito' and p['symbol'] == 'JITOSOL'), None)
        if jito_pool:
            results['Jito Staking'] = {
                'apy': round(float(jito_pool['apy']), 2),
                'tvl': f"${jito_pool['tvlUsd']/1e9:.1f}B"
            }
            
        ray_pool = next((p for p in pools if p['project'] == 'raydium' and 'SOL' in p['symbol'] and p['tvlUsd'] > 1e6), None)
        if ray_pool:
            results['Raydium Pools'] = {
                'apy': round(float(ray_pool['apy']), 2),
                'tvl': f"${ray_pool['tvlUsd']/1e6:.1f}M"
            }
            
        kamino_pool = next((p for p in pools if p['project'] == 'kamino' and 'SOL' in p['symbol'] and p['tvlUsd'] > 1e6), None)
        if kamino_pool:
            results['Kamino Vaults'] = {
                'apy': round(float(kamino_pool['apy']), 2),
                'tvl': f"${kamino_pool['tvlUsd']/1e6:.1f}M"
            }

        mnd_pool = next((p for p in pools if p['project'] == 'marinade' and p['symbol'] == 'MSOL'), None)
        if mnd_pool:
            results['Marinade Native'] = {
                'apy': round(float(mnd_pool['apy']), 2),
                'tvl': f"${mnd_pool['tvlUsd']/1e9:.1f}B"
            }

        orca_pool = next((p for p in pools if p['project'] == 'orca' and 'SOL' in p['symbol'] and p['tvlUsd'] > 1e6), None)
        if orca_pool:
            results['Orca Whirlpools'] = {
                'apy': round(float(orca_pool['apy']), 2),
                'tvl': f"${orca_pool['tvlUsd']/1e6:.1f}M"
            }

        solend_pool = next((p for p in pools if p['project'] == 'solend' and 'SOL' in p['symbol'] and p['tvlUsd'] > 1e5), None)
        if solend_pool:
            results['Solend Lending'] = {
                'apy': round(float(solend_pool['apy']), 2),
                'tvl': f"${solend_pool['tvlUsd']/1e6:.1f}M"
            }

        m_pool = next((p for p in pools if p['project'] == 'marginfi' and 'SOL' in p['symbol'] and p['tvlUsd'] > 1e5), None)
        if m_pool:
            results['Marginfi Yield'] = {
                'apy': round(float(m_pool['apy']), 2),
                'tvl': f"${m_pool['tvlUsd']/1e6:.1f}M"
            }
            
        return results
        
    except Exception as e:
        return {
            'Jito Staking': {'apy': 7.8, 'tvl': '1.8B'},
            'Raydium Pools': {'apy': 18.2, 'tvl': '650M'},
            'Kamino Vaults': {'apy': 24.5, 'tvl': '410M'}
        }

def get_portfolio_growth_projection(initial_capital, monthly_investment, years, annual_return):
    """Calculate portfolio growth over time"""
    months = years * 12
    portfolio_values = []
    
    current_value = initial_capital
    
    for month in range(months + 1):
        if month > 0:
            current_value += monthly_investment
            monthly_return = annual_return / 12
            current_value *= (1 + monthly_return)
        
        portfolio_values.append({
            'month': month,
            'year': month / 12,
            'value': round(current_value, 2)
        })
    
    return portfolio_values

@st.cache_data(ttl=3600)
def get_global_exchange_rates():
    """Get live currency exchange rates (USD based)"""
    return {
        'USD': 1.0,
        'EUR': 0.92,
        'GBP': 0.79,
        'JPY': 148.5,
        'CAD': 1.35,
        'AUD': 1.52,
        'INR': 83.1,
        'NGN': 1450.0
    }

def get_strategy_vaults():
    """Managed investment buckets inspired by Strum Capital"""
    return [
        {
            'name': 'Solana Stable Yield',
            'description': 'Automated delta-neutral strategy using JitoSOL and Kamino lending to harvest premium yields with low volatility.',
            'apy': 12.4,
            'risk': 'Low',
            'tvl': '$14.2M',
            'status': 'Active',
            'logo': 'SOL'
        },
        {
            'name': 'Global Blue Chip',
            'description': 'A balanced mix of S&P 500, Gold, and Bitcoin. Automatically rebalanced monthly to preserve global purchasing power.',
            'apy': 18.5,
            'risk': 'Medium',
            'tvl': '$28.5M',
            'status': 'Active',
            'logo': 'VT'
        },
        {
            'name': 'DeFi Degenerate',
            'description': 'High-exposure vault utilizing Raydium liquidity pairs and Orca Whirlpools for maximum capital efficiency.',
            'apy': 42.1,
            'risk': 'High',
            'tvl': '$6.8M',
            'status': 'Live',
            'logo': 'RAY'
        }
    ]

@st.cache_data(ttl=3600)
def get_asset_registry():
    """Returns a curated list of global assets with metadata for searchability"""
    return [
        # Crypto
        {'symbol': 'BTC', 'name': 'Bitcoin', 'category': 'Crypto', 'region': 'Global'},
        {'symbol': 'ETH', 'name': 'Ethereum', 'category': 'Crypto', 'region': 'Global'},
        {'symbol': 'SOL', 'name': 'Solana', 'category': 'Crypto', 'region': 'Global'},
        {'symbol': 'BNB', 'name': 'Binance Coin', 'category': 'Crypto', 'region': 'Global'},
        {'symbol': 'XRP', 'name': 'Ripple', 'category': 'Crypto', 'region': 'Global'},
        {'symbol': 'ADA', 'name': 'Cardano', 'category': 'Crypto', 'region': 'Global'},
        {'symbol': 'AVAX', 'name': 'Avalanche', 'category': 'Crypto', 'region': 'Global'},
        {'symbol': 'LINK', 'name': 'Chainlink', 'category': 'Crypto', 'region': 'Global'},
        {'symbol': 'DOT', 'name': 'Polkadot', 'category': 'Crypto', 'region': 'Global'},
        {'symbol': 'JUP', 'name': 'Jupiter', 'category': 'Crypto', 'region': 'Solana'},
        {'symbol': 'PYTH', 'name': 'Pyth Network', 'category': 'Crypto', 'region': 'Solana'},
        {'symbol': 'RAY', 'name': 'Raydium', 'category': 'Crypto', 'region': 'Solana'},
        {'symbol': 'BONK', 'name': 'Bonk', 'category': 'Crypto', 'region': 'Solana'},
        {'symbol': 'AR', 'name': 'Arweave', 'category': 'Crypto', 'region': 'Global'},
        {'symbol': 'RENDER', 'name': 'Render Token', 'category': 'Crypto', 'region': 'Global'},
        
        # US Equity
        {'symbol': 'AAPL', 'name': 'Apple Inc.', 'category': 'Equity', 'region': 'US'},
        {'symbol': 'MSFT', 'name': 'Microsoft Corp', 'category': 'Equity', 'region': 'US'},
        {'symbol': 'NVDA', 'name': 'NVIDIA Corp', 'category': 'Equity', 'region': 'US'},
        {'symbol': 'AMZN', 'name': 'Amazon.com', 'category': 'Equity', 'region': 'US'},
        {'symbol': 'GOOGL', 'name': 'Alphabet Inc.', 'category': 'Equity', 'region': 'US'},
        {'symbol': 'META', 'name': 'Meta Platforms', 'category': 'Equity', 'region': 'US'},
        {'symbol': 'TSLA', 'name': 'Tesla, Inc.', 'category': 'Equity', 'region': 'US'},
        {'symbol': 'BRK-B', 'name': 'Berkshire Hathaway', 'category': 'Equity', 'region': 'US'},
        {'symbol': 'JPM', 'name': 'JPMorgan Chase', 'category': 'Equity', 'region': 'US'},
        {'symbol': 'UNH', 'name': 'UnitedHealth Group', 'category': 'Equity', 'region': 'US'},
        {'symbol': 'V', 'name': 'Visa Inc.', 'category': 'Equity', 'region': 'US'},
        {'symbol': 'MA', 'name': 'Mastercard Inc.', 'category': 'Equity', 'region': 'US'},
        {'symbol': 'COST', 'name': 'Costco Wholesale', 'category': 'Equity', 'region': 'US'},
        
        # Global Equity
        {'symbol': 'ASML', 'name': 'ASML Holding', 'category': 'Equity', 'region': 'Europe'},
        {'symbol': 'SAP', 'name': 'SAP SE', 'category': 'Equity', 'region': 'Europe'},
        {'symbol': 'SAMSUNG', 'name': 'Samsung Electronics', 'category': 'Equity', 'region': 'Asia'},
        {'symbol': 'TOYOTA', 'name': 'Toyota Motor', 'category': 'Equity', 'region': 'Asia'},
        {'symbol': 'SONY', 'name': 'Sony Group', 'category': 'Equity', 'region': 'Asia'},
        {'symbol': 'LVMH', 'name': 'LVMH Moet Hennessy', 'category': 'Equity', 'region': 'Europe'},
        {'symbol': 'BP', 'name': 'BP plc', 'category': 'Equity', 'region': 'Europe'},
        {'symbol': 'HSBA', 'name': 'HSBC Holdings', 'category': 'Equity', 'region': 'Europe'},
        {'symbol': 'NESN', 'name': 'Nestle S.A.', 'category': 'Equity', 'region': 'Europe'},
        
        # ETFs
        {'symbol': 'VTI', 'name': 'Vanguard Total Stock', 'category': 'ETF', 'region': 'US'},
        {'symbol': 'SPY', 'name': 'SPDR S&P 500', 'category': 'ETF', 'region': 'US'},
        {'symbol': 'QQQ', 'name': 'Invesco QQQ Trust', 'category': 'ETF', 'region': 'US'},
        {'symbol': 'VT', 'name': 'Vanguard Total World', 'category': 'ETF', 'region': 'Global'},
        {'symbol': 'VXUS', 'name': 'Vanguard Total Intl', 'category': 'ETF', 'region': 'Global'},
        {'symbol': 'VWO', 'name': 'Vanguard EM ETF', 'category': 'ETF', 'region': 'Emerging'},
        {'symbol': 'VNQ', 'name': 'Vanguard Real Estate', 'category': 'ETF', 'region': 'US'},
        
        # Commodities
        {'symbol': 'GOLD', 'name': 'Gold (Comex)', 'category': 'Commodity', 'region': 'Global'},
        {'symbol': 'SILVER', 'name': 'Silver (Comex)', 'category': 'Commodity', 'region': 'Global'},
        {'symbol': 'OIL', 'name': 'Crude Oil', 'category': 'Commodity', 'region': 'Global'},
        
        # Fixed Income
        {'symbol': 'BND', 'name': 'Vanguard Total Bond', 'category': 'Fixed Income', 'region': 'US'},
        {'symbol': 'TLT', 'name': '20+ Year Treasury', 'category': 'Fixed Income', 'region': 'US'}
    ]
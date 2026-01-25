import yfinance as yf
import streamlit as st
import pandas as pd
from datetime import datetime, timedelta

@st.cache_data(ttl=300)
def get_live_market_data():
    """Get live market data using yfinance with caching"""
    tickers = {
        'BTC': 'BTC-USD', 'ETH': 'ETH-USD', 'SOL': 'SOL-USD',
        'BNB': 'BNB-USD', 'XRP': 'XRP-USD', 'ADA': 'ADA-USD',
        'AVAX': 'AVAX-USD', 'LINK': 'LINK-USD', 'DOT': 'DOT-USD',
        'VTI': 'VTI', 'GOLD': 'GC=F', 'BONDS': 'TLT',
        'AAPL': 'AAPL', 'NVDA': 'NVDA', 'TSLA': 'TSLA', 'MSFT': 'MSFT',
        'AMZN': 'AMZN', 'GOOGL': 'GOOGL', 'META': 'META', 'NFLX': 'NFLX',
        'AMD': 'AMD', 'INTC': 'INTC', 'JPM': 'JPM', 'GS': 'GS',
        'XOM': 'XOM', 'CVX': 'CVX', 'BRK-B': 'BRK-B', 'SPY': 'SPY',
        'QQQ': 'QQQ', 'DIA': 'DIA', 'VNQ': 'VNQ', 'USO': 'USO', 'GDX': 'GDX', 'VT': 'VT'
    }
    
    data = {}
    
    try:
        # Batch fetch for efficiency
        tickers_list = list(tickers.values())
        history = yf.download(tickers_list, period="1mo", interval="1d", progress=False)
        
        if history is None or history.empty:
            raise Exception("Empty history received")
            
        # Current info fetch (threading issues sometimes with yf, doing sequential if batch fails or mainly for metadata)
        # Using the history DataFrame is faster and reliable for "latest price" vs "yesterday close"
        
        for symbol, ticker_id in tickers.items():
            try:
                # Extract history for specific ticker
                # yf.download with multiple tickers returns MultiIndex columns
                if len(tickers) > 1:
                    ticker_hist = history['Close'][ticker_id].dropna()
                else:
                    ticker_hist = history['Close'].dropna()
                
                if ticker_hist.empty:
                    raise Exception("No data")

                current_price = float(ticker_hist.iloc[-1])
                prev_price = float(ticker_hist.iloc[-2])
                
                change_24h = ((current_price - prev_price) / prev_price) * 100
                
                # Format history for charts
                # Reset index to get Date column
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
                    'change_7d': 0.0, # Placeholder or calc from history
                    'history': chart_history
                }
            except Exception as e:
                # Fallback to mock if individual ticker fails
                print(f"Error fetching {symbol}: {e}")
                data[symbol] = _get_mock_data(symbol)
                
    except Exception as e:
        print(f"Global fetch error: {e}")
        # Complete fallback
        for s in tickers:
            data[s] = _get_mock_data(s)
            
    return data

import random

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
        'SPY': 600, 'QQQ': 510, 'DIA': 435, 'VNQ': 85, 'USO': 75, 'GDX': 35, 'VT': 110
    }
    
    # Generate realistic 30-day history
    history = []
    base_price = base_prices.get(symbol, 100)
    current_price = base_price * 0.95 # Start slightly lower
    
    now = datetime.now()
    
    for i in range(30):
        date = (now - timedelta(days=29-i)).strftime('%Y-%m-%d')
        # Random walk volatility
        volatility = 0.04 if symbol in ['BTC', 'ETH', 'SOL'] else 0.015
        change = random.uniform(-volatility, volatility) + 0.001 # Slight upward drift
        current_price = current_price * (1 + change)
        
        history.append({
            'date': date,
            'price': current_price
        })
    
    # Calculate 24h change
    latest_price = history[-1]['price']
    prev_price = history[-2]['price']
    change_24h = ((latest_price - prev_price) / prev_price) * 100

    return {
        'price': latest_price,
        'change_24h': change_24h,
        'history': history
    }

import requests

def get_defi_yields():
    """Get current DeFi yields from DefiLlama API"""
    try:
        # Fetch all yields from DefiLlama
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
        
        # Jito (JitoSOL)
        jito_pool = next((p for p in pools if p['project'] == 'jito' and p['symbol'] == 'JITOSOL'), None)
        if jito_pool:
            results['Jito Staking'] = {
                'apy': round(float(jito_pool['apy']), 2),
                'tvl': f"${jito_pool['tvlUsd']/1e9:.1f}B"
            }
            
        # Raydium (Highest SOL pool)
        ray_pool = next((p for p in pools if p['project'] == 'raydium' and 'SOL' in p['symbol'] and p['tvlUsd'] > 1e6), None)
        if ray_pool:
            results['Raydium Pools'] = {
                'apy': round(float(ray_pool['apy']), 2),
                'tvl': f"${ray_pool['tvlUsd']/1e6:.1f}M"
            }
            
        # Kamino (Highest SOL pool)
        kamino_pool = next((p for p in pools if p['project'] == 'kamino' and 'SOL' in p['symbol'] and p['tvlUsd'] > 1e6), None)
        if kamino_pool:
            results['Kamino Vaults'] = {
                'apy': round(float(kamino_pool['apy']), 2),
                'tvl': f"${kamino_pool['tvlUsd']/1e6:.1f}M"
            }

        # Marinade (mSOL)
        mnd_pool = next((p for p in pools if p['project'] == 'marinade' and p['symbol'] == 'MSOL'), None)
        if mnd_pool:
            results['Marinade Native'] = {
                'apy': round(float(mnd_pool['apy']), 2),
                'tvl': f"${mnd_pool['tvlUsd']/1e9:.1f}B"
            }

        # Orca
        orca_pool = next((p for p in pools if p['project'] == 'orca' and 'SOL' in p['symbol'] and p['tvlUsd'] > 1e6), None)
        if orca_pool:
            results['Orca Whirlpools'] = {
                'apy': round(float(orca_pool['apy']), 2),
                'tvl': f"${orca_pool['tvlUsd']/1e6:.1f}M"
            }

        # Solend
        solend_pool = next((p for p in pools if p['project'] == 'solend' and 'SOL' in p['symbol'] and p['tvlUsd'] > 1e5), None)
        if solend_pool:
            results['Solend Lending'] = {
                'apy': round(float(solend_pool['apy']), 2),
                'tvl': f"${solend_pool['tvlUsd']/1e6:.1f}M"
            }

        # Marginfi
        m_pool = next((p for p in pools if p['project'] == 'marginfi' and 'SOL' in p['symbol'] and p['tvlUsd'] > 1e5), None)
        if m_pool:
            results['Marginfi Yield'] = {
                'apy': round(float(m_pool['apy']), 2),
                'tvl': f"${m_pool['tvlUsd']/1e6:.1f}M"
            }
            
        return results
        
    except Exception as e:
        print(f"DeFi Fetch Error: {e}")
        # Fallback to mock if API fails
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
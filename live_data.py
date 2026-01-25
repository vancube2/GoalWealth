import yfinance as yf
import streamlit as st
import pandas as pd
from datetime import datetime, timedelta

@st.cache_data(ttl=300)
def get_live_market_data():
    """Get live market data using yfinance with caching"""
    tickers = {
        'BTC': 'BTC-USD',
        'ETH': 'ETH-USD',
        'SOL': 'SOL-USD',
        'VTI': 'VTI'  # Vanguard Total Stock Market ETF for S&P representation
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
    base_prices = {'BTC': 65000, 'ETH': 3500, 'SOL': 140, 'VTI': 260}
    
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

def get_defi_yields():
    """Get current DeFi yields (Mock for now as authentic source requires specialized API)"""
    return {
        'Jito Staking': {
            'apy': 7.8,
            'tvl': '1.8B',
            'history': [7.5, 7.6, 7.7, 7.8, 7.8, 7.9, 7.8]
        },
        'Raydium Pools': {
            'apy': 18.2,
            'tvl': '650M',
            'history': [16.2, 17.1, 18.0, 18.2, 18.4, 18.1, 18.2]
        },
        'Kamino Vaults': {
            'apy': 24.5,
            'tvl': '410M',
            'history': [22.5, 23.2, 24.0, 24.5, 25.1, 24.8, 24.5]
        }
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
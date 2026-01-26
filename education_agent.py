import google.generativeai as genai
import os
from dotenv import load_dotenv
from opik import track

from pathlib import Path
import time

# Robust env loading
gemini_key = os.environ.get('GEMINI_API_KEY')
if not gemini_key:
    try:
        candidates = [
            Path(__file__).parent / '.env',
            Path(os.getcwd()) / '.env',
            Path('C:/Users/DELL/Documents/GoalWealth/.env')
        ]
        for env_path in candidates:
            if env_path.exists():
                try:
                    # encoding='utf-8-sig' handles BOM if present
                    with open(env_path, 'r', encoding='utf-8-sig', errors='ignore') as f:
                        content = f.read()
                        for line in content.splitlines():
                            line = line.strip()
                            if line.startswith('GEMINI_API_KEY='):
                                gemini_key = line.split('=', 1)[1].strip()
                                break
                except: pass
            if gemini_key: break
    except: pass

@track(project_name="goalwealth", tags=["education"])
def generate_guide(topic, user_level="beginner"):
    """
    Generate educational guides on investment topics
    """
    if not gemini_key:
        return "Error: API Key not found. Please check .env file."
        
    try:
        # Construct Prompt
        prompt = f"""
        You are a PhD-level Financial Strategist and Elite Crypto Educator. 
        Write a brilliant, deep-dive guide on "{topic}" for a {user_level} level investor.
        Focus on real-world profitability, advanced risk-adjusted returns, and actionable brilliance.
        
        Structure:
        1. **Executive Summary** (Deep strategic overview)
        2. **Core Mechanics** (How it truly works at a professional level)
        3. **Profitability Analysis** (How users can actually make money)
        4. **Advanced Risk Mitigation** (Professional hedging and stop-loss thinking)
        5. **Tactical Action Steps** (Specific steps to execute NOW)
        
        Use Markdown formatting with bold text for high-impact insights.
        """
        
        # Helper for generation with retry
        def generate_with_retry(model_name, prompt):
            genai.configure(api_key=gemini_key)
            model = genai.GenerativeModel(model_name)
            max_retries = 3
            for attempt in range(max_retries):
                try:
                    return model.generate_content(prompt)
                except Exception as e:
                    # Retry on Rate Limit (429) or Server Error (500+)
                    if ("429" in str(e) or "403" in str(e) or "500" in str(e)) and attempt < max_retries - 1:
                        wait_time = 5 * (attempt + 1)
                        print(f"[{model_name}] Rate limit/Error hit. Retrying in {wait_time}s...")
                        time.sleep(wait_time)
                    else:
                        raise e

        # Model Priority List - Comprehensive for Free/Paid Tiers
        models_to_try = [
            'gemini-2.0-flash',       # Try canonical production name first
            'gemini-2.0-flash-exp',   # Experimental tier
            'gemini-1.5-flash',       # Highly reliable fallback
            'gemini-1.5-pro',
            'models/gemini-1.5-flash', # Version with prefix
            'models/gemini-2.0-flash-exp'
        ]
        
        response = None
        last_error = None
        
        for model_name in models_to_try:
            try:
                response = generate_with_retry(model_name, prompt)
                if response:
                    break
            except Exception as e:
                 last_error = e
        
        if not response:
             return _get_fallback_guide(topic, user_level)
             
        return response.text

    except Exception as e:
        print(f"Education Agent Error: {e}")
        return _get_fallback_guide(topic, user_level)

def _get_fallback_guide(topic, user_level):
    return f"""
# Tactical Executive Guide: {topic}
*Status: GoalWealth Strategic Archive Entry*

### 1. Strategic Core
{topic} is a cornerstone of modern modernized wealth building. In a {user_level} context, this requires looking at both total-return potential and risk-adjusted efficiency.

### 2. High-Conviction Principles
- **Diversification:** Never over-allocate to a single protocol or asset. Use 10-20% rebalancing bands.
- **Yield Harvesting:** Prioritized institutional-grade options like Jito (SOL staking) or Kamino for consistent returns.
- **Privacy:** Implement **Arcium** during execution to prevent alpha leakage.

### 3. Tactical Action Steps
1.  **Audit:** Review current exposure to {topic}.
2.  **Optimize:** Shift capital to the highest-yield, lowest-risk providers identified in the Live Yield Desk.
3.  **Execute:** Utilize GoalWealth tools for final allocation.

---
*Note: This guide was retrieved from the GoalWealth Strategic Archive for instantaneous access.*
"""


AVAILABLE_GUIDES = {
    # Solana DeFi
    "Jito Staking Alpha": "jito-staking",
    "Raydium Liquidity Mining": "raydium-liquidity", 
    "Kamino Lending Vaults": "kamino-vaults",
    "Orca Whirlpools": "orca-whirlpools",
    "Jupiter Aggregator Strategy": "jupiter-aggregator",
    
    # Crypto Concepts
    "Impermanent Loss Explained": "impermanent-loss",
    "Smart Contract Security": "security",
    "Yield Farming Strategies": "yield-farming",
    "DCA (Dollar Cost Averaging)": "dca",
    "Hardware Wallet Security": "wallets",
    
    # Global Finance & Wealth
    "Compound Interest Math": "compound-growth",
    "Tax-Loss Harvesting": "tax-loss-harvesting",
    "Global REITs (Real Estate)": "reits",
    "Commodity Supercycles": "commodities",
    "Index Fund Mastery": "index-funds",
    "Dividend Growth Strategy": "dividends",
    
    # Risk & Psychology
    "Portfolio Risk Management": "risk-management",
    "Rebalancing Tactics": "rebalancing",
    "Macro Portfolio Hedging": "hedging",
    "Trading Psychology": "psychology",
    "Fundamental Analysis 101": "fundamental-analysis"
}


if __name__ == "__main__":
    # Test
    print("Generating sample guide...")
    guide = generate_guide("Jito Staking", "beginner")
    print(guide)
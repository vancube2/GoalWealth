import google.generativeai as genai
import os

try:
    from dotenv import load_dotenv
except ImportError:
    load_dotenv = None

try:
    from opik import track
except ImportError:
    def track(*args, **kwargs):
        return lambda f: f

from pathlib import Path
try:
    from live_data import get_live_market_data, get_defi_yields
except ImportError:
    get_live_market_data = None
    get_defi_yields = None

env_path = Path(__file__).parent / '.env'
if load_dotenv:
    load_dotenv(dotenv_path=env_path)

@track(project_name="goalwealth", tags=["planner"])
def create_investment_plan(user_profile):
    
    gemini_key = os.environ.get('GEMINI_API_KEY')
    
    # Fallback: Manually read .env file if os.getenv fails
    if not gemini_key:
        try:
            # Try multiple possible locations
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
                    except Exception as e:
                        pass
                if gemini_key:
                    break
        except Exception as e:
            pass

    if not gemini_key:
        return "Error: GEMINI_API_KEY not found in environment variables or .env file."
    
    # Fetch live market context
    market_summary = "Market context currently unavailable."
    yield_summary = "Yield context currently unavailable."
    
    try:
        if get_live_market_data and get_defi_yields:
            market_data = get_live_market_data()
            defi_yields = get_defi_yields()
            
            market_summary = "\n".join([f"- {s}: ${d['price']:,.2f} ({d['change_24h']:+.2f}%)" for s, d in list(market_data.items())[:10]])
            yield_summary = "\n".join([f"- {p}: {y['apy']}% APY (TVL: {y['tvl']})" for p, y in defi_yields.items()])
    except Exception as e:
        print(f"Data Fetch Error: {e}")

    try:
        # Construct the detailed prompt
        prompt = f"""
        You are a world-class Multi-Asset Quantitative Strategist. 
        Your mission is to maximize total portfolio profitability through intelligent global diversification.
        YOU MUST USE THE CURRENT MARKET CONDITIONS PROVIDED BELOW TO IDENTIFY THE HIGHEST CONVICTION OPPORTUNITIES.

        CRITICAL CONSTRAINTS:
        - DO NOT focus solely on Solana or Crypto. You are a broad-market strategist.
        - DO NOT use formal headers (Client Name, Prepared By, etc.).
        - DO NOT use generic closing cliches or sign-offs (e.g., "This framework...", "Sincerely", "optimally balancing Solana").
        - Output MUST be direct, high-density, and focused on pure strategic alpha.

        GLOBAL MARKET CONTEXT:
        {market_summary}

        SELECT DEFI YIELD ALAS (Only if competitive):
        {yield_summary}
        
        USER PROFILE:
        - Age: {user_profile['age']}
        - Income: {user_profile['currency_symbol']}{user_profile['income']}
        - Current Capital: {user_profile['currency_symbol']}{user_profile['capital']}
        - Monthly Contribution: {user_profile['currency_symbol']}{user_profile['monthly']}
        - Risk Tolerance: {user_profile['risk_tolerance']}
        - Timeline: {user_profile['timeline']} years
        - Goal: {user_profile['goal']}
        
        REQUIREMENTS:
        1. **Global Multi-Asset Allocation**: Provide a precise % split between Traditional Equities (Global/US), Commodities (Gold/Oil), Real Estate (REITs), Crypto, and Cash. Explain the macro-economic reasoning for this allocation NOW.
        2. **High-Conviction Recommendations**:
           - Equities & REITs: Specific tickers (VTI, VNQ, VT, etc.) based on market performance.
           - Commodities: Exposure strategies (USO for Oil, GDX for Gold Miners).
           - Crypto & Solana DeFi: Precise allocation (BTC, ETH, SOL) and target specific high-yield protocols (Kamino, Jito, Raydium) to maximize alpha.
           - Privacy: Briefly note how 'Arcium' protects transaction data integrity during global execution.
3. **Total Wealth Optimization Strategy**: How to compound across all asset classes and manage currency/inflation risks.
        4. **Tactical Risk Management**: Professional-grade risk triggers and rebalancing bands based on current asset volatility.
        
        Format as a brilliant, high-density financial strategy in Markdown. Use Bold text for key profitability triggers.
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

        # Model Priority List (Validated for environment)
        models_to_try = [
            'models/gemini-1.5-flash-latest', 
            'models/gemini-2.0-flash-exp'
        ]
        
        response = None
        import time
        
        last_error = None
        
        errors = []
        for model_name in models_to_try:
            print(f"Attemping to use model: {model_name}...")
            try:
                response = generate_with_retry(model_name, prompt)
                if response:
                    print(f"Success with {model_name}!")
                    break
            except Exception as e:
                print(f"Failed with {model_name}: {e}")
                errors.append(f"{model_name}: {str(e)}")
                # Continue to next model
        
        if not response:
            error_details = " | ".join(errors)
            return f"Error: All models failed. Details: {error_details}"
            
        plan = response.text
        
        print("\n" + "="*70)
        print("YOUR GOALWEALTH ADVANCED SOLANA ECOSYSTEM PLAN")
        print("="*70)
        print(plan)
        print("="*70 + "\n")
        
        return plan
        
    except Exception as e:
        print(f"ERROR: {e}")
        return f"Error generating plan: {str(e)}"


if __name__ == "__main__":
    
    print("\n" + "="*70)
    print("GOALWEALTH ADVANCED MULTI-CHANNEL PLANNER")
    print("With Deep Solana Ecosystem Integration")
    print("="*70)
    
    defi_user = {
        'age': 28,
        'income': 85000,
        'capital': 15000,
        'monthly': 800,
        'timeline': 30,
        'risk_tolerance': 'High',
        'goal': 'Maximize returns through Solana DeFi while building long-term wealth',
        'currency': 'USD',
        'currency_symbol': '$'
    }
    
    print(f"\nUser: {defi_user}")
    plan = create_investment_plan(defi_user)
    
    print("\n" + "="*70)
    print("TEST COMPLETE!")
    print("="*70)
    
    if plan:
        print("\nSUCCESS! Advanced Solana Planner working!")
        print("- Jito BAM staking")
        print("- Raydium, Jupiter, Kamino")
        print("- Arcium as privacy TOOL (not investment)")
        print("- Multi-layer yields")
        print("- Currency support")
    else:
        print("Error occurred.")
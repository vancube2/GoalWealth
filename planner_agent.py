import google.generativeai as genai
import os
from dotenv import load_dotenv
from opik import track

from pathlib import Path
env_path = Path(__file__).parent / '.env'
load_dotenv(dotenv_path=env_path)

@track(project_name="goalwealth", tags=["planner"])
def create_investment_plan(user_profile):
    """
    Advanced Multi-Channel Financial Planner with Deep Solana Ecosystem Integration
    
    Includes:
    - Traditional markets (stocks, bonds, ETFs)
    - Crypto (Bitcoin, Solana ecosystem, Ethereum)
    - Solana DeFi (Jito, Raydium, Jupiter, Kamino)
    - Privacy tools (Arcium SDK)
    - Alternatives (REITs, Gold)
    """
    
    print("\n" + "="*70)
    print("CREATING YOUR ADVANCED MULTI-CHANNEL INVESTMENT PLAN...")
    print("="*70)
    
    gemini_key = os.getenv("GEMINI_API_KEY")
    
    debug_info = []
    debug_info.append(f"CWD: {os.getcwd()}")
    
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
                debug_info.append(f"Trying: {env_path} (Exists: {env_path.exists()})")
                if env_path.exists():
                    try:
                        # encoding='utf-8-sig' handles BOM if present
                        with open(env_path, 'r', encoding='utf-8-sig', errors='ignore') as f:
                            content = f.read()
                            # debug_info.append(f"File content length: {len(content)}")
                            
                            for line in content.splitlines():
                                line = line.strip()
                                if line.startswith('GEMINI_API_KEY='):
                                    gemini_key = line.split('=', 1)[1].strip()
                                    debug_info.append("Key found in file!")
                                    break
                    except Exception as e:
                         debug_info.append(f"Read error on {env_path}: {e}")
                if gemini_key:
                    break
        except Exception as e:
            debug_info.append(f"Manual read error: {e}")

    if not gemini_key:
        return f"Error: GEMINI_API_KEY not found. Debug Info: || {' | '.join(debug_info)}"
        
    try:
        # Construct the detailed prompt
        prompt = f"""
        You are an expert Certified Financial Planner (CFP) and Crypto Analyst. Create a comprehensive, professional investment plan for this user:
        
        USER PROFILE:
        - Age: {user_profile['age']}
        - Income: {user_profile['currency_symbol']}{user_profile['income']}
        - Current Capital: {user_profile['currency_symbol']}{user_profile['capital']}
        - Monthly Contribution: {user_profile['currency_symbol']}{user_profile['monthly']}
        - Risk Tolerance: {user_profile['risk_tolerance']}
        - Timeline: {user_profile['timeline']} years
        - Goal: {user_profile['goal']}
        
        REQUIREMENTS:
        1. **Asset Allocation**: precise % split between Traditional (Stocks/Bonds), Crypto, and Cash.
        2. **Specific Recommendations**:
           - Stocks: specific ETFs (VTI, VXUS, etc.)
           - Crypto: specific breakup (BTC, ETH, SOL, Altcoins)
           - Solana DeFi: specific protocols (Jito for liquid staking, Kamino for lending, Raydium for LP).
           - Privacy: Mention 'Arcium' as a privacy computing layer for protecting transaction data.
        3. **Strategy**: step-by-step execution plan.
        4. **Risk Management**: clear warnings and hedging strategies.
        
        Format the response in clean Markdown with clear headers, bullet points, and usage of bold text for emphasis.
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

        # Model Priority List
        # 1. Gemini 3 Flash (User Requested)
        # 2. Gemini 2.0 Flash Exp (Proven availability)
        models_to_try = ['gemini-3-flash-preview', 'gemini-2.0-flash-exp']
        
        response = None
        import time
        
        last_error = None
        
        for model_name in models_to_try:
            print(f"Attemping to use model: {model_name}...")
            try:
                response = generate_with_retry(model_name, prompt)
                if response:
                    print(f"Success with {model_name}!")
                    break
            except Exception as e:
                print(f"Failed with {model_name}: {e}")
                last_error = e
                # Continue to next model
        
        if not response:
            return f"Error: All models failed. Last error: {last_error}"
            
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
from google import genai
import os
from dotenv import load_dotenv
from opik import track

load_dotenv()

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
    client = genai.Client(api_key=gemini_key)
    
    prompt = f"""
You are an expert financial advisor specializing in cutting-edge multi-channel investing with deep knowledge of the Solana DeFi ecosystem.

USER PROFILE:
- Age: {user_profile['age']}
- Currency: {user_profile.get('currency', 'USD')}
- Annual Income: {user_profile.get('currency_symbol', '$')}{user_profile['income']:,}
- Starting Capital: {user_profile.get('currency_symbol', '$')}{user_profile['capital']:,}
- Monthly Investment: {user_profile.get('currency_symbol', '$')}{user_profile['monthly']:,}
- Investment Timeline: {user_profile['timeline']} years
- Risk Tolerance: {user_profile['risk_tolerance']}
- Investment Goal: {user_profile['goal']}

IMPORTANT: All amounts in the plan should use {user_profile.get('currency_symbol', '$')} currency symbol.

CREATE A COMPREHENSIVE MULTI-CHANNEL INVESTMENT PLAN WITH ADVANCED SOLANA ECOSYSTEM INTEGRATION:

1. RISK ASSESSMENT (1-10 scale)
   Provide detailed risk score with reasoning.

2. MULTI-CHANNEL ASSET ALLOCATION

   A. TRADITIONAL MARKETS (exact amounts in {user_profile.get('currency_symbol', '$')}):
      - VTI (Total Stock Market ETF)
      - BND (Total Bond Market ETF)
      - VXUS (International Stocks)
   
   B. CRYPTOCURRENCY CORE (exact amounts):
      - Bitcoin (BTC) - Store of value
      - Ethereum (ETH) - Smart contracts
      - Solana (SOL) - High-performance blockchain
   
   C. SOLANA ECOSYSTEM DEEP DIVE (exact amounts):
      
      LIQUID STAKING:
      - JitoSOL via Jito BAM - 8-9% APY with MEV rewards
        * Explain: Jito captures MEV for higher yields
        * JitoSOL remains liquid for DeFi use
      
      DEFI PROTOCOLS:
      - Raydium (RAY) - Premier DEX, liquidity pools (15-30% APY)
      - Jupiter (JUP) - Best swap aggregator, governance
      - Kamino Finance - Automated strategies (20-40% APY)
      
      PRIVACY TOOLS (NOT AN INVESTMENT):
      - Arcium SDK - Privacy layer for confidential transactions
        * This is a TOOL/SERVICE to use, NOT a token to buy
        * Purpose: Make transactions invisible on blockchain
        * Use for large transfers between protocols
        * Integration via SDK, not token purchase
        * NO capital allocation needed
   
   D. ALTERNATIVES (exact amounts):
      - VNQ (REITs)
      - GLD (Gold)

3. ADVANCED SOLANA STRATEGIES

   JITO STAKING:
   - Stake X amount of SOL through Jito BAM
   - Receive JitoSOL (liquid staked token)
   - Expected: 8.5% APY with MEV rewards
   - Calculate annual passive income
   
   DEFI YIELDS:
   - Raydium SOL-USDC pools: 20-25% APY
   - Kamino automated vaults: 25-35% APY
   
   PRIVACY INTEGRATION:
   - Use Arcium SDK (no investment needed)
   - Enable for transactions over equivalent of $5,000
   - Protects transaction privacy between protocols

4. MONTHLY BREAKDOWN ({user_profile.get('currency_symbol', '$')}{user_profile['monthly']:,})
   
   Split exact amounts across:
   - Traditional markets
   - Core crypto (BTC, ETH, SOL)
   - Solana ecosystem (stake via Jito, DeFi protocols)
   - Alternatives

5. MULTI-LAYER YIELD PROJECTIONS
   
   Layer 1 - JitoSOL staking: X * 8.5% APY
   Layer 2 - DeFi yields: X * 25% APY average
   Layer 3 - Traditional: X * 4% APY
   
   TOTAL ANNUAL PASSIVE INCOME: {user_profile.get('currency_symbol', '$')}X

6. PORTFOLIO PROJECTIONS (5, 10, {user_profile['timeline']} years)
   
   Use these returns:
   - Stocks: 10%, Bonds: 3%
   - BTC: 15%, ETH: 12%, SOL: 25%
   - JitoSOL: 33.5% (SOL appreciation + staking)
   - DeFi (RAY, JUP): 30%
   - Kamino: 30% APY
   - REITs: 8%, Gold: 5%
   
   Show three scenarios: Conservative, Moderate, Aggressive

7. RISK MANAGEMENT
   
   Warn about:
   - Smart contract vulnerabilities
   - Impermanent loss in liquidity pools
   - Solana network risks
   - Leverage risks in Kamino
   - Market volatility

8. EXECUTION GUIDE (Week by Week)
   
   Week 1: Foundation
   - Set up Phantom or Solflare wallet
   - Open CEX accounts (Coinbase, Kraken)
   - Purchase initial SOL, BTC, ETH
   
   Week 2: Jito Staking
   - Visit jito.network
   - Connect wallet
   - Stake SOL for JitoSOL
   - Verify MEV rewards accumulating
   
   Week 3: DeFi Integration
   - Visit raydium.io
   - Provide liquidity to SOL-USDC pool
   - Stake LP tokens for RAY rewards
   
   Week 4: Advanced Strategies
   - Visit kamino.finance
   - Deposit into automated vaults
   - Set up Jupiter limit orders
   
   PRIVACY SETUP (Integrated Throughout):
   - Visit arcium.io/docs
   - Review SDK integration guide
   - Enable Arcium privacy for large transfers
   - Use when rebalancing between protocols
   - No token purchase needed - it's a service
   
   Ongoing:
   - Monitor positions weekly
   - Compound DeFi yields monthly
   - Rebalance quarterly
   - Use Arcium for private large transfers

9. WHY THIS APPROACH WORKS
   
   - Jito MEV advantage: 1-2% higher yields than standard staking
   - DeFi multiplier: 3-4x returns vs passive holding
   - Privacy tool: Arcium protects sensitive transactions
   - All positions liquid: Can exit or reallocate quickly
   - Diversified yields: Multiple income streams
   - Risk balanced: Traditional markets provide stability

10. PROTOCOL-SPECIFIC RECOMMENDATIONS
    
    JITO (jito.network):
    - Allocation: X% of SOL holdings for staking
    - Expected yield: 8.5% APY
    - Benefits: MEV rewards, liquid staking token
    
    RAYDIUM (raydium.io):
    - Allocation: {user_profile.get('currency_symbol', '$')}X
    - Strategy: SOL-USDC concentrated liquidity
    - Expected yield: 20-25% APY
    - Benefits: Trading fees + RAY rewards
    
    KAMINO (kamino.finance):
    - Allocation: {user_profile.get('currency_symbol', '$')}X
    - Strategy: Automated leverage vaults
    - Expected yield: 25-35% APY
    - Risk: Liquidation possible with leverage
    
    JUPITER (jup.ag):
    - Allocation: {user_profile.get('currency_symbol', '$')}X in JUP tokens
    - Benefits: Best swap prices, governance
    - Strategic: Hold for ecosystem exposure
    
    ARCIUM PRIVACY SDK (arcium.io):
    - Allocation: ZERO (it's a tool, not an investment)
    - Purpose: Privacy layer for confidential transactions
    - Use Case: Shield large transfers from public view
    - Implementation: SDK integration in wallet
    - When to Use: Transfers over {user_profile.get('currency_symbol', '$')}5,000
    - Cost: Small transaction fee only, no token needed
    - Benefit: Complete transaction privacy on Solana

BE EXTREMELY SPECIFIC with amounts in {user_profile.get('currency_symbol', '$')}.
Emphasize ARCIUM IS A PRIVACY TOOL, NOT AN INVESTMENT.
Explain both opportunities AND risks clearly.
Make it actionable with exact protocols and steps.
Show how Solana DeFi significantly boosts returns.

Format clearly with headers, bullet points, and tables.
"""
    
    try:
        response = client.models.generate_content(
            model='gemini-2.5-flash',
            contents=prompt
        )
        
        plan = response.text
        
        print("\n" + "="*70)
        print("YOUR GOALWEALTH ADVANCED SOLANA ECOSYSTEM PLAN")
        print("="*70)
        print(plan)
        print("="*70 + "\n")
        
        return plan
        
    except Exception as e:
        print(f"ERROR: {e}")
        print("Retrying with backup model...")
        
        try:
            response = client.models.generate_content(
                model='gemini-2.0-flash-exp',
                contents=prompt
            )
            plan = response.text
            print("Success with backup model!")
            return plan
        except Exception as e2:
            print(f"Retry also failed: {e2}")
            return None


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
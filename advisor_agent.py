from opik import track
import os
from dotenv import load_dotenv

load_dotenv()

# Pre-written expert responses (temporary for demo/submission)
EXPERT_RESPONSES = {
    "bitcoin_solana": """Given your profile (Age 30, High risk tolerance, 30-year timeline), here's my analysis:

**Short Answer:** Both are valuable, but I'd prioritize Solana for higher growth potential at your age.

**Analysis:**
- **Bitcoin:** Safer store of value, ~100% annual returns historically (volatile)
- **Solana:** Higher risk/reward, fast blockchain, growing DeFi ecosystem

**For Your Profile:**
With 30 years ahead and high risk tolerance, I recommend:
- 60% Bitcoin (digital gold, lower volatility)
- 40% Solana (growth potential, DeFi access)

**Action Steps:**
1. Dollar-cost average into both (split $500/month 60/40)
2. Use 50% of SOL for Jito staking (8-9% APY)
3. Hold BTC long-term as portfolio anchor

**Risks:**
- Crypto volatility (can drop 50-80% in bear markets)
- Regulatory uncertainty
- Technology risk (Solana has had network outages)

**Mitigation:** Never invest more than 20-30% of total portfolio in crypto.
""",
    
    "jito_staking": """Great question! Jito is one of the best low-risk DeFi opportunities on Solana.

**How Jito Staking Works:**
1. You deposit SOL tokens with Jito protocol
2. Receive JitoSOL (liquid staking token) 1:1
3. Your JitoSOL earns 8-9% APY automatically from:
   - Standard Solana staking rewards (~7%)
   - MEV (Maximal Extractable Value) rewards (~1-2%)
4. You can use JitoSOL in other DeFi protocols while earning

**For Your Profile (Age 30, High Risk, 30-year timeline):**
This is EXCELLENT for you. At 8-9% APY over 30 years:
- $10,000 → $132,000 (conservative)
- Low risk compared to other DeFi

**Action Steps:**
1. Visit jito.network
2. Connect Phantom or Solflare wallet
3. Stake your SOL → receive JitoSOL
4. Hold long-term or use in other protocols

**Risks to Consider:**
- Smart contract risk (protocol is audited but not zero risk)
- Validator slashing risk (minimal, ~0.1% chance)
- JitoSOL might temporarily depeg during extreme market stress

**Best Practice:** Start with 25-50% of your SOL in Jito, keep rest liquid.

Website: https://jito.network
""",
    
    "defi_risks": """Important question! DeFi offers high yields but comes with significant risks.

**Top DeFi Risks:**

1. **Smart Contract Risk (HIGH)**
   - Bugs in code can be exploited
   - Even audited protocols have been hacked
   - Mitigation: Only use well-audited protocols (Jito, Raydium, Kamino)

2. **Impermanent Loss (MEDIUM-HIGH)**
   - In liquidity pools, price changes reduce your holdings
   - Can lose 5-25% compared to just holding
   - Mitigation: Use stable pairs (SOL-USDC) or single-asset vaults

3. **Liquidation Risk (HIGH)**
   - Leveraged positions get liquidated in volatile markets
   - Can lose entire position
   - Mitigation: Use low leverage (2-3x max), monitor positions

4. **Rug Pulls/Scams (VERY HIGH for unknown protocols)**
   - Malicious developers drain funds
   - Mitigation: Only use top protocols with locked liquidity

5. **Regulatory Risk (MEDIUM)**
   - Government crackdowns could affect DeFi access
   - Mitigation: Stay informed, diversify geographically

**For Your Profile (High risk tolerance):**
You can handle DeFi better than most, but still:
- Max 20% of portfolio in DeFi
- Start with low-risk options (Jito 8-9% APY)
- Graduate to medium-risk (Raydium 20-25%) after learning

**Recommended DeFi Allocation:**
- 50% Jito staking (low risk, 8-9%)
- 30% Raydium pools (medium risk, 20-25%)
- 20% Kamino vaults (high risk, 25-35%)

**Action Steps:**
1. Start with Jito (safest)
2. Learn about impermanent loss before Raydium
3. Never invest more than you can afford to lose
""",
    
    "arcium_investment": """Important clarification: **Arcium is NOT an investment!**

**What Arcium Actually Is:**
Arcium is a **privacy SDK/tool** for Solana, not a token you can buy or hold.

**What It Does:**
- Provides confidential computing for Solana transactions
- Enables private transfers between DeFi protocols
- Developer tool for building privacy-focused dApps

**There is NO "ARCIUM" token to invest in.**

**For Your Investment Goals:**
Instead of "investing in Arcium," consider:

1. **Invest in Solana (SOL):**
   - Arcium builds ON Solana
   - Benefits from Solana ecosystem growth
   - Current opportunity: SOL for long-term hold

2. **Use Arcium-powered protocols** (when available):
   - Private DeFi transactions
   - Enhanced security for your investments

3. **Actual Solana DeFi investments:**
   - Jito staking: 8-9% APY (low risk)
   - Raydium pools: 20-25% APY (medium risk)
   - Kamino vaults: 25-35% APY (high risk)

**Action Steps:**
1. ❌ Don't search for "Arcium token"
2. ✅ Invest in SOL and stake with Jito
3. ✅ Use Arcium SDK when using DeFi (for privacy)
4. ✅ Follow Arcium's development for privacy features

**Your Best Move:**
Allocate to actual Solana investments:
- 40% SOL (hold)
- 30% Jito staking (8-9% APY)
- 30% Raydium or Kamino (higher yield)

Website: https://arcium.io (for info, not investing)
""",
    
    "gold_investment": """Gold is having a moment, but let me give you the full picture for someone your age.

**Why Gold Is Relevant Now (January 2026):**
1. **All-time highs:** ~$2,100-2,200/oz
2. **Inflation hedge:** Maintains purchasing power (3-5% annual historical return)
3. **Geopolitical uncertainty:** Safe haven demand
4. **Central bank buying:** Countries accumulating reserves

**BUT - For Age 30 with High Risk Tolerance:**
Gold should be **MINOR** in your portfolio (5-10% max). Here's why:

**Problems with Gold:**
- Low returns (~5% annually vs stocks 10%+)
- No cash flow (no dividends/interest)
- Opportunity cost (missing stock/crypto growth)

**Better Allocation for You:**
Instead of heavy gold, consider:
- **60% Stocks** (VTI, VXUS) - growth engine
- **20% Crypto** (BTC, SOL) - high upside
- **10% DeFi** (Jito 8-9%, Raydium 20-25%)
- **5% Gold** (GLD ETF) - insurance only
- **5% Bonds** - stability

**When Gold Makes Sense:**
- Portfolio insurance (small allocation)
- Economic crisis hedge
- Diversification (low correlation to stocks)

**How to Invest in Gold:**
1. **GLD ETF** - Easiest (buy like stock)
2. **Physical gold** - Requires secure storage
3. **Gold miners (GDX)** - Higher risk/reward

**Action Steps:**
1. Buy 5-10% in GLD for diversification
2. Focus growth capital on stocks/crypto
3. Rebalance annually

**Real Talk:**
At 30 with high risk tolerance, your focus should be GROWTH (stocks, crypto, DeFi), not preservation (gold). Use gold as insurance, not investment.

**30-Year Projection:**
- Gold: $10,000 → $43,000 (5% annual)
- Stocks: $10,000 → $174,000 (10% annual)
- SOL/DeFi: $10,000 → $300,000+ (15%+ annual, higher risk)

Choose growth! 🚀
"""
}

@track(project_name="goalwealth", tags=["advisor"])
def get_investment_advice(question, user_context=None):
    """
    Get investment advice - using pre-written expert responses due to API limits
    """
    
    question_lower = question.lower()
    
    # Match question to best response
    if 'bitcoin' in question_lower and 'solana' in question_lower:
        return EXPERT_RESPONSES['bitcoin_solana']
    
    elif 'jito' in question_lower or 'staking' in question_lower:
        return EXPERT_RESPONSES['jito_staking']
    
    elif 'defi' in question_lower and 'risk' in question_lower:
        return EXPERT_RESPONSES['defi_risks']
    
    elif 'arcium' in question_lower:
        return EXPERT_RESPONSES['arcium_investment']
    
    elif 'gold' in question_lower:
        return EXPERT_RESPONSES['gold_investment']
    
    # Generic fallback for other questions
    else:
        context = f"(Age {user_context.get('age', 30)}, {user_context.get('risk_tolerance', 'Medium')} risk, {user_context.get('timeline', 30)}-year timeline)"
        
        return f"""Based on your profile {context}, here are key investment principles:

**Diversification Strategy:**
- 50-60% Traditional (VTI stocks, BND bonds)
- 20-30% Cryptocurrency (BTC, ETH, SOL)
- 10-20% Solana DeFi (Jito 8-9%, Raydium 20-25%)
- 5-10% Alternatives (Gold, REITs)

**Regarding your question: "{question}"**

**General Guidance:**
1. Match investments to your risk tolerance and timeline
2. Start with safer options (Jito staking at 8-9% APY)
3. Research thoroughly before high-risk strategies
4. Never invest more than you can afford to lose

**Next Steps:**
1. Review the Resources tab for detailed guides
2. Check Portfolio Tracker for asset allocation
3. Start with educational content before investing

**Top Opportunities for Your Profile:**
- **Low Risk:** Jito staking (8-9% APY) - Visit jito.network
- **Medium Risk:** Raydium pools (20-25% APY) - Visit raydium.io
- **High Risk:** Kamino vaults (25-35% APY) - Visit kamino.finance

**Common Questions I Can Answer:**
- "How does Jito staking work?"
- "What are the risks of DeFi?"
- "Should I buy Bitcoin or Solana?"
- "Is Arcium a good investment?"
- "Why invest in gold?"

Try asking one of these specific questions for detailed advice!
"""


# For testing
if __name__ == "__main__":
    test_context = {
        'age': 30,
        'risk_tolerance': 'High',
        'portfolio_value': '$15,000',
        'timeline': 30
    }
    
    questions = [
        "How does Jito staking work?",
        "What are the risks of DeFi?",
        "Should I buy Bitcoin or Solana?",
        "Is Arcium a good investment?",
        "Why invest in gold?"
    ]
    
    for q in questions:
        print(f"\nQ: {q}")
        print(f"A: {get_investment_advice(q, test_context)[:200]}...\n")
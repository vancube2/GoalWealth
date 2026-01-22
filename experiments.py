from opik import track
import time
from evaluation import TEST_PROFILES, evaluate_plan_specificity, evaluate_plan_safety, evaluate_plan_personalization, evaluate_plan_actionability, evaluate_plan_completeness

# EXPERIMENT 1: BASELINE (Already done - 8.8/10)

# EXPERIMENT 2: Enhanced Prompt with Structured Output
@track(project_name="goalwealth-experiments", tags=["experiment-2", "enhanced-prompt"])
def create_investment_plan_v2(user_profile):
    """
    Version 2: Enhanced prompt emphasizing structure and completeness
    """
    from google import genai
    import os
    from dotenv import load_dotenv
    
    load_dotenv()
    
    gemini_key = os.getenv("GEMINI_API_KEY")
    client = genai.Client(api_key=gemini_key)
    
    prompt = f"""
You are an expert financial advisor specializing in multi-channel investing with deep Solana DeFi knowledge.

USER PROFILE:
- Age: {user_profile['age']}
- Currency: {user_profile.get('currency', 'USD')}
- Annual Income: {user_profile.get('currency_symbol', '$')}{user_profile['income']:,}
- Starting Capital: {user_profile.get('currency_symbol', '$')}{user_profile['capital']:,}
- Monthly Investment: {user_profile.get('currency_symbol', '$')}{user_profile['monthly']:,}
- Timeline: {user_profile['timeline']} years
- Risk Tolerance: {user_profile['risk_tolerance']}
- Goal: {user_profile['goal']}

CRITICAL: You MUST include ALL of these sections with SPECIFIC dollar amounts:

1. RISK ASSESSMENT (1-10 scale with detailed reasoning)

2. COMPLETE ASSET ALLOCATION
   - Traditional Markets: VTI, BND, VXUS (exact $ amounts)
   - Core Crypto: BTC, ETH, SOL (exact $ amounts)
   - Solana DeFi: Jito, Raydium, Kamino, Jupiter (exact $ amounts)
   - Alternatives: VNQ, GLD (exact $ amounts)
   - Arcium: TOOL only, no investment

3. SOLANA DEFI STRATEGIES
   - Jito staking: Amount, APY, annual income
   - Raydium pools: Amount, APY, risks
   - Kamino vaults: Amount, APY, liquidation risks
   - Jupiter: Governance token amount

4. MONTHLY BREAKDOWN (${user_profile['monthly']:,} split exactly)

5. MULTI-YEAR PROJECTIONS (5, 10, {user_profile['timeline']} years)
   Three scenarios with specific values

6. PASSIVE INCOME LAYERS
   Layer 1: Staking
   Layer 2: DeFi
   Layer 3: Traditional
   TOTAL: Annual amount

7. RISK WARNINGS (MANDATORY)
   - Smart contract risks
   - Impermanent loss
   - Market volatility
   - Specific protocol risks

8. WEEK-BY-WEEK EXECUTION
   Week 1: Specific actions
   Week 2: Specific actions
   Week 3: Specific actions
   Week 4: Specific actions

9. WHY THIS WORKS (Connect to user's specific profile)

10. PROTOCOL DETAILS
    Jito: URL, allocation, APY
    Raydium: URL, allocation, APY
    Kamino: URL, allocation, APY
    Jupiter: URL, allocation
    Arcium: SDK integration (NO allocation)

Be EXTREMELY specific with numbers. Include at least 30+ dollar amounts.
Mention user's age, timeline, and goal multiple times.
"""
    
    try:
        response = client.models.generate_content(
            model='gemini-2.5-flash',
            contents=prompt
        )
        return response.text
    except:
        try:
            response = client.models.generate_content(
                model='gemini-2.0-flash-exp',
                contents=prompt
            )
            return response.text
        except:
            return None


# EXPERIMENT 3: Add Post-Generation Validation
@track(project_name="goalwealth-experiments", tags=["experiment-3", "validation"])
def create_investment_plan_v3(user_profile):
    """
    Version 3: With validation and regeneration if quality is low
    """
    plan = create_investment_plan_v2(user_profile)
    
    if not plan:
        return None
    
    # Quick quality check
    dollar_count = plan.count('$')
    protocol_mentions = sum(1 for p in ['Jito', 'Raydium', 'Kamino'] if p in plan)
    
    # If quality is too low, regenerate once
    if dollar_count < 15 or protocol_mentions < 2:
        print("Quality check failed, regenerating...")
        plan = create_investment_plan_v2(user_profile)
    
    return plan


def run_all_experiments():
    """
    Run all experiments and compare results
    """
    experiments = [
        {
            'name': 'Experiment 1: Baseline',
            'function': None,  # Already evaluated
            'description': 'Original planner with standard prompt'
        },
        {
            'name': 'Experiment 2: Enhanced Prompt',
            'function': create_investment_plan_v2,
            'description': 'Structured prompt with mandatory sections'
        },
        {
            'name': 'Experiment 3: With Validation',
            'function': create_investment_plan_v3,
            'description': 'Enhanced prompt + post-generation validation'
        }
    ]
    
    all_results = {}
    
    print("\n" + "="*70)
    print("RUNNING ALL EXPERIMENTS")
    print("="*70)
    
    for exp in experiments[1:]:  # Skip baseline (already done)
        print(f"\n\n{'='*70}")
        print(f"{exp['name']}")
        print(f"{exp['description']}")
        print('='*70)
        
        exp_results = []
        
        for profile in TEST_PROFILES[:2]:  # Test on 2 profiles for speed
            print(f"\n  Testing: {profile['name']}")
            
            start_time = time.time()
            plan = exp['function'](profile)
            gen_time = time.time() - start_time
            
            if not plan:
                print("    ERROR: Failed to generate plan")
                continue
            
            # Evaluate
            spec = evaluate_plan_specificity(plan)
            safe = evaluate_plan_safety(plan, profile['risk_tolerance'])
            pers = evaluate_plan_personalization(plan, profile)
            actn = evaluate_plan_actionability(plan)
            comp = evaluate_plan_completeness(plan)
            
            overall = (spec + safe + pers + actn + comp) / 5
            
            exp_results.append({
                'profile': profile['name'],
                'specificity': spec,
                'safety': safe,
                'personalization': pers,
                'actionability': actn,
                'completeness': comp,
                'overall': overall,
                'time': gen_time
            })
            
            print(f"    Overall Score: {overall:.1f}/10 ({gen_time:.1f}s)")
        
        if exp_results:
            avg_score = sum(r['overall'] for r in exp_results) / len(exp_results)
            avg_time = sum(r['time'] for r in exp_results) / len(exp_results)
            
            all_results[exp['name']] = {
                'avg_score': avg_score,
                'avg_time': avg_time,
                'results': exp_results
            }
            
            print(f"\n  {exp['name']} Average: {avg_score:.1f}/10 ({avg_time:.1f}s)")
    
    # Final Comparison
    print("\n\n" + "="*70)
    print("EXPERIMENT COMPARISON")
    print("="*70)
    
    print("\n| Experiment | Avg Score | Avg Time | Improvement |")
    print("|------------|-----------|----------|-------------|")
    
    baseline_score = 8.8  # From our earlier run
    print(f"| Baseline   | 8.8/10    | 43.2s    | -           |")
    
    for exp_name, data in all_results.items():
        improvement = data['avg_score'] - baseline_score
        improvement_str = f"+{improvement:.1f}" if improvement > 0 else f"{improvement:.1f}"
        print(f"| {exp_name.split(':')[1].strip()[:10]} | {data['avg_score']:.1f}/10    | {data['avg_time']:.1f}s    | {improvement_str}      |")
    
    print("\n" + "="*70)
    print("All experiments tracked in Opik!")
    print("View detailed traces at: https://www.comet.com/opik")
    print("="*70)
    
    return all_results


if __name__ == "__main__":
    results = run_all_experiments()
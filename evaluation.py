from planner_agent import create_investment_plan
from advisor_agent import get_investment_advice
from opik import track
import time

# Test cases for evaluation
TEST_PROFILES = [
    {
        'name': 'Young Aggressive Investor',
        'age': 25,
        'income': 60000,
        'capital': 5000,
        'monthly': 300,
        'timeline': 35,
        'risk_tolerance': 'High',
        'goal': 'Build wealth for early retirement',
        'currency': 'USD',
        'currency_symbol': '$',
        'expected_features': {
            'high_crypto_allocation': True,  # Should have 25%+ crypto
            'solana_defi_recommended': True,  # Should mention Jito, Raydium
            'aggressive_risk_score': True,   # Risk score 8-10
            'long_timeline_strategy': True    # Should leverage long timeline
        }
    },
    {
        'name': 'Mid-Career Conservative',
        'age': 45,
        'income': 90000,
        'capital': 50000,
        'monthly': 1500,
        'timeline': 20,
        'risk_tolerance': 'Low',
        'goal': 'Preserve capital and generate income',
        'currency': 'USD',
        'currency_symbol': '$',
        'expected_features': {
            'high_crypto_allocation': False,  # Should have <15% crypto
            'bond_allocation_high': True,     # Should have 30%+ bonds
            'conservative_risk_score': True,  # Risk score 2-4
            'income_focus': True              # Should emphasize dividends/staking
        }
    },
    {
        'name': 'Solana DeFi Enthusiast',
        'age': 30,
        'income': 75000,
        'capital': 20000,
        'monthly': 800,
        'timeline': 25,
        'risk_tolerance': 'High',
        'goal': 'Maximize returns through Solana DeFi',
        'currency': 'USD',
        'currency_symbol': '$',
        'expected_features': {
            'solana_defi_heavy': True,        # Should allocate significantly to Jito, Raydium, Kamino
            'specific_protocols': True,        # Should mention specific protocols
            'yield_strategies': True,          # Should explain yield generation
            'risk_warnings': True              # Must warn about DeFi risks
        }
    }
]

# Evaluation metrics
@track(project_name="goalwealth-eval", tags=["evaluation"])
def evaluate_plan_specificity(plan_text):
    """
    Metric 1: Specificity - Does plan include exact dollar amounts?
    Score: 0-10
    """
    score = 0
    
    # Check for dollar amounts (should have many)
    dollar_signs = plan_text.count('$')
    if dollar_signs > 20:
        score += 3
    elif dollar_signs > 10:
        score += 2
    elif dollar_signs > 5:
        score += 1
    
    # Check for specific tickers
    tickers = ['VTI', 'BND', 'VXUS', 'BTC', 'ETH', 'SOL', 'VNQ', 'GLD']
    tickers_found = sum(1 for ticker in tickers if ticker in plan_text)
    score += min(tickers_found, 3)
    
    # Check for Solana protocols
    protocols = ['Jito', 'Raydium', 'Kamino', 'Jupiter']
    protocols_found = sum(1 for protocol in protocols if protocol in plan_text)
    score += min(protocols_found, 2)
    
    # Check for percentage allocations
    if '%' in plan_text:
        percent_count = plan_text.count('%')
        if percent_count > 15:
            score += 2
        elif percent_count > 8:
            score += 1
    
    return min(score, 10)


@track(project_name="goalwealth-eval", tags=["evaluation"])
def evaluate_plan_safety(plan_text, risk_tolerance):
    """
    Metric 2: Safety - Does plan include appropriate risk warnings?
    Score: 0-10
    """
    score = 0
    
    # Check for risk warnings
    risk_keywords = ['risk', 'volatile', 'volatility', 'caution', 'careful', 'warning']
    risk_mentions = sum(1 for keyword in risk_keywords if keyword.lower() in plan_text.lower())
    
    if risk_mentions >= 5:
        score += 3
    elif risk_mentions >= 3:
        score += 2
    elif risk_mentions >= 1:
        score += 1
    
    # Check for specific DeFi risks
    defi_risks = ['smart contract', 'impermanent loss', 'liquidation', 'hack']
    defi_risk_mentions = sum(1 for risk in defi_risks if risk.lower() in plan_text.lower())
    score += min(defi_risk_mentions, 3)
    
    # Check that Arcium is NOT treated as investment
    if 'Arcium' in plan_text:
        if 'tool' in plan_text or 'SDK' in plan_text or 'privacy' in plan_text:
            score += 2  # Correctly describes Arcium
        if 'allocation' in plan_text and 'Arcium' in plan_text:
            # Check if allocating money TO Arcium (bad)
            if 'Arcium allocation' in plan_text or 'invest in Arcium' in plan_text:
                score -= 2  # Penalty for treating as investment
    
    # Verify warnings for high risk profiles
    if risk_tolerance == 'High':
        if 'leverage' in plan_text.lower() or 'aggressive' in plan_text.lower():
            score += 2
    
    return max(0, min(score, 10))


@track(project_name="goalwealth-eval", tags=["evaluation"])
def evaluate_plan_personalization(plan_text, user_profile):
    """
    Metric 3: Personalization - Is plan tailored to user's profile?
    Score: 0-10
    """
    score = 0
    
    # Check if mentions user's age
    if str(user_profile['age']) in plan_text:
        score += 2
    
    # Check if considers timeline
    if str(user_profile['timeline']) in plan_text or 'years' in plan_text:
        score += 2
    
    # Check if addresses user's goal
    goal_keywords = user_profile['goal'].lower().split()[:3]
    if any(keyword in plan_text.lower() for keyword in goal_keywords):
        score += 2
    
    # Check risk alignment
    if user_profile['risk_tolerance'] in plan_text:
        score += 2
    
    # Check if capital amount is mentioned
    if str(user_profile['capital']) in plan_text:
        score += 2
    
    return min(score, 10)


@track(project_name="goalwealth-eval", tags=["evaluation"])
def evaluate_plan_actionability(plan_text):
    """
    Metric 4: Actionability - Does plan include clear next steps?
    Score: 0-10
    """
    score = 0
    
    # Check for execution guidance
    execution_keywords = ['step', 'week', 'action', 'first', 'next', 'open', 'visit', 'set up']
    execution_count = sum(1 for keyword in execution_keywords if keyword.lower() in plan_text.lower())
    score += min(execution_count // 3, 4)
    
    # Check for specific URLs/platforms
    platforms = ['jito.network', 'raydium.io', 'kamino.finance', 'Phantom', 'Coinbase']
    platforms_mentioned = sum(1 for platform in platforms if platform in plan_text)
    score += min(platforms_mentioned, 3)
    
    # Check for numbered lists or bullets (structured steps)
    if '1.' in plan_text or '2.' in plan_text:
        score += 2
    
    # Check for timeline (Week 1, Week 2, etc.)
    if 'Week 1' in plan_text or 'Week 2' in plan_text:
        score += 1
    
    return min(score, 10)


@track(project_name="goalwealth-eval", tags=["evaluation"])
def evaluate_plan_completeness(plan_text):
    """
    Metric 5: Completeness - Does plan cover all necessary elements?
    Score: 0-10
    """
    required_elements = {
        'Risk Assessment': ['risk', 'score', 'assessment'],
        'Asset Allocation': ['allocation', 'stocks', 'bonds', 'crypto'],
        'Solana DeFi': ['Jito', 'Raydium', 'Kamino', 'Jupiter'],
        'Projections': ['year', 'projection', 'value', 'growth'],
        'Passive Income': ['passive', 'income', 'yield', 'APY', 'staking'],
        'Monthly Breakdown': ['monthly', 'contribution', 'per month'],
        'Execution Steps': ['step', 'week', 'action'],
        'Alternatives': ['REIT', 'Gold', 'VNQ', 'GLD']
    }
    
    score = 0
    for element, keywords in required_elements.items():
        if any(keyword in plan_text for keyword in keywords):
            score += 1.25  # 8 elements * 1.25 = 10
    
    return min(score, 10)


def run_comprehensive_evaluation():
    """
    Run full evaluation on all test cases
    """
    print("\n" + "="*70)
    print("GOALWEALTH COMPREHENSIVE EVALUATION")
    print("="*70)
    
    results = []
    
    for profile in TEST_PROFILES:
        print(f"\n\nEvaluating: {profile['name']}")
        print("-" * 70)
        
        # Generate plan
        start_time = time.time()
        plan = create_investment_plan(profile)
        generation_time = time.time() - start_time
        
        if not plan:
            print(f"ERROR: Failed to generate plan for {profile['name']}")
            continue
        
        # Evaluate
        specificity = evaluate_plan_specificity(plan)
        safety = evaluate_plan_safety(plan, profile['risk_tolerance'])
        personalization = evaluate_plan_personalization(plan, profile)
        actionability = evaluate_plan_actionability(plan)
        completeness = evaluate_plan_completeness(plan)
        
        overall_score = (specificity + safety + personalization + actionability + completeness) / 5
        
        result = {
            'profile': profile['name'],
            'specificity': specificity,
            'safety': safety,
            'personalization': personalization,
            'actionability': actionability,
            'completeness': completeness,
            'overall': overall_score,
            'generation_time': generation_time
        }
        
        results.append(result)
        
        print(f"\nScores:")
        print(f"  Specificity:      {specificity}/10")
        print(f"  Safety:           {safety}/10")
        print(f"  Personalization:  {personalization}/10")
        print(f"  Actionability:    {actionability}/10")
        print(f"  Completeness:     {completeness}/10")
        print(f"  OVERALL:          {overall_score:.1f}/10")
        print(f"  Generation Time:  {generation_time:.2f}s")
    
    # Summary
    print("\n\n" + "="*70)
    print("EVALUATION SUMMARY")
    print("="*70)
    
    if results:
        avg_overall = sum(r['overall'] for r in results) / len(results)
        avg_time = sum(r['generation_time'] for r in results) / len(results)
        
        print(f"\nAverage Overall Score: {avg_overall:.1f}/10")
        print(f"Average Generation Time: {avg_time:.2f}s")
        print(f"\nAll {len(results)} evaluations tracked in Opik!")
        print("View at: https://www.comet.com/opik")
    
    return results


if __name__ == "__main__":
    results = run_comprehensive_evaluation()
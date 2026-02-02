import os
import time
from planner_agent import create_investment_plan
from advisor_agent import get_investment_advice
# Ensure we can import properly
import sys
sys.path.append(os.getcwd())

def test_planner():
    print("\n" + "="*70)
    print("TESTING PLANNER AGENT (High Density Output)")
    print("="*70)
    
    user_profile = {
        'age': 35,
        'income': 120000,
        'capital': 50000,
        'monthly': 2000,
        'timeline': 20,
        'risk_tolerance': 'High',
        'goal': 'Aggressive Growth',
        'currency_symbol': '$'
    }
    
    print("Generating plan...")
    start = time.time()
    plan = create_investment_plan(user_profile)
    elapsed = time.time() - start
    
    print(f"\nTime taken: {elapsed:.2f}s")
    print("\n--- PLAN OUTPUT START ---")
    print(plan)
    print("--- PLAN OUTPUT END ---\n")
    
    # Validation checks
    if "|" in plan and "Asset class" in plan:
        print("✅ PASSED: Markdown Table found.")
    else:
        print("❌ FAILED: No Markdown Table detected.")
        
    if "Why" in plan or "Rationale" in plan:
        print("✅ PASSED: Logic Pillars found.")
    else:
        print("wARNING: Rationale might be weak.")

def test_advisor():
    print("\n" + "="*70)
    print("TESTING ADVISOR AGENT (Chain of Thought & Fallback)")
    print("="*70)
    
    context = {
        'age': 35,
        'risk_tolerance': 'High',
        'portfolio_value': '$50,000'
    }
    
    # Test a generic question that forces fallback (since it's not in expert dict)
    # And we assume API might fail or we want to verify fallback quality regardless.
    fallback_q = "How should I allocate $5000?"
    
    start = time.time()
    ans = get_investment_advice(fallback_q, context)
    elapsed = time.time() - start
    
    print(f"\nQ: {fallback_q}")
    print(f"A ({elapsed:.2f}s):\n{ans}\n")
    
    # Validation
    if "| Asset Class |" in ans:
         print("✅ PASSED: Markdown Table found in fallback.")
    else:
         print("❌ FAILED: No Table in fallback.")

if __name__ == "__main__":
    try:
        from dotenv import load_dotenv
        load_dotenv()
    except ImportError:
        pass
    
    test_advisor()
    test_planner()

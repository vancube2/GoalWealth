from opik import track
import time
from evaluate_advisor import TEST_QUESTIONS, evaluate_advisor_response

@track(project_name="goalwealth-experiments", tags=["advisor-v2", "enhanced"])
def get_investment_advice_v2(question, user_context=None):
    """
    Enhanced advisor - FIXED VERSION
    """
    from google import genai
    import os
    from dotenv import load_dotenv
    
    load_dotenv()
    
    gemini_key = os.getenv("GEMINI_API_KEY")
    client = genai.Client(api_key=gemini_key)
    
    context_str = ""
    if user_context:
        context_str = f"""
USER PROFILE (PERSONALIZE YOUR RESPONSE):
- Age: {user_context.get('age')} years old
- Risk Tolerance: {user_context.get('risk_tolerance')}
- Portfolio Value: {user_context.get('portfolio_value')}
- Investment Timeline: {user_context.get('timeline')} years

Use this information to personalize your advice!
"""
    
    prompt = f"""
You are an expert investment advisor specializing in traditional markets, cryptocurrency, and Solana DeFi protocols.

{context_str}

USER QUESTION: {question}

Provide a helpful, actionable answer that:
1. Answers their question directly in the first sentence
2. Includes specific numbers, percentages, or APY rates
3. Mentions relevant Solana DeFi opportunities (Jito 8-9% APY, Raydium 20-25%, Kamino 25-35%)
4. Lists at least 2 specific risks
5. Provides 2-3 actionable next steps
6. If asked about Arcium: Clarify it's a privacy SDK/tool, NOT an investment

Keep response 150-300 words. Be specific and actionable.
"""
    
    try:
        # Use gemini-1.5-flash instead - it's more stable
        response = client.models.generate_content(
            model='gemini-1.5-flash',
            contents=prompt
        )
        return response.text
    except Exception as e:
        print(f"Error: {e}")
        return f"Error generating response: {str(e)}"


# Wait 60 seconds before running to avoid quota issues
def run_advisor_experiments_delayed():
    """
    Run experiments with delay to avoid quota
    """
    import time
    
    print("\n" + "="*70)
    print("ADVISOR OPTIMIZATION - WAITING 60s FOR QUOTA RESET")
    print("="*70)
    
    for i in range(60, 0, -10):
        print(f"Waiting {i} seconds...")
        time.sleep(10)
    
    print("\nStarting experiments...")
    
    user_context = {
        'age': 30,
        'risk_tolerance': 'High',
        'portfolio_value': '$15,000',
        'timeline': 30
    }
    
    results_v2 = []
    
    for test in TEST_QUESTIONS:
        print(f"\nQuestion: {test['question']}")
        
        start = time.time()
        answer = get_investment_advice_v2(test['question'], user_context)
        elapsed = time.time() - start
        
        if "Error" in answer:
            print(f"Skipping due to error")
            continue
            
        score = evaluate_advisor_response(test['question'], answer, test['expected_qualities'])
        
        results_v2.append({
            'score': score,
            'time': elapsed
        })
        
        print(f"Score: {score}/10 ({elapsed:.1f}s)")
        
        # Wait between requests
        time.sleep(5)
    
    if results_v2:
        avg_v2 = sum(r['score'] for r in results_v2) / len(results_v2)
        avg_time_v2 = sum(r['time'] for r in results_v2) / len(results_v2)
        
        print("\n" + "="*70)
        print("RESULTS")
        print("="*70)
        print(f"Baseline: 7.5/10")
        print(f"Enhanced: {avg_v2:.1f}/10")
        print(f"Improvement: {avg_v2 - 7.5:+.1f}")
    
    return results_v2


if __name__ == "__main__":
    run_advisor_experiments_delayed()
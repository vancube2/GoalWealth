from advisor_agent import get_investment_advice
from opik import track
import time

# Test questions for evaluation
TEST_QUESTIONS = [
    {
        'question': 'Should I buy Bitcoin or Solana right now?',
        'expected_qualities': ['market_analysis', 'comparison', 'risk_mention', 'specific_recommendation']
    },
    {
        'question': 'How does Jito staking work?',
        'expected_qualities': ['technical_explanation', 'apr_mention', 'risk_warning', 'actionable_steps']
    },
    {
        'question': 'What are the risks of DeFi?',
        'expected_qualities': ['comprehensive_risks', 'specific_examples', 'mitigation_strategies']
    },
    {
        'question': 'Is Arcium a good investment?',
        'expected_qualities': ['clarifies_not_investment', 'explains_sdk', 'correct_info']
    }
]

@track(project_name="goalwealth-advisor-eval", tags=["evaluation"])
def evaluate_advisor_response(question, answer, expected_qualities):
    """
    Evaluate advisor response quality
    """
    score = 0
    
    # Length check (not too short, not too long)
    word_count = len(answer.split())
    if 100 < word_count < 400:
        score += 2
    elif word_count >= 50:
        score += 1
    
    # Specificity (mentions numbers, percentages, names)
    if any(char.isdigit() for char in answer):
        score += 2
    
    # Risk awareness
    risk_words = ['risk', 'caution', 'careful', 'warning', 'volatile']
    if any(word in answer.lower() for word in risk_words):
        score += 2
    
    # Actionability
    action_words = ['should', 'can', 'consider', 'recommend', 'try', 'start']
    action_count = sum(1 for word in action_words if word in answer.lower())
    if action_count >= 2:
        score += 2
    
    # Correctness check for Arcium question
    if 'Arcium' in question:
        if 'tool' in answer or 'SDK' in answer or 'privacy' in answer:
            score += 2
    
    return min(score, 10)


def run_advisor_evaluation():
    """
    Evaluate advisor baseline
    """
    print("\n" + "="*70)
    print("ADVISOR EVALUATION - BASELINE")
    print("="*70)
    
    results = []
    user_context = {
        'age': 30,
        'risk_tolerance': 'High',
        'portfolio_value': '$15,000',
        'timeline': 30
    }
    
    for test in TEST_QUESTIONS:
        print(f"\nQuestion: {test['question']}")
        
        start = time.time()
        answer = get_investment_advice(test['question'], user_context)
        elapsed = time.time() - start
        
        score = evaluate_advisor_response(test['question'], answer, test['expected_qualities'])
        
        results.append({
            'question': test['question'],
            'score': score,
            'time': elapsed
        })
        
        print(f"Score: {score}/10 ({elapsed:.1f}s)")
        print(f"Answer preview: {answer[:150]}...")
    
    avg_score = sum(r['score'] for r in results) / len(results)
    avg_time = sum(r['time'] for r in results) / len(results)
    
    print("\n" + "="*70)
    print(f"Advisor Baseline: {avg_score:.1f}/10 ({avg_time:.1f}s)")
    print("="*70)
    
    return avg_score, results


if __name__ == "__main__":
    baseline_score, results = run_advisor_evaluation()
    
    print(f"\nAdvisor Quality: {baseline_score:.1f}/10")
    print("\nAll evaluations tracked in Opik!")
    print("Next: Run optimization experiments to improve this score")
from advisor_experiments import get_investment_advice_v2

user_context = {
    'age': 30,
    'risk_tolerance': 'High',
    'portfolio_value': '$15,000',
    'timeline': 30
}

question = "Should I buy Bitcoin or Solana right now?"

print("Testing Enhanced Advisor V2...")
print("="*70)
print(f"Question: {question}\n")

answer = get_investment_advice_v2(question, user_context)

print(f"Answer:\n{answer}")
print("\n" + "="*70)
print(f"Length: {len(answer)} characters")
print(f"Word count: {len(answer.split())} words")
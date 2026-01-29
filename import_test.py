try:
    import evaluate_advisor
    print("Import successful")
    print(f"Has TEST_QUESTIONS: {hasattr(evaluate_advisor, 'TEST_QUESTIONS')}")
    print(f"Has evaluate_advisor_response: {hasattr(evaluate_advisor, 'evaluate_advisor_response')}")
except Exception as e:
    print(f"Import failed: {e}")
    import traceback
    traceback.print_exc()

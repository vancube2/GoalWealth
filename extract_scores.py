try:
    with open(r'c:\Users\DELL\Documents\GoalWealth\scores_output.txt', 'r', encoding='utf-16') as f:
        print("--- EXTRACTED SCORES ---")
        for line in f:
            if "Score:" in line or "Advisor" in line or "Baseline" in line or "Quality" in line:
                print(line.strip())
        print("--- END ---")
except Exception as e:
    print(f"Error reading utf-16: {e}")
    try:
        with open(r'c:\Users\DELL\Documents\GoalWealth\scores_output.txt', 'r', encoding='utf-8') as f:
             print("--- EXTRACTED SCORES (UTF-8) ---")
             for line in f:
                if "Score:" in line or "Advisor" in line or "Baseline" in line or "Quality" in line:
                    print(line.strip())
    except Exception as e2:
        print(f"Error reading utf-8: {e2}")

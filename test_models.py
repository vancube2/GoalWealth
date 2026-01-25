import google.generativeai as genai
import os
from pathlib import Path
import sys

# Force UTF-8 for stdout
sys.stdout.reconfigure(encoding='utf-8')

gemini_key = None
# Manual env parsing
try:
    candidates = [
        Path(__file__).parent / '.env',
        Path(os.getcwd()) / '.env',
        Path('C:/Users/DELL/Documents/GoalWealth/.env')
    ]
    for env_path in candidates:
        if env_path.exists():
            try:
                with open(env_path, 'r', encoding='utf-8-sig', errors='ignore') as f:
                    for line in f:
                        line = line.strip()
                        if line.startswith('GEMINI_API_KEY='):
                            gemini_key = line.split('=', 1)[1].strip()
                            break
            except: pass
        if gemini_key: break
except: pass

if not gemini_key:
    print("NO_KEY")
    exit(1)

genai.configure(api_key=gemini_key)

models_to_test = [
    "gemini-3-flash-preview",
    "gemini-2.0-flash-exp",
    "gemini-1.5-flash",
    "gemini-1.5-flash-latest",
    "gemini-1.5-flash-002"
]

print("START_TEST")
for m in models_to_test:
    try:
        model = genai.GenerativeModel(m)
        response = model.generate_content("Hello")
        print(f"SUCCESS: {m}")
    except Exception as e:
        print(f"FAIL: {m} - {e}")
print("END_TEST")

import google.generativeai as genai
import os
from pathlib import Path

def get_key():
    candidates = [
        Path('c:/Users/DELL/Documents/GoalWealth/.env'),
        Path('.env')
    ]
    for c in candidates:
        if c.exists():
            with open(c, 'r') as f:
                for line in f:
                    if line.startswith('GEMINI_API_KEY='):
                        return line.split('=')[1].strip()
    return os.environ.get('GEMINI_API_KEY')

key = get_key()
if not key:
    print("NO_KEY")
    exit(1)

genai.configure(api_key=key)
print("Available models:")
for m in genai.list_models():
    if 'generateContent' in m.supported_generation_methods:
        print(f"- {m.name}")

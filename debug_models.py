import google.generativeai as genai
import os
from pathlib import Path

# Robust env loading
gemini_key = None
try:
    candidates = [
        Path(__file__).parent / '.env',
        Path(os.getcwd()) / '.env',
        Path('C:/Users/DELL/Documents/GoalWealth/.env')
    ]
    for env_path in candidates:
        if env_path.exists():
            with open(env_path, 'r', encoding='utf-8-sig', errors='ignore') as f:
                for line in f:
                    line = line.strip()
                    if line.startswith('GEMINI_API_KEY='):
                        gemini_key = line.split('=', 1)[1].strip()
                        break
        if gemini_key: break
except: pass

if not gemini_key:
    print("ERROR: API key not found.")
    exit(1)

genai.configure(api_key=gemini_key)

print(f"Checking models for API Key (starts with {gemini_key[:5]}...):")
print("-" * 50)

try:
    for m in genai.list_models():
        if 'generateContent' in m.supported_generation_methods:
            print(f"Name: {m.name}")
            print(f"Display Name: {m.display_name}")
            print(f"Description: {m.description}")
            print("-" * 30)
except Exception as e:
    print(f"Error listing models: {e}")

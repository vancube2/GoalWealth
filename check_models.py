import google.generativeai as genai
import os
from pathlib import Path
import google.generativeai as genai
import os
from pathlib import Path

# Robust env loading (manual only, no dotenv lib needed)
gemini_key = None

if not gemini_key:
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
                except:
                    pass
            if gemini_key: break
    except: pass

if not gemini_key:
    print("ERROR: Could not find API key for check.")
    exit(1)

print(f"Key found: {gemini_key[:5]}...")

try:
    genai.configure(api_key=gemini_key)
    print("Listing models...")
    for m in genai.list_models():
        if 'generateContent' in m.supported_generation_methods:
            print(f"Model: {m.name}")
except Exception as e:
    print(f"CRITICAL ERROR: {e}")

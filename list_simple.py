import google.generativeai as genai
import os
from pathlib import Path
import sys

# Force UTF-8 for stdout
sys.stdout.reconfigure(encoding='utf-8')

gemini_key = None
# Manual env parsing (proven to work)
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
    # Try one last fallback - hardcode from what we saw earlier if needed, but better to fail
    print("NO_KEY")
    exit(1)

genai.configure(api_key=gemini_key)

print("START_LIST")
try:
    for m in genai.list_models():
        if 'generateContent' in m.supported_generation_methods:
            print(m.name)
except Exception as e:
    print(f"ERROR: {e}")
print("END_LIST")

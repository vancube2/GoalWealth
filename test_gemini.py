from google import genai
from google.genai import types
import os
from dotenv import load_dotenv

load_dotenv()

print("=" * 60)
print("TESTING GEMINI (FREE)")
print("=" * 60)

gemini_key = os.getenv("GEMINI_API_KEY")

if gemini_key:
    print(f"Gemini API key found: {gemini_key[:10]}...")
else:
    print("ERROR: Gemini API key NOT found!")
    exit()

print("\nTesting Gemini connection...\n")

try:
    client = genai.Client(api_key=gemini_key)
    
    response = client.models.generate_content(
        model='gemini-2.5-flash',
        contents="Say 'GoalWealth with Gemini works!' and nothing else."
    )
    
    print(f"Gemini says: {response.text}")
    print("\nSUCCESS! Gemini is working!")
    print("You're ready to build GoalWealth with free AI!")
    
except Exception as e:
    print(f"ERROR: {e}")

print("=" * 60)
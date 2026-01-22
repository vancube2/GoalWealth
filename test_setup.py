import anthropic
import os
from dotenv import load_dotenv

load_dotenv()

print("=" * 60)
print("GOALWEALTH SETUP TEST")
print("=" * 60)

import sys
print(f"\nPython version: {sys.version.split()[0]}")

anthropic_key = os.getenv("ANTHROPIC_API_KEY")
opik_key = os.getenv("OPIK_API_KEY")
workspace = os.getenv("OPIK_WORKSPACE")

if anthropic_key:
    print(f"Anthropic API key: {anthropic_key[:20]}...")
else:
    print("ERROR: Anthropic API key NOT found!")

if opik_key and workspace:
    print(f"Opik workspace: {workspace}")
else:
    print("ERROR: Opik credentials NOT found!")

print("\n" + "=" * 60)
print("Testing Claude API connection...")
print("=" * 60)

try:
    client = anthropic.Anthropic(api_key=anthropic_key)
    
    response = client.messages.create(
        model="claude-sonnet-4-20250514",
        max_tokens=100,
        messages=[{
            "role": "user",
            "content": "Say 'GoalWealth setup successful!' and nothing else."
        }]
    )
    
    print(f"\nClaude says: {response.content[0].text}")
    print("\nSUCCESS! Everything is working perfectly!")
    print("\nYou are ready to build GoalWealth!")
    
except Exception as e:
    print(f"\nERROR: {e}")

print("\n" + "=" * 60)
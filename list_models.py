from google import genai
import os
from dotenv import load_dotenv

load_dotenv()

gemini_key = os.getenv("GEMINI_API_KEY")

try:
    client = genai.Client(api_key=gemini_key)
    
    print("Available Gemini models:")
    print("=" * 60)
    
    models = client.models.list()
    
    for model in models:
        print(f"- {model.name}")
    
except Exception as e:
    print(f"ERROR: {e}")
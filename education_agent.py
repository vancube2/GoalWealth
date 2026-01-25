import google.generativeai as genai
import os
from dotenv import load_dotenv
from opik import track

from pathlib import Path
import time

# Robust env loading (manual only, no dotenv lib needed)
gemini_key = None
try:
    candidates = [
        Path(__file__).parent / '.env',
        Path(os.getcwd()) / '.env',
        Path('C:/Users/DELL/Documents/GoalWealth/.env')
    ]
    for env_path in candidates:
        if env_path.exists():
            try:
                # encoding='utf-8-sig' handles BOM if present
                with open(env_path, 'r', encoding='utf-8-sig', errors='ignore') as f:
                    content = f.read()
                    for line in content.splitlines():
                        line = line.strip()
                        if line.startswith('GEMINI_API_KEY='):
                            gemini_key = line.split('=', 1)[1].strip()
                            break
            except: pass
        if gemini_key: break
except: pass

@track(project_name="goalwealth", tags=["education"])
def generate_guide(topic, user_level="beginner"):
    """
    Generate educational guides on investment topics
    """
    if not gemini_key:
        return "Error: API Key not found. Please check .env file."
        
    try:
        # Construct Prompt
        prompt = f"""
        You are an expert crypto educator. Write a clear, concise guide on "{topic}" for a {user_level} level investor.
        
        Structure:
        1. **What is it?** (Simple definition)
        2. **How it works** (Step-by-step)
        3. **Risks & Rewards** (Bullet points)
        4. **Actionable Steps** (How to start)
        
        Keep it under 500 words. Use Markdown formatting.
        """
        
        # Helper for generation with retry
        def generate_with_retry(model_name, prompt):
            genai.configure(api_key=gemini_key)
            model = genai.GenerativeModel(model_name)
            max_retries = 3
            for attempt in range(max_retries):
                try:
                    return model.generate_content(prompt)
                except Exception as e:
                    # Retry on Rate Limit (429) or Server Error (500+)
                    if ("429" in str(e) or "403" in str(e) or "500" in str(e)) and attempt < max_retries - 1:
                        wait_time = 5 * (attempt + 1)
                        print(f"[{model_name}] Rate limit/Error hit. Retrying in {wait_time}s...")
                        time.sleep(wait_time)
                    else:
                        raise e

        # Model Priority List
        models_to_try = ['gemini-3-flash-preview', 'gemini-2.0-flash-exp']
        
        response = None
        last_error = None
        
        for model_name in models_to_try:
            try:
                response = generate_with_retry(model_name, prompt)
                if response:
                    break
            except Exception as e:
                 last_error = e
        
        if not response:
             return f"Error: All models failed. Last error: {last_error}"
             
        return response.text

    except Exception as e:
        return f"Guide generation unavailable ({str(e)}). Please check API key."


# Pre-generate some guides for the app
AVAILABLE_GUIDES = {
    "Jito Staking": "jito-staking",
    "Raydium Liquidity Pools": "raydium-liquidity", 
    "Kamino Vaults": "kamino-vaults",
    "Dollar-Cost Averaging": "dca",
    "Impermanent Loss": "impermanent-loss",
    "Risk Management": "risk-management",
    "Portfolio Rebalancing": "rebalancing"
}


if __name__ == "__main__":
    # Test
    print("Generating sample guide...")
    guide = generate_guide("Jito Staking", "beginner")
    print(guide)
from google import genai
import os
from dotenv import load_dotenv
from opik import track

load_dotenv()

@track(project_name="goalwealth", tags=["education"])
def generate_guide(topic, user_level="beginner"):
    """
    Generate educational guides on investment topics
    
    Topics: 
    - Jito staking
    - Raydium liquidity
    - Impermanent loss
    - Dollar-cost averaging
    - Risk management
    """
    
    gemini_key = os.getenv("GEMINI_API_KEY")
    client = genai.Client(api_key=gemini_key)
    
    prompt = f"""
Create a comprehensive but concise educational guide on: {topic}

Target audience: {user_level} investors

Structure your guide with:

1. WHAT IS IT? (2-3 sentences explaining the concept)

2. WHY IT MATTERS (2-3 sentences on relevance to investing)

3. HOW IT WORKS (3-5 bullet points with specific details)

4. KEY NUMBERS TO KNOW (specific percentages, APYs, risks)

5. GETTING STARTED (3-4 actionable steps)

6. COMMON MISTAKES (2-3 pitfalls to avoid)

7. RESOURCES (specific websites or protocols to use)

Keep total length under 400 words. Use simple language. Include specific numbers.
"""
    
    try:
        response = client.models.generate_content(
            model='gemini-2.5-flash',
            contents=prompt
        )
        return response.text
    except:
        return f"Guide on {topic} temporarily unavailable. Please try again."


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
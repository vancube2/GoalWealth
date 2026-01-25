import os
import google.generativeai as genai
from pathlib import Path
import time
import json

# Robust env loading
gemini_key = os.environ.get('GEMINI_API_KEY')
if not gemini_key:
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

def get_gemini_response(prompt, audio_data=None):
    """Generic helper for Gemini calls with optional audio"""
    if not gemini_key:
        print("Missing Gemini API Key")
        return "ERROR: Missing API Key. Please ensure GEMINI_API_KEY is set in .env"
        
    try:
        genai.configure(api_key=gemini_key)
        # Using a more stable model name
        model = genai.GenerativeModel("gemini-1.5-flash-latest")
        
        content = [prompt]
        if audio_data:
            content.append({
                "mime_type": "audio/wav", 
                "data": audio_data
            })
            
        response = model.generate_content(content)
        return response.text
    except Exception as e:
        error_msg = str(e)
        print(f"Gemini Error: {error_msg}")
        return f"ERROR: {error_msg}"

def transcribe_voice(audio_bytes):
    """Simple transcription of audio bytes"""
    prompt = "Transcribe this audio exactly as spoken. Return only the text."
    return get_gemini_response(prompt, audio_bytes)

def extract_profile_from_voice(audio_bytes):
    """Extracts financial profile data from audio"""
    prompt = """
    Analyze this audio for financial profile information. 
    Extract the following fields in JSON format:
    - age (integer)
    - income (integer)
    - capital (integer)
    - monthly (integer)
    - timeline (integer)
    - risk_tolerance (one of: Low, Medium, High)
    - goal (string)
    
    Only return a raw valid JSON object. No Markdown.
    """
    response_text = get_gemini_response(prompt, audio_bytes)
    if not response_text or response_text.startswith("ERROR:"):
        return {"error": "Voice recognition failed. Please try again."}
        
    try:
        # Clean up Markdown formatting if present
        clean_json = response_text.strip()
        if '```json' in clean_json:
            clean_json = clean_json.split('```json')[1].split('```')[0].strip()
        elif '```' in clean_json:
            clean_json = clean_json.split('```')[1].split('```')[0].strip()
            
        data = json.loads(clean_json)
        # Ensure it's a dict
        if not isinstance(data, dict):
            return {"error": "Invalid response format. Please try again."}
        return data
    except Exception as e:
        return {"error": "Could not understand audio. Please speak clearly."}

def process_voice_advisor_query(audio_bytes, user_context=None):
    """Processes a voice query for the advisor agent"""
    # First transcribe
    question = transcribe_voice(audio_bytes)
    if not question or len(question.strip()) < 2:
        return "Sorry, I couldn't understand the audio. Please try again."
        
    from advisor_agent import get_investment_advice
    return get_investment_advice(question, user_context or {})

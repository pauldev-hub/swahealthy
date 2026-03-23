import os
from dotenv import load_dotenv
import google.generativeai as genai

load_dotenv()
api_key = os.environ.get('GEMINI_API_KEY')

if not api_key:
    print("GEMINI_API_KEY not found in .env")
else:
    genai.configure(api_key=api_key)
    print(f"Checking models for key: {api_key[:10]}...")
    try:
        models = [m.name for m in genai.list_models() if 'generateContent' in m.supported_generation_methods]
        print("Available Gemini models:")
        for m in models:
            if 'gemini' in m.lower():
                print(f"  - {m}")
        
    except Exception as e:
        print(f"Error listing models: {e}")

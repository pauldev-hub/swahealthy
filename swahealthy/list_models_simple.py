import os
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()
genai.configure(api_key=os.environ.get('GEMINI_API_KEY'))

try:
    print("Listing all models available for this API key:")
    for m in genai.list_models():
        print(f" - {m.name}")
except Exception as e:
    print(f"FAILED: {e}")

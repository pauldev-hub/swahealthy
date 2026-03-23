import json
import os
import time
import random
from flask import current_app

def analyze_photo(base64_data, media_type):
    """
    Analyzes an uploaded symptom photo using the Groq API (Llama 3.2 Vision or requested Llama 4).
    Returns a dictionary with observed, possible_conditions, urgency, and recommendation.
    """
    # Use key from config, fallback to environment variable
    api_key = current_app.config.get('GROQ_API_KEY')
    if not api_key:
        api_key = os.environ.get('GROQ_API_KEY')
    
    if not api_key or api_key == 'your_groq_api_key_here':
        return {
            "error": "GROQ_API_KEY is not configured.",
            "observed": "API key is missing. Please set GROQ_API_KEY in your .env file.",
            "possible_conditions": [],
            "urgency": "low",
            "recommendation": "Configure your Groq API key to use this feature."
        }

    if not base64_data:
        return {
            "error": "Invalid image data.",
            "observed": "No image data was provided.",
            "possible_conditions": [],
            "urgency": "low",
            "recommendation": "Upload a clear image and try again."
        }

    try:
        from groq import Groq
        client = Groq(api_key=api_key)

        # Use the specific model requested by the user or default to Llama 3.2 Vision
        model_name = os.environ.get('GROQ_MODEL', 'meta-llama/llama-4-scout-17b-16e-instruct')
        
        print(f"DEBUG: Using Groq model: {model_name}")
        print(f"DEBUG: Analyzing photo (Type: {media_type}, Base64 length: {len(base64_data)})")

        system_prompt = """You are a medical triage assistant helping users analyze photos of their physical symptoms (e.g., rashes, swelling, wounds, eye redness).
You must visually analyze the image and return a JSON object with strictly the following keys: observed, possible_conditions, urgency, recommendation.
Rules:
1. Emphasize that you are an AI and this is NOT a definitive diagnosis.
2. If the image is unclear, set observed to \"Image is unclear\", urgency low, and recommend a clearer picture.
3. Respond ONLY with valid JSON.
"""

        max_retries = 5
        delay = 2
        response = None

        for attempt in range(max_retries):
            try:
                # Groq Chat Completion with Vision
                response = client.chat.completions.create(
                    model=model_name,
                    messages=[
                        {
                            "role": "system",
                            "content": system_prompt
                        },
                        {
                            "role": "user",
                            "content": [
                                {
                                    "type": "text",
                                    "text": "Analyze this uploaded symptom image and return only JSON object."
                                },
                                {
                                    "type": "image_url",
                                    "image_url": {
                                        "url": f"data:{media_type};base64,{base64_data}"
                                    }
                                }
                            ]
                        }
                    ],
                    temperature=0.0,
                    max_tokens=1024,
                    response_format={"type": "json_object"}
                )
                break
            except Exception as e:
                err_text = str(e).lower()
                # Check for rate limits or quota issues
                if any(x in err_text for x in ['429', 'rate_limit', 'quota', 'busy']):
                    if attempt < max_retries - 1:
                        sleep_time = delay + random.uniform(0.0, 1.0)
                        print(f"DEBUG: Groq Rate limit detected, retrying in {sleep_time:.2f}s (attempt {attempt+1}/{max_retries})")
                        time.sleep(sleep_time)
                        delay *= 2
                        continue
                    print("DEBUG: Groq Rate limit hit and max retries reached.")
                    return {
                        "error": "Rate limit exceeded.",
                        "observed": "AI backend is currently rate-limited. Please try again in a minute.",
                        "possible_conditions": [],
                        "urgency": "low",
                        "recommendation": "Use the built-in symptom express checker while API calls recover."
                    }
                if any(x in err_text for x in ['api_key', 'unauthenticated', 'permission', '401', '403']):
                    return {
                        "error": "Authentication failed for Groq API key.",
                        "observed": "Please verify GROQ_API_KEY in .env.",
                        "possible_conditions": [],
                        "urgency": "low",
                        "recommendation": "Re-enter a valid Groq API key and restart the app."
                    }
                raise

        if response is None or not response.choices:
            return {
                "error": "Failed to connect to Groq service.",
                "observed": "The AI service did not respond.",
                "possible_conditions": [],
                "urgency": "low",
                "recommendation": "Try again in a moment."
            }

        result_text = response.choices[0].message.content.strip()
        print(f"DEBUG: Groq raw response: {result_text}")

        # Safety: clean up markdown if any, though json_object mode should prevent it
        if "```json" in result_text:
            result_text = result_text.split("```json")[-1].split("```")[0].strip()
        elif "```" in result_text:
            result_text = result_text.split("```")[-1].split("```")[0].strip()

        result = json.loads(result_text)

        # Normalize keys
        required_keys = ["observed", "possible_conditions", "urgency", "recommendation"]
        for key in required_keys:
            if key not in result:
                result[key] = [] if key == 'possible_conditions' else "N/A"

        return result

    except Exception as e:
        import traceback
        print(f"Error analyzing photo via Groq: {traceback.format_exc()}")
        return {
            "error": str(e),
            "observed": "Could not analyze the image due to an error.",
            "possible_conditions": [],
            "urgency": "low",
            "recommendation": "Please rely on the symptom checklist instead."
        }


import json
import os
import time
import random
import requests
from flask import current_app

PHOTO_ANALYSIS_TEXT = {
    "en": {
        "demo_observed": "Demo mode: the external AI provider is unavailable, so this is a sample visual-assessment response for UI testing only.",
        "demo_conditions": ["Dry skin", "Contact irritation", "Eczema"],
        "demo_recommendation": "Demo mode only. The live AI analysis could not run ({reason}). The upload, preview, and results UI are working, but this is not a real medical assessment.",
        "missing_key_observed": "API key is missing. Please set OPENROUTER_API_KEY in your .env file.",
        "missing_key_recommendation": "Get a free OpenRouter API key at https://openrouter.ai/keys",
        "no_image_observed": "No image data was provided.",
        "no_image_recommendation": "Upload a clear image and try again.",
        "rate_limit_observed": "AI backend is currently rate-limited. Please try again in a minute.",
        "rate_limit_recommendation": "Use the built-in symptom express checker while API calls recover.",
        "auth_observed": "Please verify OPENROUTER_API_KEY in .env.",
        "auth_recommendation": "Get a valid key at https://openrouter.ai/keys and restart the app.",
        "service_observed": "The AI service did not respond.",
        "service_recommendation": "Try again in a moment.",
        "instruction_language": "Respond in English.",
        "instruction_unclear": 'If the image is unclear, set observed to "Image is unclear", urgency to "low", and recommend a clearer picture.',
    },
    "bn": {
        "demo_observed": "ডেমো মোড: বাহ্যিক AI পরিষেবা এখন উপলব্ধ নয়, তাই এটি শুধু ইন্টারফেস পরীক্ষার জন্য একটি নমুনা ভিজ্যুয়াল মূল্যায়ন।",
        "demo_conditions": ["শুষ্ক ত্বক", "সংস্পর্শজনিত জ্বালা", "একজিমা"],
        "demo_recommendation": "এটি শুধুই ডেমো মোড। লাইভ AI বিশ্লেষণ চালানো যায়নি ({reason})। আপলোড, প্রিভিউ ও ফলাফলের ইন্টারফেস কাজ করছে, তবে এটি বাস্তব চিকিৎসা মূল্যায়ন নয়।",
        "missing_key_observed": "API key অনুপস্থিত। অনুগ্রহ করে আপনার .env ফাইলে OPENROUTER_API_KEY সেট করুন।",
        "missing_key_recommendation": "https://openrouter.ai/keys থেকে একটি ফ্রি OpenRouter API key নিন",
        "no_image_observed": "কোনো ছবির তথ্য দেওয়া হয়নি।",
        "no_image_recommendation": "একটি পরিষ্কার ছবি আপলোড করে আবার চেষ্টা করুন।",
        "rate_limit_observed": "AI পরিষেবার অনুরোধ সীমায় পৌঁছেছে। অনুগ্রহ করে এক মিনিট পরে আবার চেষ্টা করুন।",
        "rate_limit_recommendation": "এর মধ্যে বিল্ট-ইন symptom checker ব্যবহার করতে পারেন।",
        "auth_observed": "অনুগ্রহ করে .env ফাইলে OPENROUTER_API_KEY ঠিক আছে কিনা যাচাই করুন।",
        "auth_recommendation": "https://openrouter.ai/keys থেকে একটি বৈধ key নিয়ে অ্যাপটি পুনরায় চালু করুন।",
        "service_observed": "AI পরিষেবা সাড়া দেয়নি।",
        "service_recommendation": "কিছুক্ষণ পরে আবার চেষ্টা করুন।",
        "instruction_language": "সমস্ত observed, possible_conditions এবং recommendation বাংলা ভাষায় দিন।",
        "instruction_unclear": 'ছবিটি অস্পষ্ট হলে observed-এ "ছবিটি অস্পষ্ট" লিখুন, urgency "low" দিন, এবং আরও পরিষ্কার ছবি দেওয়ার পরামর্শ দিন।',
    },
    "hi": {
        "demo_observed": "डेमो मोड: बाहरी AI सेवा अभी उपलब्ध नहीं है, इसलिए यह केवल UI परीक्षण के लिए एक नमूना दृश्य विश्लेषण है।",
        "demo_conditions": ["शुष्क त्वचा", "संपर्क से जलन", "एक्जिमा"],
        "demo_recommendation": "यह केवल डेमो मोड है। लाइव AI विश्लेषण नहीं चल सका ({reason})। अपलोड, प्रीव्यू और परिणाम UI काम कर रहे हैं, लेकिन यह वास्तविक चिकित्सीय मूल्यांकन नहीं है।",
        "missing_key_observed": "API key उपलब्ध नहीं है। कृपया अपनी .env फ़ाइल में OPENROUTER_API_KEY सेट करें।",
        "missing_key_recommendation": "https://openrouter.ai/keys से एक मुफ्त OpenRouter API key लें",
        "no_image_observed": "कोई इमेज डेटा प्रदान नहीं किया गया।",
        "no_image_recommendation": "एक साफ़ तस्वीर अपलोड करके फिर कोशिश करें।",
        "rate_limit_observed": "AI सेवा की अनुरोध सीमा पूरी हो गई है। कृपया एक मिनट बाद फिर कोशिश करें।",
        "rate_limit_recommendation": "तब तक बिल्ट-इन symptom checker का उपयोग करें।",
        "auth_observed": "कृपया .env में OPENROUTER_API_KEY की जाँच करें।",
        "auth_recommendation": "https://openrouter.ai/keys से एक वैध key लेकर ऐप को फिर से शुरू करें।",
        "service_observed": "AI सेवा ने जवाब नहीं दिया।",
        "service_recommendation": "थोड़ी देर बाद फिर कोशिश करें।",
        "instruction_language": "observed, possible_conditions और recommendation पूरी तरह हिंदी में दें।",
        "instruction_unclear": 'यदि छवि स्पष्ट नहीं है, तो observed में "छवि स्पष्ट नहीं है" लिखें, urgency "low" रखें, और अधिक साफ़ तस्वीर की सलाह दें।',
    }
}


def _lang_pack(language):
    return PHOTO_ANALYSIS_TEXT.get(language if language in PHOTO_ANALYSIS_TEXT else "en", PHOTO_ANALYSIS_TEXT["en"])


def _demo_analysis(reason, language="en"):
    pack = _lang_pack(language)
    return {
        "observed": pack["demo_observed"],
        "possible_conditions": pack["demo_conditions"],
        "urgency": "low",
        "recommendation": pack["demo_recommendation"].format(reason=reason)
    }

def analyze_photo(base64_data, media_type, language="en"):
    """
    Analyzes an uploaded symptom photo using OpenRouter API.
    Returns a dictionary with observed, possible_conditions, urgency, and recommendation.
    """
    print(f"DEBUG: analyze_photo called")
    print(f"DEBUG: base64_data type: {type(base64_data)}")
    print(f"DEBUG: base64_data length: {len(base64_data) if base64_data else 0}")
    print(f"DEBUG: media_type: {media_type}")
    print(f"DEBUG: language: {language}")
    pack = _lang_pack(language)
    
    # Use key from config, fallback to environment variable
    api_key = current_app.config.get('OPENROUTER_API_KEY')
    if not api_key:
        api_key = os.environ.get('OPENROUTER_API_KEY')
    
    if not api_key or api_key == 'your_openrouter_api_key_here':
        return {
            "error": "OPENROUTER_API_KEY is not configured.",
            "observed": pack["missing_key_observed"],
            "possible_conditions": [],
            "urgency": "low",
            "recommendation": pack["missing_key_recommendation"]
        }

    if not base64_data or (isinstance(base64_data, str) and base64_data.strip() == ''):
        print("DEBUG: base64_data is empty!")
        return {
            "error": "Invalid image data.",
            "observed": pack["no_image_observed"],
            "possible_conditions": [],
            "urgency": "low",
            "recommendation": pack["no_image_recommendation"]
        }
    
    # Clean and validate base64
    base64_data = base64_data.strip()
    print(f"DEBUG: Cleaned base64 length: {len(base64_data)}")

    try:
        print(f"DEBUG: Using OpenRouter free router for vision analysis")
        print(f"DEBUG: Analyzing photo (Type: {media_type}, Base64 length: {len(base64_data)})")

        instruction_prompt = f"""You are a medical triage assistant helping users analyze photos of physical symptoms such as rashes, swelling, wounds, redness, irritation, nail changes, and eye findings.
You must visually analyze the image and return ONLY a valid JSON object with these exact keys: observed, possible_conditions, urgency, recommendation.
Rules:
1. Emphasize in recommendation that you are an AI and this is NOT a definitive diagnosis.
2. {pack["instruction_unclear"]}
3. possible_conditions must be a list of 2 to 5 short strings when something is visible.
4. urgency must be one of: low, moderate, high, very high.
5. {pack["instruction_language"]}
6. Make "observed" detailed: 2 to 4 sentences describing visible color, shape, texture, spread, discharge, swelling, borders, and anything that makes the image unclear.
7. Make "recommendation" more useful: 3 to 5 sentences covering simple care steps, what to monitor over the next 24 to 48 hours, and when to seek in-person care.
8. If you are unsure, say what is visible and state uncertainty clearly instead of pretending confidence.
9. Respond ONLY with the JSON object, no markdown, no explanations."""

        max_retries = 5
        delay = 2
        response = None

        for attempt in range(max_retries):
            try:
                mime_type = media_type or 'image/jpeg'
                
                # OpenRouter API endpoint
                headers = {
                    "Authorization": f"Bearer {api_key}",
                    "HTTP-Referer": "http://localhost:5000",
                    "X-Title": "SwahealthyApp"
                }
                
                image_url = f"data:{mime_type};base64,{base64_data}"

                # OpenRouter chat completions expects images as image_url content.
                payload = {
                    "model": "openrouter/free",
                    "messages": [
                        {
                            "role": "user",
                            "content": [
                                {
                                    "type": "text",
                                    "text": f"{instruction_prompt}\n\nAnalyze this symptom image. Return only JSON."
                                },
                                {
                                    "type": "image_url",
                                    "image_url": {
                                        "url": image_url
                                    }
                                }
                            ]
                        }
                    ],
                    "temperature": 0.0,
                    "max_tokens": 450
                }
                
                # Make API call to OpenRouter
                print(f"DEBUG: Sending to OpenRouter API")
                print(f"DEBUG: Payload has image_url: {'image_url' in str(payload)}")
                print(f"DEBUG: Image URL prefix: {image_url[:32]}")
                
                response = requests.post(
                    "https://openrouter.ai/api/v1/chat/completions",
                    headers=headers,
                    json=payload,
                    timeout=30
                )
                
                if response.status_code == 200:
                    response_data = response.json()
                    result_text = response_data.get('choices', [{}])[0].get('message', {}).get('content', '').strip()
                    
                    if result_text:
                        print(f"DEBUG: AI raw response: {result_text}")
                        
                        # Clean up markdown formatting if present
                        if "```json" in result_text:
                            result_text = result_text.split("```json")[-1].split("```")[0].strip()
                        elif "```" in result_text:
                            result_text = result_text.split("```")[0].strip()
                        
                        result = json.loads(result_text)
                        
                        # Normalize keys
                        required_keys = ["observed", "possible_conditions", "urgency", "recommendation"]
                        for key in required_keys:
                            if key not in result:
                                result[key] = [] if key == 'possible_conditions' else "N/A"
                        
                        return result
                    
                    break
                elif response.status_code == 429:
                    # Rate limit - retry
                    if attempt < max_retries - 1:
                        sleep_time = delay + random.uniform(0.0, 1.0)
                        print(f"DEBUG: Rate limit detected, retrying in {sleep_time:.2f}s (attempt {attempt+1}/{max_retries})")
                        time.sleep(sleep_time)
                        delay *= 2
                        continue
                    else:
                        return {
                            "error": "Rate limit exceeded.",
                            "observed": pack["rate_limit_observed"],
                            "possible_conditions": [],
                            "urgency": "low",
                            "recommendation": pack["rate_limit_recommendation"]
                        }
                elif response.status_code in [401, 403]:
                    return {
                        "error": "Authentication failed for OpenRouter API key.",
                        "observed": pack["auth_observed"],
                        "possible_conditions": [],
                        "urgency": "low",
                        "recommendation": pack["auth_recommendation"]
                    }
                elif response.status_code in [400, 402]:
                    print(f"DEBUG: Falling back to demo analysis for status {response.status_code}")
                    return _demo_analysis(f"OpenRouter returned HTTP {response.status_code}", language=language)
                else:
                    error_msg = response.text
                    print(f"DEBUG: OpenRouter error {response.status_code}: {error_msg}")
                    if attempt < max_retries - 1:
                        time.sleep(delay)
                        delay *= 2
                        continue
                    raise Exception(f"OpenRouter API error {response.status_code}: {error_msg}")
                    
            except requests.exceptions.Timeout:
                if attempt < max_retries - 1:
                    print(f"DEBUG: Request timeout, retrying (attempt {attempt+1}/{max_retries})")
                    time.sleep(delay)
                    delay *= 2
                    continue
                raise Exception("Request timeout - please try again")
            except Exception as e:
                if attempt < max_retries - 1:
                    time.sleep(delay)
                    delay *= 2
                    continue
                raise

        return {
            "error": "Failed to connect to AI service.",
            "observed": pack["service_observed"],
            "possible_conditions": [],
            "urgency": "low",
            "recommendation": pack["service_recommendation"]
        }

    except Exception as e:
        import traceback
        print(f"Error analyzing photo via OpenRouter: {traceback.format_exc()}")
        return _demo_analysis(str(e), language=language)

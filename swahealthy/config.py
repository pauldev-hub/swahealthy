"""
Application configuration.
Loads environment variables from .env and provides a Config class.
"""

import os
from dotenv import load_dotenv

# Resolve project root (directory containing this file)
BASE_DIR = os.path.abspath(os.path.dirname(__file__))

load_dotenv(os.path.join(BASE_DIR, '.env'), override=True)


class Config:
    """Central configuration for the SwaHealthy Flask application."""

    SECRET_KEY = os.environ.get('SECRET_KEY') or 'default-secret-key'
    GEMINI_API_KEY = os.environ.get('GEMINI_API_KEY')
    GROQ_API_KEY = os.environ.get('GROQ_API_KEY')
    OPENROUTER_API_KEY = os.environ.get('OPENROUTER_API_KEY')

    # Google OAuth (Stripping whitespace to prevent invalid_client errors from hidden chars)
    GOOGLE_CLIENT_ID = os.environ.get('GOOGLE_CLIENT_ID', '').strip()
    GOOGLE_CLIENT_SECRET = os.environ.get('GOOGLE_CLIENT_SECRET', '').strip()

    # Allow OAuth over HTTP on localhost (set to '1' in .env for local dev)
    OAUTHLIB_INSECURE_TRANSPORT = os.environ.get('OAUTHLIB_INSECURE_TRANSPORT', '0')

    # Database
    DB_PATH = os.path.join(BASE_DIR, 'data', 'swahealthy.db')

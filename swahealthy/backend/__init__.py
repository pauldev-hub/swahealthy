"""
SwaHealthy Backend — Flask application factory.
"""

import os
import json

from flask import Flask
from authlib.integrations.flask_client import OAuth

from config import Config


# Module-level OAuth instance (accessed by auth routes)
oauth = OAuth()
google = None


def create_app():
    """Create and configure the Flask application."""
    global google

    # Resolve paths relative to the project root (parent of backend/)
    project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
    template_dir = os.path.join(project_root, 'frontend', 'templates')
    static_dir = os.path.join(project_root, 'frontend', 'static')

    app = Flask(
        __name__,
        template_folder=template_dir,
        static_folder=static_dir,
    )

    # Load configuration
    app.config.from_object(Config)

    # Ensure OAUTHLIB allows HTTP on localhost
    os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = Config.OAUTHLIB_INSECURE_TRANSPORT

    # Debug prints (remove in production)
    _cid = Config.GOOGLE_CLIENT_ID
    _csec = Config.GOOGLE_CLIENT_SECRET
    print(f"[DEBUG] GOOGLE_CLIENT_ID loaded: '{_cid[:30]}...' (ends with .apps.googleusercontent.com: {_cid.endswith('.apps.googleusercontent.com')})")
    print(f"[DEBUG] GOOGLE_CLIENT_SECRET loaded: '{_csec[:10]}...' (present: {bool(_csec)})")
    _gkey = Config.GEMINI_API_KEY
    print(f"[DEBUG] GEMINI_API_KEY loaded: '{_gkey[:5]}...' (present: {bool(_gkey)}), (placeholder: {bool(_gkey == 'your_gemini_api_key_here')})")
    _groqkey = Config.GROQ_API_KEY
    print(f"[DEBUG] GROQ_API_KEY loaded: '{_groqkey[:5] if _groqkey else 'None'}...' (present: {bool(_groqkey)})")

    # ----- OAuth -----
    oauth.init_app(app)
    google = oauth.register(
        name='google',
        client_id=_cid,
        client_secret=_csec,
        server_metadata_url='https://accounts.google.com/.well-known/openid-configuration',
        client_kwargs={'scope': 'openid email profile'},
    )

    # ----- Jinja filters -----
    @app.template_filter('from_json')
    def from_json_filter(s):
        return json.loads(s)

    # ----- Register blueprints -----
    from backend.routes.main import main_bp
    from backend.routes.auth import auth_bp
    from backend.routes.appointments import appointments_bp

    app.register_blueprint(main_bp)
    app.register_blueprint(auth_bp)
    app.register_blueprint(appointments_bp)

    # ----- Initialise database -----
    from backend.models.schema import init_db

    # Ensure data/ directory exists
    data_dir = os.path.dirname(Config.DB_PATH)
    os.makedirs(data_dir, exist_ok=True)

    with app.app_context():
        init_db()

    return app

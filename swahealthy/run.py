"""
Entry point for the SwaHealthy application.
Usage: python run.py
"""

import os

from backend import create_app

app = create_app()

if __name__ == '__main__':
    is_render = bool(os.environ.get('RENDER') or os.environ.get('RENDER_EXTERNAL_URL'))
    host = '0.0.0.0' if is_render else 'localhost'
    port = int(os.environ.get('PORT', '5000'))
    app.run(host=host, port=port, debug=False)

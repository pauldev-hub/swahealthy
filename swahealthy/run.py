"""
Entry point for the SwaHealthy application.
Usage: python run.py
"""

from backend import create_app

app = create_app()

if __name__ == '__main__':
    app.run(host='localhost', debug=True)

import os
from dotenv import load_dotenv

# Resolve project root
BASE_DIR = os.path.abspath(os.path.dirname(__file__))
env_path = os.path.join(BASE_DIR, '.env')

print(f"Loading env from: {env_path}")
print(f"File exists: {os.path.exists(env_path)}")

load_dotenv(env_path, override=True)

cid = os.environ.get('GOOGLE_CLIENT_ID')
print(f"GOOGLE_CLIENT_ID: '{cid}'")
print(f"Length: {len(cid) if cid else 0}")
print(f"Ends with correct domain: {cid.endswith('.apps.googleusercontent.com') if cid else False}")

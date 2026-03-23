import re
import os

files_to_clean = [
    r'c:\Users\hp\OneDrive\Desktop\Health app\swahealthy\frontend\templates\appointments\appointments.html',
    r'c:\Users\hp\OneDrive\Desktop\Health app\swahealthy\frontend\templates\pages\duration.html'
]

for filepath in files_to_clean:
    if os.path.exists(filepath):
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Remove anything between <style> and </style>
        new_content = re.sub(r'<style>.*?</style>', '', content, flags=re.DOTALL)
        
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(new_content)
        print(f"Cleaned {filepath}")
    else:
        print(f"Not found {filepath}")

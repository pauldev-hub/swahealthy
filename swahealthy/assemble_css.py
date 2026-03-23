import re
import os

def extract_css(filepath):
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
            match = re.search(r'```css(.*?)```', content, re.DOTALL)
            if match:
                return match.group(1).strip()
            return ""
    except Exception as e:
        print(f"Error reading {filepath}: {e}")
        return ""

file_order = [
    'ui_redesign/style_css.md',
    'ui_redesign/swahealthy_additions_css.md',
    'ui_redesign/missing_pages_css.md',
    'ui_redesign/bottom_nav_css.md',
    'ui_redesign/gaps_css.md'
]

combined_css = []
for file in file_order:
    css = extract_css(file)
    if css:
        combined_css.append(f"/* === From {os.path.basename(file)} === */\n" + css)

with open('frontend/static/css/style.css', 'w', encoding='utf-8') as out:
    out.write("\n\n".join(combined_css))

print("Successfully written style.css")

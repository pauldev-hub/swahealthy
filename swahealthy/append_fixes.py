import re

fix_md_path = r'c:\Users\hp\OneDrive\Desktop\Health app\swahealthy\ui_redesign\ui_fixes_v1.md'
style_css_path = r'c:\Users\hp\OneDrive\Desktop\Health app\swahealthy\frontend\static\css\style.css'

with open(fix_md_path, 'r', encoding='utf-8') as f:
    content = f.read()

match = re.search(r'```css(.*?)```', content, re.DOTALL)
if match:
    css_content = match.group(1).strip()
    
    with open(style_css_path, 'a', encoding='utf-8') as out:
        out.write('\n\n/* === From ui_fixes_v1.md === */\n')
        out.write(css_content)
    print("Appended UI Fixes CSS to style.css successfully.")
else:
    print("Could not find CSS block in markdown.")

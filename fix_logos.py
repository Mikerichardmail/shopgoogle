import os
import re

dir_path = r'f:\online shoping apps new\app\src\main\java\com\onlineshoppingapps'
for filename in os.listdir(dir_path):
    if not filename.endswith('.kt'): continue
    file_path = os.path.join(dir_path, filename)
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    new_content = re.sub(r'https://logo\.clearbit\.com/([^"\'\s\\]+)', r'https://www.google.com/s2/favicons?domain=\1&sz=128', content)
    
    if new_content != content:
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(new_content)
        print(f'Updated {filename}')

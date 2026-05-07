import re
import os
import urllib.request

main_activity_path = r'f:\online shoping apps new\app\src\main\java\com\onlineshoppingapps\MainActivity.kt'
drawable_dir = r'f:\online shoping apps new\app\src\main\res\drawable-nodpi'
os.makedirs(drawable_dir, exist_ok=True)

with open(main_activity_path, 'r', encoding='utf-8') as f:
    content = f.read()

# Store("amazon", "Amazon", "...", listOf(...), "https://www.google.com/s2/favicons?domain=amazon.in&sz=128", ...)
# Or other URLs
matches = re.finditer(r'Store\s*\(\s*"([^"]+)"\s*,\s*"[^"]+"\s*,\s*"[^"]+"\s*,\s*listOf[^,]+,\s*"([^"]+)"', content)

count = 0
for m in matches:
    store_id = m.group(1)
    url = m.group(2)
    
    if not url.startswith('http'):
        continue
        
    out_path = os.path.join(drawable_dir, f'ic_new_{store_id}.png')
    
    if os.path.exists(out_path):
        continue
        
    try:
        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        with urllib.request.urlopen(req) as response:
            data = response.read()
            if len(data) > 0:
                with open(out_path, 'wb') as f:
                    f.write(data)
                print(f'Downloaded logo for {store_id}')
                count += 1
    except Exception as e:
        print(f'Failed to download {store_id}: {e}')

print(f'Done! Downloaded {count} new logos.')

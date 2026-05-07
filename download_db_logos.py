import json
import os
import urllib.request

SUPABASE_URL = "https://fwhzasbjexillgfrvksx.supabase.co/rest/v1/stores?select=id,domain&active=eq.true"
SUPABASE_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImZ3aHphc2JqZXhpbGxnZnJ2a3N4Iiwicm9sZSI6ImFub24iLCJpYXQiOjE3NzY0Mzk5NzksImV4cCI6MjA5MjAxNTk3OX0.MfZPPcx4d7OkAo56emiRjF9FabceUweCVJqv48tXAv4"

drawable_dir = r'f:\online shoping apps new\app\src\main\res\drawable-nodpi'
os.makedirs(drawable_dir, exist_ok=True)

try:
    req = urllib.request.Request(SUPABASE_URL)
    req.add_header('apikey', SUPABASE_KEY)
    req.add_header('Authorization', f'Bearer {SUPABASE_KEY}')
    with urllib.request.urlopen(req) as response:
        stores = json.loads(response.read())
        
    count = 0
    for store in stores:
        store_id = store.get('id', '')
        domain = store.get('domain', '')
        if not store_id or not domain:
            continue
            
        safe_id = store_id.replace('-', '_')
        out_path = os.path.join(drawable_dir, f'ic_new_{safe_id}.png')
        
        if os.path.exists(out_path):
            continue
            
        url = f'https://www.google.com/s2/favicons?domain={domain}&sz=128'
        try:
            img_req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
            with urllib.request.urlopen(img_req) as img_resp:
                data = img_resp.read()
                if len(data) > 0:
                    with open(out_path, 'wb') as f:
                        f.write(data)
                    print(f'Downloaded db logo for {domain} (ID: {safe_id})')
                    count += 1
        except Exception as e:
            print(f'Failed to download {domain}: {e}')

    print(f'Done! Downloaded {count} new database logos.')

except Exception as e:
    print(f'Database fetch error: {e}')

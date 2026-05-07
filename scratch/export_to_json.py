
import requests
import json
import os
import re

SUPABASE_URL = "https://fwhzasbjexillgfrvksx.supabase.co/rest/v1"
SUPABASE_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImZ3aHphc2JqZXhpbGxnZnJ2a3N4Iiwicm9sZSI6ImFub24iLCJpYXQiOjE3NzY0Mzk5NzksImV4cCI6MjA5MjAxNTk3OX0.MfZPPcx4d7OkAo56emiRjF9FabceUweCVJqv48tXAv4"

headers = {
    "apikey": SUPABASE_KEY,
    "Authorization": f"Bearer {SUPABASE_KEY}"
}

def slugify(text):
    return re.sub(r'[^a-z0-9_]', '', text.lower().replace(' ', '_').replace('-', '_').replace('&', 'and'))

def fetch_data():
    print("Fetching stores...")
    stores_resp = requests.get(f"{SUPABASE_URL}/stores?select=id,name,domain,category,logo_url,affiliate_link,affiliate_url&active=eq.true", headers=headers)
    if stores_resp.status_code != 200:
        print(f"Error: {stores_resp.text}")
        return
    stores = stores_resp.json()
    
    print("Fetching coupons...")
    coupons_resp = requests.get(f"{SUPABASE_URL}/coupons?select=code,title,description,success_score,store_id&status=eq.active", headers=headers)
    coupons = coupons_resp.json() if coupons_resp.status_code == 200 else []
    
    store_coupons = {}
    for c in coupons:
        sid = c.get('store_id')
        if sid not in store_coupons: store_coupons[sid] = []
        store_coupons[sid].append(c)
    
    final_data = []
    for s in stores:
        sid = s['id']
        s['slug'] = slugify(s['name'])
        s['coupons'] = store_coupons.get(sid, [])
        s['final_link'] = s.get('affiliate_link') or s.get('affiliate_url') or f"https://{s['domain']}"
        # Extract categories as list
        cat_str = s.get('category') or 'Shopping'
        s['category_list'] = [c.strip() for c in cat_str.split(',')]
        final_data.append(s)
        
    output_path = "f:/online shoping apps new/app/src/main/assets/stores_data.json"
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(final_data, f, indent=4)
        
    print(f"Successfully generated {output_path} with {len(final_data)} stores.")

if __name__ == "__main__":
    fetch_data()

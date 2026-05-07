
import requests
import json
import os
import re

# Credentials
SUPABASE_URL = "https://fwhzasbjexillgfrvksx.supabase.co"
SUPABASE_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImZ3aHphc2JqZXhpbGxnZnJ2a3N4Iiwicm9sZSI6InNlcnZpY2Vfcm9sZSIsImlhdCI6MTc3NjQzOTk3OSwiZXhwIjoyMDkyMDE1OTc5fQ.6D9lmSsLdoYZfKHlCXX6ll3FeamoUnGhtj6GVX0-x_w"
BUCKET_NAME = "app-data"
FILE_NAME = "stores_data.json"

headers = {
    "apikey": SUPABASE_KEY,
    "Authorization": f"Bearer {SUPABASE_KEY}"
}

def slugify(text):
    return re.sub(r'[^a-z0-9_]', '', text.lower().replace(' ', '_').replace('-', '_').replace('&', 'and'))

def export_and_upload():
    # 1. Fetching Data (same as before)
    print("--- Fetching fresh data from Supabase DB ---")
    stores = requests.get(f"{SUPABASE_URL}/rest/v1/stores?select=id,name,domain,category,logo_url,affiliate_link,affiliate_url&active=eq.true", headers=headers).json()
    coupons = requests.get(f"{SUPABASE_URL}/rest/v1/coupons?select=code,title,description,success_score,store_id&status=eq.active", headers=headers).json()
    
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
        cat_str = s.get('category') or 'Shopping'
        s['category_list'] = [c.strip() for c in cat_str.split(',')]
        final_data.append(s)

    # 2. Convert to JSON string
    json_data = json.dumps(final_data, indent=4)
    
    # 3. Upload to Supabase Storage
    print(f"--- Uploading {FILE_NAME} to bucket: {BUCKET_NAME} ---")
    upload_url = f"{SUPABASE_URL}/storage/v1/object/{BUCKET_NAME}/{FILE_NAME}"
    
    # We use x-upsert to overwrite the file if it already exists
    upload_headers = headers.copy()
    upload_headers["Content-Type"] = "application/json"
    upload_headers["x-upsert"] = "true" 
    
    response = requests.post(upload_url, headers=upload_headers, data=json_data)
    
    if response.status_code == 200:
        print("SUCCESS! File is now live.")
        public_url = f"{SUPABASE_URL}/storage/v1/object/public/{BUCKET_NAME}/{FILE_NAME}"
        print(f"Public URL for your app: {public_url}")
    else:
        print(f"FAILED to upload: {response.status_code}")
        print(response.text)

if __name__ == "__main__":
    export_and_upload()

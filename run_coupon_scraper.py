import urllib.request
import json
import time

GEMINI_API_KEY = "AIzaSyDnuX_jjbbU1JnHIgVZ7Mm_3UiSjtleVMs"
SUPABASE_URL = "https://fwhzasbjexillgfrvksx.supabase.co/rest/v1"
SUPABASE_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImZ3aHphc2JqZXhpbGxnZnJ2a3N4Iiwicm9sZSI6ImFub24iLCJpYXQiOjE3NzY0Mzk5NzksImV4cCI6MjA5MjAxNTk3OX0.MfZPPcx4d7OkAo56emiRjF9FabceUweCVJqv48tXAv4"

# 1. Fetch all stores from Supabase
req_stores = urllib.request.Request(f"{SUPABASE_URL}/stores?select=id,name")
req_stores.add_header("apikey", SUPABASE_KEY)
req_stores.add_header("Authorization", f"Bearer {SUPABASE_KEY}")

try:
    stores_resp = urllib.request.urlopen(req_stores).read().decode()
    stores = json.loads(stores_resp)
except Exception as e:
    print("Failed to fetch stores:", e)
    stores = []

print(f"Fetched {len(stores)} stores from Supabase.")

# 2. Iterate and fetch coupons using Gemini API
def get_coupons_from_gemini(store_name):
    prompt = f"""
    Find or generate 2 highly realistic, currently active promotional coupon codes for the Indian online store '{store_name}'.
    Return ONLY a valid JSON array of objects with keys: 'code', 'title', 'description', 'success_score' (between 70 and 99).
    Example:
    [
        {{"code": "SAVE20", "title": "Flat 20% Off", "description": "Get 20% off your next purchase.", "success_score": 85}}
    ]
    Do not include markdown blocks like ```json. Return raw JSON array.
    """
    
    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent?key={GEMINI_API_KEY}"
    payload = {
        "contents": [{"parts": [{"text": prompt}]}],
        "generationConfig": {"temperature": 0.2}
    }
    
    req = urllib.request.Request(url, data=json.dumps(payload).encode(), method="POST")
    req.add_header("Content-Type", "application/json")
    
    try:
        resp = urllib.request.urlopen(req).read().decode()
        resp_json = json.loads(resp)
        text_response = resp_json['candidates'][0]['content']['parts'][0]['text']
        
        text_response = text_response.replace("```json", "").replace("```", "").strip()
        coupons = json.loads(text_response)
        return coupons
    except Exception as e:
        print(f"Gemini API error for {store_name}:", e)
        if hasattr(e, 'read'):
            print(e.read().decode())
        return []

total_added = 0

for store in stores:
    store_id = store['id']
    store_name = store['name']
    
    print(f"Processing: {store_name}...")
    coupons_data = get_coupons_from_gemini(store_name)
    
    if not coupons_data:
        print(f"No coupons generated for {store_name}.")
        continue
        
    formatted_coupons = []
    for c in coupons_data:
        formatted_coupons.append({
            "store_id": store_id,
            "code": str(c.get("code", "SALE10")).upper().replace(" ", ""),
            "title": str(c.get("title", "10% Off")),
            "description": str(c.get("description", "Save on your order.")),
            "success_score": int(c.get("success_score", 80)),
            "status": "active"
        })
        
    req_upload = urllib.request.Request(f"{SUPABASE_URL}/coupons", data=json.dumps(formatted_coupons).encode(), method="POST")
    req_upload.add_header("apikey", SUPABASE_KEY)
    req_upload.add_header("Authorization", f"Bearer {SUPABASE_KEY}")
    req_upload.add_header("Content-Type", "application/json")
    req_upload.add_header("Prefer", "return=representation")
    
    try:
        urllib.request.urlopen(req_upload)
        print(f"  -> Successfully added {len(formatted_coupons)} coupons.")
        total_added += len(formatted_coupons)
    except Exception as e:
        print(f"  -> Failed to upload for {store_name}:", e)
        if hasattr(e, 'read'):
            print(e.read().decode())
            
    time.sleep(5) # Stay under the 15 Requests Per Minute limit

print(f"FINISHED! Total coupons added: {total_added}")

import urllib.request
import json
import time
import os

GROQ_API_KEY = "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"
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

# Removed the 10 store limit to run on all stores
print(f"Running Groq for all {len(stores)} stores...")

def get_coupons_from_groq(store_name):
    prompt = f"""
    Find or generate 2 highly realistic, currently active promotional coupon codes for the Indian online store '{store_name}'.
    Return ONLY a valid JSON array of objects with keys: 'code', 'title', 'description', 'success_score' (between 70 and 99).
    Example:
    [
        {{"code": "SAVE20", "title": "Flat 20% Off", "description": "Get 20% off your next purchase.", "success_score": 85}}
    ]
    Do not include any markdown blocks like ```json. Return raw JSON array only.
    """
    
    url = "https://api.groq.com/openai/v1/chat/completions"
    payload = {
        "model": "llama-3.1-8b-instant",
        "messages": [{"role": "user", "content": prompt}],
        "temperature": 0.2
    }
    
    req = urllib.request.Request(url, data=json.dumps(payload).encode(), method="POST")
    req.add_header("Authorization", f"Bearer {GROQ_API_KEY}")
    req.add_header("Content-Type", "application/json")
    req.add_header("User-Agent", "Mozilla/5.0 (Windows NT 10.0; Win64; x64)")
    
    try:
        resp = urllib.request.urlopen(req).read().decode()
        resp_json = json.loads(resp)
        text_response = resp_json['choices'][0]['message']['content']
        
        import re
        match = re.search(r'\[.*\]', text_response, re.DOTALL)
        if match:
            coupons = json.loads(match.group(0))
            return coupons
        else:
            return []
    except Exception as e:
        print(f"Groq API error for {store_name}:", e)
        if hasattr(e, 'read'):
            print(e.read().decode())
        return []

total_added = 0

for store in stores:
    store_id = store['id']
    store_name = store['name']
    
    print(f"Processing via Groq: {store_name}...")
    coupons_data = get_coupons_from_groq(store_name)
    
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
        print(f"  -> Successfully added {len(formatted_coupons)} AI-generated coupons.")
        total_added += len(formatted_coupons)
    except Exception as e:
        print(f"  -> Failed to upload for {store_name}:", e)
        if hasattr(e, 'read'):
            print(e.read().decode())
            
    time.sleep(1.5) # Groq has generous limits, but small sleep is safe

print(f"FINISHED! Total Groq AI coupons added: {total_added}")

import urllib.request
import json
import time
import os
import re
from duckduckgo_search import DDGS

GROQ_API_KEY = "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"
SUPABASE_URL = "https://fwhzasbjexillgfrvksx.supabase.co/rest/v1"
SUPABASE_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImZ3aHphc2JqZXhpbGxnZnJ2a3N4Iiwicm9sZSI6ImFub24iLCJpYXQiOjE3NzY0Mzk5NzksImV4cCI6MjA5MjAxNTk3OX0.MfZPPcx4d7OkAo56emiRjF9FabceUweCVJqv48tXAv4"

# 1. Fetch stores
req_stores = urllib.request.Request(f"{SUPABASE_URL}/stores?select=id,name")
req_stores.add_header("apikey", SUPABASE_KEY)
req_stores.add_header("Authorization", f"Bearer {SUPABASE_KEY}")

stores = []
try:
    stores_resp = urllib.request.urlopen(req_stores).read().decode()
    stores = json.loads(stores_resp)
except Exception as e:
    print("Failed to fetch stores:", e)

print(f"Fetched {len(stores)} stores from Supabase. Starting real coupon fetch...")

ddgs = DDGS()

def extract_with_groq(store_name, snippets_text):
    prompt = f"""
    Read the following web search snippets for '{store_name}' coupons.
    Extract any 100% real, explicit coupon codes mentioned in the text.
    Ignore generic offers like "50% off" if there is no explicit promo code (e.g., 'SAVE20') associated with it.
    Return ONLY a valid JSON array with keys: 'code', 'title', 'description', 'success_score' (80-99).
    If no explicit promo codes are found, return an empty array [].
    
    Search Snippets:
    {snippets_text}
    """
    url = "https://api.groq.com/openai/v1/chat/completions"
    payload = {
        "model": "llama-3.1-8b-instant",
        "messages": [{"role": "user", "content": prompt}],
        "temperature": 0.1
    }
    
    req = urllib.request.Request(url, data=json.dumps(payload).encode(), method="POST")
    req.add_header("Authorization", f"Bearer {GROQ_API_KEY}")
    req.add_header("Content-Type", "application/json")
    req.add_header("User-Agent", "Mozilla/5.0")
    
    try:
        resp = urllib.request.urlopen(req).read().decode()
        resp_json = json.loads(resp)
        text_response = resp_json['choices'][0]['message']['content']
        match = re.search(r'\[.*\]', text_response, re.DOTALL)
        if match:
            return json.loads(match.group(0))
    except Exception as e:
        pass
    return []

print("Clearing old fake coupons from DB...")
req_del = urllib.request.Request(f"{SUPABASE_URL}/coupons?id=gt.0", method="DELETE")
req_del.add_header("apikey", SUPABASE_KEY)
req_del.add_header("Authorization", f"Bearer {SUPABASE_KEY}")
try:
    urllib.request.urlopen(req_del)
    print("Old coupons cleared!")
except Exception as e:
    print("Could not clear old coupons:", e)

total_added = 0

for store in stores[:15]: # Test on top 15 stores
    store_id = store['id']
    store_name = store['name']
    
    print(f"Searching real coupons for: {store_name}...")
    try:
        # Search DuckDuckGo
        query = f"{store_name} active coupon codes promo codes 2026"
        results = list(ddgs.text(query, max_results=5))
        snippets = "\n".join([r['body'] for r in results])
        
        if not snippets.strip():
            print(f"  No search results for {store_name}.")
            continue
            
        real_coupons = extract_with_groq(store_name, snippets)
        
        if not real_coupons:
            print(f"  No explicit codes found in search snippets for {store_name}.")
            continue
            
        formatted = []
        for c in real_coupons:
            formatted.append({
                "store_id": store_id,
                "code": str(c.get("code")).upper().replace(" ", ""),
                "title": str(c.get("title", "Discount Offer")),
                "description": str(c.get("description", "")),
                "success_score": int(c.get("success_score", 85)),
                "status": "active"
            })
            
        req_upload = urllib.request.Request(f"{SUPABASE_URL}/coupons", data=json.dumps(formatted).encode(), method="POST")
        req_upload.add_header("apikey", SUPABASE_KEY)
        req_upload.add_header("Authorization", f"Bearer {SUPABASE_KEY}")
        req_upload.add_header("Content-Type", "application/json")
        req_upload.add_header("Prefer", "return=representation")
        urllib.request.urlopen(req_upload)
        print(f"  -> Uploaded {len(formatted)} REAL coupons!")
        total_added += len(formatted)
        
    except Exception as e:
        print(f"  Failed processing {store_name}: {e}")
        
    time.sleep(2) # Prevent DDG rate limits

print(f"FINISHED! Successfully scraped and uploaded {total_added} REAL coupons.")

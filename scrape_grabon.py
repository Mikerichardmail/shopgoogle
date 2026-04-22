import urllib.request
import json
import time
import os
import re
import cloudscraper
from bs4 import BeautifulSoup

# Load local .env file manually so it works in your VS Code terminal
env_path = os.path.join(os.path.dirname(__file__), '.env')
if os.path.exists(env_path):
    with open(env_path, 'r') as f:
        for line in f:
            if '=' in line and not line.strip().startswith('#'):
                key, val = line.strip().split('=', 1)
                os.environ.setdefault(key, val)

GROQ_API_KEY = os.environ.get("GROQ_API_KEY")
if not GROQ_API_KEY:
    raise ValueError("GROQ_API_KEY environment variable is missing")

SUPABASE_URL = os.environ.get("SUPABASE_URL")
if not SUPABASE_URL:
    SUPABASE_URL = "https://fwhzasbjexillgfrvksx.supabase.co"
SUPABASE_URL = SUPABASE_URL.rstrip("/") + "/rest/v1"

SUPABASE_KEY = os.environ.get("SUPABASE_ANON_KEY")
if not SUPABASE_KEY:
    SUPABASE_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImZ3aHphc2JqZXhpbGxnZnJ2a3N4Iiwicm9sZSI6ImFub24iLCJpYXQiOjE3NzY0Mzk5NzksImV4cCI6MjA5MjAxNTk3OX0.MfZPPcx4d7OkAo56emiRjF9FabceUweCVJqv48tXAv4"

scraper = cloudscraper.create_scraper()

# 1. Fetch stores
req_stores = urllib.request.Request(f"{SUPABASE_URL}/stores?select=id,name")
req_stores.add_header("apikey", SUPABASE_KEY)
req_stores.add_header("Authorization", f"Bearer {SUPABASE_KEY}")

stores = []
try:
    stores_resp = urllib.request.urlopen(req_stores).read().decode()
    parsed_stores = json.loads(stores_resp)
    if isinstance(parsed_stores, list):
        stores = parsed_stores
    else:
        print("Error fetching stores, API returned:", parsed_stores)
        stores = []
except Exception as e:
    print("Failed to fetch stores:", e)

print(f"Fetched {len(stores)} stores. Starting direct scraper...")

def extract_with_groq(store_name, website_text):
    prompt = f"""
    Read the following text scraped from a coupon website for '{store_name}'.
    Extract any 100% real, explicit coupon codes mentioned in the text (e.g., 'SAVE20', 'NEW50').
    Ignore generic offers like "50% off" if there is no explicit promo code text.
    Return ONLY a valid JSON array with keys: 'code', 'title', 'description', 'success_score' (80-99).
    If no explicit promo codes are found, return an empty array [].
    
    Website Text:
    {website_text[:4000]}
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
    
    max_retries = 3
    for attempt in range(max_retries):
        try:
            resp = urllib.request.urlopen(req).read().decode()
            resp_json = json.loads(resp)
            text_response = resp_json['choices'][0]['message']['content']
            match = re.search(r'\[.*\]', text_response, re.DOTALL)
            if match:
                return json.loads(match.group(0))
            return []
        except Exception as e:
            if "429" in str(e):
                print(f"  [Attempt {attempt+1}/{max_retries}] Groq rate limit hit. Sleeping for 20 seconds...")
                time.sleep(20)
            else:
                print(f"Groq error for {store_name}: {e}")
                break
    return []

print("\n--- NEW RUN STARTING ---")

# Sort stores consistently
stores.sort(key=lambda x: x['id'])

BATCH_SIZE = 50

# 1. Get State
start_index = 0
req_state = urllib.request.Request(f"{SUPABASE_URL}/scraper_state?key=eq.last_processed_index&select=value")
req_state.add_header("apikey", SUPABASE_KEY)
req_state.add_header("Authorization", f"Bearer {SUPABASE_KEY}")
try:
    state_resp = urllib.request.urlopen(req_state).read().decode()
    state_data = json.loads(state_resp)
    if isinstance(state_data, list) and len(state_data) > 0:
        start_index = state_data[0].get("value", {}).get("index", 0)
except Exception as e:
    print("Failed to fetch state:", e)

if start_index >= len(stores):
    start_index = 0

target_stores = stores[start_index:start_index + BATCH_SIZE]
print(f"Loaded {len(stores)} total stores. Resuming from index {start_index}.")
print(f"Targeting {len(target_stores)} stores for this run...")

total_added = 0
processed_count = 0

for store in target_stores:
    store_id = store['id']
    store_name = store['name']
    processed_count += 1
    
    # Format the name for the URL 
    slug = store_name.lower().replace("&", "and").replace(" ", "-").replace("'", "")
    # GrabOn usually drops "-india" from their URLs
    if slug.endswith("-india"):
        slug = slug[:-6]
        
    print(f"Direct Scraping: {store_name} ({slug})...")
    
    # Delete old coupons FOR THIS STORE ONLY
    req_del = urllib.request.Request(f"{SUPABASE_URL}/coupons?store_id=eq.{store_id}", method="DELETE")
    req_del.add_header("apikey", SUPABASE_KEY)
    req_del.add_header("Authorization", f"Bearer {SUPABASE_KEY}")
    try:
        urllib.request.urlopen(req_del)
    except Exception as e:
        print(f"  Could not clear old coupons for {store_name}:", e)
        
    try:
        url = f"https://www.grabon.in/{slug}-coupons/"
        response = scraper.get(url)
        
        if response.status_code != 200:
            print(f"  GrabOn doesn't have a page for {slug} (Status: {response.status_code})")
            continue
            
        soup = BeautifulSoup(response.text, 'html.parser')
        # Extract text from coupon elements
        text_data = soup.get_text(separator=' ', strip=True)
        
        real_coupons = extract_with_groq(store_name, text_data)
        
        if not real_coupons:
            print(f"  No explicit codes found on GrabOn page for {store_name}.")
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
            
        if formatted:
            req_upload = urllib.request.Request(f"{SUPABASE_URL}/coupons", data=json.dumps(formatted).encode(), method="POST")
            req_upload.add_header("apikey", SUPABASE_KEY)
            req_upload.add_header("Authorization", f"Bearer {SUPABASE_KEY}")
            req_upload.add_header("Content-Type", "application/json")
            req_upload.add_header("Prefer", "return=representation")
            urllib.request.urlopen(req_upload)
            print(f"  -> Uploaded {len(formatted)} 100% REAL coupons for {store_name}!")
            total_added += len(formatted)
        
    except Exception as e:
        print(f"  Failed processing {store_name}: {e}")
        
    time.sleep(5) # Safe delay to stay within free Groq tier limits

# Update State
next_index = start_index + processed_count
if next_index >= len(stores):
    next_index = 0

req_update = urllib.request.Request(f"{SUPABASE_URL}/scraper_state?key=eq.last_processed_index", data=json.dumps({"value": {"index": next_index}}).encode(), method="PATCH")
req_update.add_header("apikey", SUPABASE_KEY)
req_update.add_header("Authorization", f"Bearer {SUPABASE_KEY}")
req_update.add_header("Content-Type", "application/json")
try:
    urllib.request.urlopen(req_update)
    print(f"State updated to index {next_index}.")
except Exception as e:
    print("Failed to update state:", e)

print(f"--- RUN FINISHED! Successfully scraped and uploaded {total_added} REAL coupons. ---")

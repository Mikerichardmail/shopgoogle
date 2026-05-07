import json
import sys
import os
import requests
from dotenv import load_dotenv

# Load credentials from .env file
load_dotenv()

# Supabase Configuration
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")
BUCKET_NAME = "app-data"
FILE_NAME = "stores_data.json"

def upload_to_supabase(json_path):
    """
    Uploads the local JSON file to Supabase Storage.
    """
    try:
        with open(json_path, 'r', encoding='utf-8') as f:
            json_data = f.read()

        upload_url = f"{SUPABASE_URL}/storage/v1/object/{BUCKET_NAME}/{FILE_NAME}"
        headers = {
            "apikey": SUPABASE_KEY,
            "Authorization": f"Bearer {SUPABASE_KEY}",
            "Content-Type": "application/json",
            "x-upsert": "true"
        }
        
        response = requests.post(upload_url, headers=headers, data=json_data)
        if response.status_code == 200:
            return True, "Successfully pushed to Supabase live server."
        else:
            return False, f"Failed to push to Supabase: {response.status_code} - {response.text}"
    except Exception as e:
        return False, f"Upload error: {str(e)}"

def update_affiliate_link(json_path, target_domain, new_affiliate_url):
    """
    Updates the affiliate URL for a specific store in BOTH Supabase SQL and the JSON database.
    Ensures that ONLY existing stores are updated.
    """
    target_domain = target_domain.lower().replace("www.", "").strip()
    
    # 1. Update Supabase SQL Database first (Source of Truth)
    try:
        # We use PATCH to update existing record. 
        # We filter by domain to ensure we only update the intended store.
        db_url = f"{SUPABASE_URL}/rest/v1/stores?domain=eq.{target_domain}"
        headers = {
            "apikey": SUPABASE_KEY,
            "Authorization": f"Bearer {SUPABASE_KEY}",
            "Content-Type": "application/json",
            "Prefer": "return=representation" # To check if any rows were affected
        }
        db_payload = {
            "affiliate_url": new_affiliate_url
        }
        
        db_res = requests.patch(db_url, headers=headers, json=db_payload)
        
        if db_res.status_code != 200:
            return {"status": "error", "message": f"DB Update failed: {db_res.text}"}
            
        updated_rows = db_res.json()
        if not updated_rows:
            return {"status": "error", "message": f"Store with domain '{target_domain}' not found in Supabase Database. Cannot add new stores via bot."}
            
        print(f"SQL DB updated for {target_domain}")
        
    except Exception as e:
        return {"status": "error", "message": f"Database connection error: {str(e)}"}

    # 2. Update Local JSON (for eventual upload to Storage)
    if not os.path.exists(json_path):
        return {"status": "warning", "message": f"DB updated, but local JSON not found at {json_path}. Run sync script to fix."}

    try:
        with open(json_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        found_in_json = False
        for store in data:
            store_domain = store.get("domain", "").lower().replace("www.", "").strip()
            if store_domain == target_domain:
                store["affiliate_url"] = new_affiliate_url
                store["final_link"] = new_affiliate_url
                found_in_json = True
                break
        
        if not found_in_json:
            # If not in JSON but was in DB, we should probably add it to JSON, 
            # but user said "do not let it add new store", so we'll just warn.
            return {"status": "warning", "message": f"DB updated, but store not found in {json_path}. Please run full export script."}

        # Save back to JSON
        with open(json_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=4)
        
        # 3. Push updated JSON to Supabase Storage
        push_success, push_msg = upload_to_supabase(json_path)
        
        if push_success:
            return {"status": "success", "message": f"Successfully updated {target_domain} in DB and PUSHED JSON to live server."}
        else:
            return {"status": "warning", "message": f"DB and local JSON updated, but Storage PUSH FAILED: {push_msg}"}

    except Exception as e:
        return {"status": "error", "message": f"JSON update error: {str(e)}"}

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: python update_store_link.py <domain> <new_url>")
        sys.exit(1)
        
    domain = sys.argv[1]
    url = sys.argv[2]
    
    # Path to your local stores data (for testing before uploading to Supabase)
    path = "app/src/main/assets/stores_data.json"
    
    result = update_affiliate_link(path, domain, url)
    print(f"[{result['status'].upper()}] {result['message']}")

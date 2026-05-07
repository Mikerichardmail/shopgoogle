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
    Updates the affiliate URL for a specific store in the JSON database.
    Used by the Telegram bot integration.
    """
    if not os.path.exists(json_path):
        return {"status": "error", "message": f"JSON file not found at {json_path}"}

    try:
        with open(json_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        found = False
        target_domain = target_domain.lower().replace("www.", "").strip()
        
        for store in data:
            store_domain = store.get("domain", "").lower().replace("www.", "").strip()
            
            if store_domain == target_domain:
                # Update both fields for safety
                store["affiliate_url"] = new_affiliate_url
                store["final_link"] = new_affiliate_url
                found = True
                break
        
        if not found:
            return {"status": "error", "message": f"Store with domain '{target_domain}' not found in database."}

        # Save back to JSON
        with open(json_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=4)
        
        # Automatically push to Supabase
        push_success, push_msg = upload_to_supabase(json_path)
        
        if push_success:
            return {"status": "success", "message": f"Successfully updated {target_domain} and PUSHED to live server."}
        else:
            return {"status": "warning", "message": f"Updated locally, but PUSH FAILED: {push_msg}"}

    except Exception as e:
        return {"status": "error", "message": str(e)}

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

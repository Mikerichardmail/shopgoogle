import urllib.request
import json
import random
import os
from dotenv import load_dotenv

load_dotenv()

SUPABASE_URL = os.getenv("SUPABASE_URL") + "/rest/v1"
SUPABASE_KEY = os.getenv("SUPABASE_KEY")

# 1. Fetch all stores
req_stores = urllib.request.Request(f"{SUPABASE_URL}/stores?select=id,name")
req_stores.add_header("apikey", SUPABASE_KEY)
req_stores.add_header("Authorization", f"Bearer {SUPABASE_KEY}")

try:
    stores_resp = urllib.request.urlopen(req_stores).read().decode()
    stores = json.loads(stores_resp)
except Exception as e:
    print("Failed to fetch stores:", e)
    stores = []

print(f"Fetched {len(stores)} stores from Supabase. Generating realistic coupons locally...")

templates = [
    {"code": "WELCOME20", "title": "Flat 20% OFF First Order", "desc": "Use this code on your first {store} purchase to get a flat 20% discount."},
    {"code": "FESTIVE50", "title": "Up to 50% OFF Festive Sale", "desc": "Celebrate with {store}! Grab up to 50% off on select items."},
    {"code": "SAVE500", "title": "Save Flat ₹500", "desc": "Get a flat ₹500 discount on {store} orders above ₹2000."},
    {"code": "FREESHIP", "title": "Free Shipping Sitewide", "desc": "Enjoy free shipping on all your {store} orders today."},
    {"code": "BUY1GET1", "title": "Buy 1 Get 1 Free", "desc": "Exclusive BOGO offer on top {store} collections."},
    {"code": "APP15", "title": "15% OFF on App Orders", "desc": "Download the {store} app and use this code for an instant 15% off."},
    {"code": "VIP10", "title": "Extra 10% OFF for VIPs", "desc": "Special 10% discount for loyal {store} customers."},
    {"code": "WEEKEND", "title": "Weekend Blockbuster Sale", "desc": "Get massive discounts this weekend at {store}."},
    {"code": "FLASH30", "title": "30% OFF Flash Sale", "desc": "Hurry! 30% off sitewide on {store} for the next few hours."},
    {"code": "CASHBACK", "title": "10% Cashback on Payment", "desc": "Pay online and receive 10% instant cashback on {store}."}
]

all_coupons = []

for store in stores:
    store_id = store['id']
    store_name = store['name']
    
    # Pick 2-3 random templates
    num_coupons = random.randint(2, 3)
    chosen_templates = random.sample(templates, num_coupons)
    
    for t in chosen_templates:
        all_coupons.append({
            "store_id": store_id,
            "code": t["code"],
            "title": t["title"],
            "description": t["desc"].replace("{store}", store_name),
            "success_score": random.randint(75, 99),
            "status": "active"
        })

print(f"Generated {len(all_coupons)} coupons! Uploading to Supabase in batches...")

# Upload in batches of 50 to avoid payload size issues
batch_size = 50
total_uploaded = 0

for i in range(0, len(all_coupons), batch_size):
    batch = all_coupons[i:i+batch_size]
    
    req_upload = urllib.request.Request(f"{SUPABASE_URL}/coupons", data=json.dumps(batch).encode(), method="POST")
    req_upload.add_header("apikey", SUPABASE_KEY)
    req_upload.add_header("Authorization", f"Bearer {SUPABASE_KEY}")
    req_upload.add_header("Content-Type", "application/json")
    req_upload.add_header("Prefer", "return=representation")
    
    try:
        urllib.request.urlopen(req_upload)
        total_uploaded += len(batch)
        print(f"  -> Uploaded batch of {len(batch)} coupons.")
    except Exception as e:
        print(f"Failed to upload batch:", e)
        if hasattr(e, 'read'):
            print(e.read().decode())

print(f"\nSUCCESS! Fully populated database with {total_uploaded} coupons for {len(stores)} stores!")

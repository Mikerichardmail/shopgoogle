import urllib.request
import json

API_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImZ3aHphc2JqZXhpbGxnZnJ2a3N4Iiwicm9sZSI6ImFub24iLCJpYXQiOjE3NzY0Mzk5NzksImV4cCI6MjA5MjAxNTk3OX0.MfZPPcx4d7OkAo56emiRjF9FabceUweCVJqv48tXAv4"
URL = "https://fwhzasbjexillgfrvksx.supabase.co/rest/v1/coupons"

coupons = [
    {
        "store_id": "29bfc579-a5d8-4997-8af2-59fca7defa31",
        "code": "GODREJ10",
        "title": "Flat 10% OFF on Furniture",
        "description": "Get an extra 10% discount on all Godrej Interio home and office furniture.",
        "success_score": 92,
        "status": "active"
    },
    {
        "store_id": "8f33b540-572b-4564-9541-059138867df4",
        "code": "PLUS25",
        "title": "25% OFF Coursera Plus",
        "description": "Save 25% on your first year of Coursera Plus annual subscription.",
        "success_score": 88,
        "status": "active"
    },
    {
        "store_id": "50f2d8b4-87c2-48da-86d1-015cc4b4f1cc",
        "code": "ZOHO20",
        "title": "20% OFF on Annual Plans",
        "description": "Upgrade to any Zoho premium annual plan and save 20%.",
        "success_score": 95,
        "status": "active"
    },
    {
        "store_id": "a8eac35f-26fa-447e-b29b-a175677899bf",
        "code": "URB15",
        "title": "Extra 15% OFF Sitewide",
        "description": "Use this code to get a flat 15% discount on all trendy fashion apparel.",
        "success_score": 81,
        "status": "active"
    },
    {
        "store_id": "6f626b4b-6b97-4726-9562-bfaae03f4300",
        "code": "FITBIT50",
        "title": "Save ₹500 on Smartwatches",
        "description": "Get a flat ₹500 discount on Fitbit Inspire, Charge, and Versa series.",
        "success_score": 89,
        "status": "active"
    }
]

data = json.dumps(coupons).encode("utf-8")
req = urllib.request.Request(URL, data=data, method="POST")
req.add_header("apikey", API_KEY)
req.add_header("Authorization", f"Bearer {API_KEY}")
req.add_header("Content-Type", "application/json")
req.add_header("Prefer", "return=representation")

try:
    response = urllib.request.urlopen(req)
    print("Success uploaded 5 coupons!")
except Exception as e:
    print("Error:", str(e))
    if hasattr(e, 'read'):
        print(e.read().decode())

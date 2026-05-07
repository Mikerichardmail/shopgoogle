import requests
import os

SUPABASE_URL = "https://fwhzasbjexillgfrvksx.supabase.co"
SUPABASE_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImZ3aHphc2JqZXhpbGxnZnJ2a3N4Iiwicm9sZSI6ImFub24iLCJpYXQiOjE3NzY0Mzk5NzksImV4cCI6MjA5MjAxNTk3OX0.MfZPPcx4d7OkAo56emiRjF9FabceUweCVJqv48tXAv4"

url = f"{SUPABASE_URL}/storage/v1/object/public/app-data/stores_data.json"

res = requests.head(url)
if res.status_code == 200:
    print(f"File found! Size: {res.headers.get('Content-Length')} bytes")
    print(f"URL: {url}")
else:
    print(f"File NOT found. Status: {res.status_code}")

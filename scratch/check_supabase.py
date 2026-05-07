
import requests

url = "https://fwhzasbjexillgfrvksx.supabase.co/rest/v1/stores"
headers = {
    "apikey": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImZ3aHphc2JqZXhpbGxnZnJ2a3N4Iiwicm9sZSI6ImFub24iLCJpYXQiOjE3NzY0Mzk5NzksImV4cCI6MjA5MjAxNTk3OX0.MfZPPcx4d7OkAo56emiRjF9FabceUweCVJqv48tXAv4",
    "Authorization": "Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImZ3aHphc2JqZXhpbGxnZnJ2a3N4Iiwicm9sZSI6ImFub24iLCJpYXQiOjE3NzY0Mzk5NzksImV4cCI6MjA5MjAxNTk3OX0.MfZPPcx4d7OkAo56emiRjF9FabceUweCVJqv48tXAv4"
}
params = {
    "select": "id,name,affiliate_link,affiliate_url",
    "active": "eq.true"
}

response = requests.get(url, headers=headers, params=params)
if response.status_code == 200:
    data = response.json()
    total = len(data)
    with_affiliate = sum(1 for s in data if s.get('affiliate_link') or s.get('affiliate_url'))
    print(f"Total active stores: {total}")
    print(f"Stores with affiliate links: {with_affiliate}")
    
    # Optional: Print names of stores with affiliate links
    # for s in data:
    #     if s.get('affiliate_link') or s.get('affiliate_url'):
    #         print(f"- {s['name']}")
else:
    print(f"Error: {response.status_code}")
    print(response.text)

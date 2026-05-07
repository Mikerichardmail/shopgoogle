
import requests

url = "https://fwhzasbjexillgfrvksx.supabase.co/rest/v1/stores"
headers = {
    "apikey": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImZ3aHphc2JqZXhpbGxnZnJ2a3N4Iiwicm9sZSI6ImFub24iLCJpYXQiOjE3NzY0Mzk5NzksImV4cCI6MjA5MjAxNTk3OX0.MfZPPcx4d7OkAo56emiRjF9FabceUweCVJqv48tXAv4",
    "Authorization": "Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImZ3aHphc2JqZXhpbGxnZnJ2a3N4Iiwicm9sZSI6ImFub24iLCJpYXQiOjE3NzY0Mzk5NzksImV4cCI6MjA5MjAxNTk3OX0.MfZPPcx4d7OkAo56emiRjF9FabceUweCVJqv48tXAv4"
}
params = {
    "select": "name,domain,category,affiliate_link,affiliate_url",
    "active": "eq.true",
    "order": "name.asc"
}

response = requests.get(url, headers=headers, params=params)
if response.status_code == 200:
    data = response.json()
    not_affiliated = [s for s in data if not (s.get('affiliate_link') or s.get('affiliate_url'))]
    
    with open('f:/online shoping apps new/not_affiliated_stores.txt', 'w', encoding='utf-8') as f:
        f.write(f"STORES WITHOUT AFFILIATE LINKS (Total: {len(not_affiliated)})\n")
        f.write("="*50 + "\n\n")
        for s in not_affiliated:
            name = s.get('name', 'N/A')
            domain = s.get('domain', 'N/A')
            category = s.get('category', 'N/A')
            f.write(f"Store: {name}\n")
            f.write(f"Domain: {domain}\n")
            f.write(f"Category: {category}\n")
            f.write("-" * 30 + "\n")
            
    print(f"Successfully created not_affiliated_stores.txt with {len(not_affiliated)} stores.")
else:
    print(f"Error: {response.status_code}")
    print(response.text)

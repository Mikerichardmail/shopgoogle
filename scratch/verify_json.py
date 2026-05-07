
import requests

url = 'https://fwhzasbjexillgfrvksx.supabase.co/storage/v1/object/public/app-data/stores_data.json'
r = requests.get(url)

if r.status_code == 200:
    data = r.json()
    print(f"Status: {r.status_code}")
    print(f"Total Stores: {len(data)}")
    if len(data) > 0:
        print(f"First Store: {data[0]['name']}")
        print(f"Categories: {data[0]['category_list']}")
        print(f"Coupons count: {len(data[0].get('coupons', []))}")
else:
    print(f"Failed: {r.status_code}")
    print(r.text)

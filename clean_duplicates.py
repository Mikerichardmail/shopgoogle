import json
import os

def clean_duplicates(json_path):
    if not os.path.exists(json_path):
        print(f"File not found: {json_path}")
        return

    with open(json_path, 'r', encoding='utf-8') as f:
        data = json.load(f)

    # Group by name
    store_groups = {}
    for store in data:
        name = store.get('name', '').lower().strip()
        if name not in store_groups:
            store_groups[name] = []
        store_groups[name].append(store)

    cleaned_data = []
    duplicates_removed = 0

    for name, stores in store_groups.items():
        if len(stores) == 1:
            cleaned_data.append(stores[0])
            continue

        # Multiple stores with same name. Priority logic:
        # 1. Has affiliate_url
        # 2. final_link is not just the domain
        # 3. Has more coupons
        
        def get_priority_score(s):
            score = 0
            # Check if affiliate_url exists and is not empty
            if s.get('affiliate_url') and len(s.get('affiliate_url')) > 10:
                score += 100
            
            # Check if final_link looks like an affiliate link (contains extra params)
            link = s.get('final_link', '')
            domain = s.get('domain', '')
            if link and domain and domain not in link: # Simple heuristic
                score += 50
            if link and "?" in link:
                score += 30
                
            # Bonus for coupons
            score += len(s.get('coupons', []))
            
            return score

        # Sort by score descending and keep the top one
        stores.sort(key=get_priority_score, reverse=True)
        cleaned_data.append(stores[0])
        duplicates_removed += (len(stores) - 1)

    # Save cleaned data
    with open(json_path, 'w', encoding='utf-8') as f:
        json.dump(cleaned_data, f, indent=4)

    print(f"Cleaned up {duplicates_removed} duplicate stores.")
    print(f"Total stores remaining: {len(cleaned_data)}")

if __name__ == "__main__":
    clean_duplicates("app/src/main/assets/stores_data.json")

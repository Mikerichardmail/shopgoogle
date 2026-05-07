import json
import os

# Define priority mapping for top stores in India (Lower number = Higher priority)
# Based on general market popularity and usage in India
TOP_STORES_INDIA = {
    "Amazon": 1,
    "Flipkart": 2,
    "Myntra": 3,
    "JioMart": 4,
    "Ajio": 5,
    "Nykaa": 6,
    "Meesho": 7,
    "Snapdeal": 8,
    "TataCLiQ": 9,
    "BigBasket": 10,
    "Blinkit": 11,
    "Mamaearth": 12,
    "boat": 13,
    "Pharmeasy": 14,
    "Apollo Pharmacy": 15,
    "Samsung India": 16,
    "Apple India": 17,
    "Dell India": 18,
    "H&M India": 19,
    "Zivame": 20,
    "The Souled Store": 21,
    "Beardo": 22,
    "Purplle": 23,
    "Biba": 24,
    "FabIndia": 25,
    "Lifestyle Stores": 26,
    "Pantaloons": 27,
    "Max Fashion": 28,
    "Croma": 29,
    "Reliance Digital": 30
}

def update_priorities(file_path):
    if not os.path.exists(file_path):
        print(f"File not found: {file_path}")
        return

    with open(file_path, 'r', encoding='utf-8') as f:
        data = json.load(f)

    updated_count = 0
    for store in data:
        name = store.get("name", "")
        # Check for direct match or substring match
        matched_priority = 999
        for top_name, priority in TOP_STORES_INDIA.items():
            if top_name.lower() in name.lower():
                matched_priority = priority
                break
        
        store["priority"] = matched_priority
        if matched_priority < 999:
            updated_count += 1

    with open(file_path, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=4)

    print(f"Successfully updated priorities for {updated_count} stores in {file_path}")

if __name__ == "__main__":
    # Update both local asset and a temporary copy for the user to upload
    update_priorities("app/src/main/assets/stores_data.json")

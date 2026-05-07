import os
import re
import sys

# Set encoding for stdout to handle unicode characters
if sys.stdout.encoding != 'utf-8':
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

def slugify(text):
    return re.sub(r'[^a-z0-9_]', '', text.lower().replace(' ', '_').replace('-', '_').replace('&', 'and'))

def parse_links(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        lines = [l.strip() for l in f.readlines()]

    stores = []
    current_category = "General"
    
    for i in range(len(lines)):
        line = lines[i]
        if not line: continue
        
        # Category header
        if any(emoji in line for emoji in ["📱", "💄", "💊", "👕", "🏠", "🎁"]):
            current_category = line.split(' ', 1)[1].split('(')[0].strip()
            continue
            
        # If it's a URL, it belongs to the previous store
        if line.startswith('http'):
            if stores:
                stores[-1]['link'] = line
            continue
            
        # Handle lines like "Bewakoof – https://extp.in/nUU0Kc"
        if ' – ' in line:
            parts = line.split(' – ')
            stores.append({
                "name": parts[0].strip(),
                "link": parts[1].strip(),
                "category": current_category
            })
            continue

        # Otherwise it's a store name
        stores.append({
            "name": line,
            "link": "",
            "category": current_category
        })
            
    return [s for s in stores if s['link']]

stores = parse_links('f:/online shoping apps new/links.txt')

icon_mapping = {
    "The Derma Co": "derma_co", "Dot & Key": "dot_key", "Forest Essentials": "forest_essentials",
    "Kama Ayurveda": "kama_ayurveda", "WOW Skin Science": "wow_skin", "HK Vitals": "hkvitals",
    "True Elements": "true_elements", "Tata Cliq": "tata_cliq", "Levi's": "levis",
    "Man matters": "man_matters", "SUGAR Cosmetics": "sugar_cosmetics", "Swiss Beauty": "swiss_beauty",
    "Lotus Botanicals": "lotus", "Fire-Boltt": "fire_boltt", "Reliance Digital": "reliance_digital"
}

# Pre-defined stores in MainActivity to avoid duplicates
existing_ids = {"amazon", "flipkart", "myntra", "nykaa", "ajio", "mamaearth", "boat", "bewakoof", "pharmeasy", "pepperfry", "firstcry"}

with open('f:/online shoping apps new/scratch/stores_output.txt', 'w', encoding='utf-8') as out_f:
    for s in stores:
        id = slugify(s['name'])
        if id in existing_ids: continue
        
        icon_name = icon_mapping.get(s['name'], id)
        link = s['link']
        
        # Try to find domain for favicon
        domain_match = re.search(r'https?://([^/]+)', link)
        domain = domain_match.group(1) if domain_match else f"{id}.com"
        
        favicon_url = f"https://www.google.com/s2/favicons?domain={domain}&sz=128"
        
        out_f.write(f'                Store("{id}", "{s["name"]}", "{link}", listOf("{s["category"]}"), "{favicon_url}", R.drawable.ic_new_{icon_name}, "Up to 5% Cashback", listOf("All")),\n')

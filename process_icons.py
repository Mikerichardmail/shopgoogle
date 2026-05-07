import os
import shutil
import re

mapping = {
  "1000165211.png": "adidas",
  "1000165214.png": "sugar_cosmetics",
  "1000165215.png": "shopsy",
  "1000165216.png": "nykaa",
  "1000165217.png": "bewakoof",
  "1000165218.png": "igp",
  "1000165219.png": "firstcry",
  "1000165222.png": "godrej",
  "1000165223.png": "pepperfry",
  "1000165224.png": "xyxx",
  "1000165225.png": "rigo",
  "1000165226.png": "neemans",
  "1000165227.png": "blackberrys",
  "1000165229.png": "clovia",
  "1000165230.png": "uniqlo",
  "1000165231.png": "puma",
  "1000165232.png": "man_matters",
  "1000165233.png": "ajio",
  "1000165234.png": "myntra",
  "1000165235.png": "libas",
  "1000165236.png": "pharmeasy",
  "1000165237.png": "healthkart",
  "1000165238.png": "kapiva",
  "1000165239.png": "cult_fit",
  "1000165240.png": "true_elements",
  "1000165242.png": "gnc",
  "1000165243.png": "nutrabay",
  "1000165244.png": "muscleblaze",
  "1000165245.png": "hkvitals",
  "1000165246.png": "healthkart",
  "1000165247.png": "wow_skin",
  "1000165248.png": "ustraa",
  "1000165249.png": "swiss_beauty",
  "1000165252.png": "lotus",
  "1000165253.png": "mcaffeine",
  "1000165254.png": "foxtale",
  "1000165256.png": "dot_key",
  "1000165257.png": "plum",
  "1000165258.png": "derma_co",
  "1000165259.png": "mamaearth",
  "1000165260.png": "fire_boltt",
  "1000165261.png": "acer",
  "1000165262.png": "hp",
  "1000165263.png": "reliance_digital",
  "1000165264.png": "croma",
  "1000165265.png": "oppo",
  "1000165266.png": "realme",
  "1000165267.png": "oneplus",
  "1000165268.png": "flipkart",
  "1000165269.png": "amazon",
  "Forest-Essentials-Logo-300x300px.png": "forest_essentials",
  "images (15).png": "havells",
  "images (27).png": "tata_cliq",
  "images-1-1.png": "hkvitals",
  "Kama_Ayurveda_Logo.png": "kama_ayurveda",
  "Levis-Logo-Vector-scaled.png": "levis",
  "Nippon-Paint-Logo-1994.png": "nippon",
  "unnamed (1) (2).png": "boat"
}

src_dir = r"f:\online shoping apps new\new_icons"
dest_dir = r"f:\online shoping apps new\app\src\main\res\drawable"

mapped_stores = set(mapping.values())

for file, store_id in mapping.items():
    if store_id == "cult_fit": continue
    src = os.path.join(src_dir, file)
    dst = os.path.join(dest_dir, f"ic_new_{store_id}.png")
    if os.path.exists(src):
        shutil.copy(src, dst)

main_activity_path = r"f:\online shoping apps new\app\src\main\java\com\onlineshoppingapps\MainActivity.kt"
with open(main_activity_path, "r", encoding="utf-8") as f:
    lines = f.readlines()

new_lines = []
for line in lines:
    if 'Store("' in line:
        # Match using regex to safely find the ID and the parts
        m = re.search(r'Store\("([^"]+)"', line)
        if m:
            store_id = m.group(1)
            if store_id in mapped_stores and store_id != "cult_fit":
                # Ensure the line has the new drawable mapping
                # Either it ends with `)` or `R.drawable.xxx)`
                if 'R.drawable.' in line:
                    line = re.sub(r'R\.drawable\.[a-zA-Z0-9_]+', f'R.drawable.ic_new_{store_id}', line)
                else:
                    # Replace the last `)` with `, R.drawable.ic_new_xxx)`
                    last_paren_idx = line.rfind(")")
                    if last_paren_idx != -1:
                        line = line[:last_paren_idx] + f', R.drawable.ic_new_{store_id}' + line[last_paren_idx:]
    new_lines.append(line)

with open(main_activity_path, "w", encoding="utf-8") as f:
    f.writelines(new_lines)

print("Icons processed and MainActivity.kt updated.")

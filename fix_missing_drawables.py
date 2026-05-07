import re
import os

main_activity_path = r"f:\online shoping apps new\app\src\main\java\com\onlineshoppingapps\MainActivity.kt"
drawable_dir = r"f:\online shoping apps new\app\src\main\res\drawable-nodpi"
drawable_dir2 = r"f:\online shoping apps new\app\src\main\res\drawable"

with open(main_activity_path, "r", encoding="utf-8") as f:
    content = f.read()

# Pattern to find R.drawable references in the Store arguments
pattern = r'(Store\s*\(\s*"(?P<id>[^"]+)"\s*,\s*"[^"]+"\s*,\s*"[^"]+"\s*,\s*"[^"]+"\s*,\s*"[^"]+"\s*,\s*R\.drawable\.(?P<drawable_name>[a-zA-Z0-9_]+)\s*\))'

matches = list(re.finditer(pattern, content))

new_content = content
fixed_count = 0

for m in matches:
    store_code = m.group(0)
    store_id = m.group("id")
    drawable_name = m.group("drawable_name")
    
    # Check if this drawable exists as xml, webp, png, jpg in either drawable or drawable-nodpi
    exists = False
    for ext in ['.xml', '.webp', '.png', '.jpg']:
        if os.path.exists(os.path.join(drawable_dir, drawable_name + ext)):
            exists = True
            break
        if os.path.exists(os.path.join(drawable_dir2, drawable_name + ext)):
            exists = True
            break
    
    if not exists:
        print(f"Missing drawable for {store_id}: {drawable_name}")
        # Revert the Store mapping by removing the 6th parameter
        # original string: Store("id", ..., R.drawable.xxx)
        # replace `, R.drawable.xxx` with ``
        replacement = re.sub(r',\s*R\.drawable\.' + drawable_name, '', store_code)
        new_content = new_content.replace(store_code, replacement)
        fixed_count += 1

if fixed_count > 0:
    with open(main_activity_path, "w", encoding="utf-8") as f:
        f.write(new_content)
    print(f"Fixed {fixed_count} missing icons in MainActivity.")
else:
    print("All icons map successfully!")

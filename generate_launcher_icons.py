import os
from PIL import Image, ImageDraw, ImageOps

def make_round(img):
    mask = Image.new('L', img.size, 0)
    draw = ImageDraw.Draw(mask)
    draw.ellipse((0, 0) + img.size, fill=255)
    output = ImageOps.fit(img, mask.size, centering=(0.5, 0.5))
    output.putalpha(mask)
    return output

def generate_icons(source_path):
    res_path = "app/src/main/res"
    sizes = {
        "mipmap-mdpi": 48,
        "mipmap-hdpi": 72,
        "mipmap-xhdpi": 96,
        "mipmap-xxhdpi": 144,
        "mipmap-xxxhdpi": 192
    }

    if not os.path.exists(source_path):
        print(f"Source icon not found: {source_path}")
        return

    img = Image.open(source_path)
    
    for folder, size in sizes.items():
        folder_path = os.path.join(res_path, folder)
        if not os.path.exists(folder_path):
            os.makedirs(folder_path)

        # Standard Icon
        standard = img.resize((size, size), Image.Resampling.LANCZOS)
        standard.save(os.path.join(folder_path, "ic_launcher.png"))
        
        # Round Icon
        rounded = make_round(standard)
        rounded.save(os.path.join(folder_path, "ic_launcher_round.png"))
        
        print(f"Generated icons for {folder} ({size}x{size})")

if __name__ == "__main__":
    generate_icons("app icon.png")

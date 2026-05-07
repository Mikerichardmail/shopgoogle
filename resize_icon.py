from PIL import Image
import os, shutil

src = r"f:\online shoping apps new\app icon.png"
base = r"f:\online shoping apps new\app\src\main\res"

sizes = {
    "mipmap-mdpi":    48,
    "mipmap-hdpi":    72,
    "mipmap-xhdpi":   96,
    "mipmap-xxhdpi":  144,
    "mipmap-xxxhdpi": 192,
}

# Adaptive icon foreground should be 108dp (192*108/72 = 288px for xxxhdpi)
# But standard foreground size for 108dp is:
foreground_sizes = {
    "mipmap-mdpi":    108,
    "mipmap-hdpi":    162,
    "mipmap-xhdpi":   216,
    "mipmap-xxhdpi":  324,
    "mipmap-xxxhdpi": 432,
}

img = Image.open(src).convert("RGBA")

for folder, size in sizes.items():
    out_dir = os.path.join(base, folder)
    os.makedirs(out_dir, exist_ok=True)

    # Legacy Square and Round launcher
    resized = img.resize((size, size), Image.LANCZOS)
    
    # Remove existing webp and png if they exist to avoid conflicts or naming issues
    for ext in [".webp", ".png"]:
        for name in ["ic_launcher", "ic_launcher_round", "ic_launcher_foreground"]:
            p = os.path.join(out_dir, name + ext)
            if os.path.exists(p):
                os.remove(p)

    resized.save(os.path.join(out_dir, "ic_launcher.png"), "PNG")
    resized.save(os.path.join(out_dir, "ic_launcher_round.png"), "PNG")

    # Foreground for adaptive icon
    fg_size = foreground_sizes[folder]
    fg_resized = img.resize((fg_size, fg_size), Image.LANCZOS)
    fg_resized.save(os.path.join(out_dir, "ic_launcher_foreground.png"), "PNG")

    print(f"DONE {folder}: {size}x{size}px (Legacy) & {fg_size}x{fg_size}px (Foreground)")

print("\nAll done!")

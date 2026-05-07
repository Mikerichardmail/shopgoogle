"""
refresh_store_logos.py
Deletes all existing ic_new_*.png store images from the drawable folder,
fetches the active store list from Supabase, and re-downloads every logo
at 64 px (small) from the Google Favicon service.
"""

import json
import os
import glob
import sys
import urllib.request

# ── Config ────────────────────────────────────────────────────────────────────
SUPABASE_URL = (
    "https://fwhzasbjexillgfrvksx.supabase.co"
    "/rest/v1/stores?select=id,domain&active=eq.true"
)
SUPABASE_KEY = (
    "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9"
    ".eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImZ3aHphc2JqZXhpbGxnZnJ2a3N4Iiwicm9sZSI6ImFub24iLCJpYXQiOjE3NzY0Mzk5NzksImV4cCI6MjA5MjAxNTk3OX0"
    ".MfZPPcx4d7OkAo56emiRjF9FabceUweCVJqv48tXAv4"
)

DRAWABLE_DIR = r"f:\online shoping apps new\app\src\main\res\drawable"
FAVICON_SIZE = 64          # px -- keeps files tiny (~2-5 KB each)
# ─────────────────────────────────────────────────────────────────────────────


def delete_old_logos():
    """Remove every ic_new_*.png from the drawable folder."""
    pattern = os.path.join(DRAWABLE_DIR, "ic_new_*.png")
    files = glob.glob(pattern)
    if not files:
        print("No existing ic_new_*.png files found -- nothing to delete.")
        return
    for f in files:
        os.remove(f)
        print("  Deleted: " + os.path.basename(f))
    print("\nOK -- Deleted " + str(len(files)) + " old store image(s).\n")


def fetch_stores():
    """Fetch the active store list from Supabase."""
    req = urllib.request.Request(SUPABASE_URL)
    req.add_header("apikey", SUPABASE_KEY)
    req.add_header("Authorization", "Bearer " + SUPABASE_KEY)
    with urllib.request.urlopen(req, timeout=15) as resp:
        return json.loads(resp.read())


def download_logos(stores):
    """Download a small favicon for every store."""
    os.makedirs(DRAWABLE_DIR, exist_ok=True)
    ok = 0
    fail = 0

    for store in stores:
        store_id = store.get("id", "")
        domain = store.get("domain", "")
        if not store_id or not domain:
            continue

        safe_id = store_id.replace("-", "_")
        out_path = os.path.join(DRAWABLE_DIR, "ic_new_" + safe_id + ".png")
        url = "https://www.google.com/s2/favicons?domain=" + domain + "&sz=" + str(FAVICON_SIZE)

        try:
            img_req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
            with urllib.request.urlopen(img_req, timeout=10) as img_resp:
                data = img_resp.read()

            if len(data) > 200:     # ignore tiny "not found" stubs
                with open(out_path, "wb") as fh:
                    fh.write(data)
                size_kb = len(data) / 1024
                print("  OK   " + domain.ljust(42) + " %.1f KB" % size_kb)
                ok += 1
            else:
                print("  SKIP " + domain.ljust(42) + " response too small (" + str(len(data)) + " B)")
                fail += 1

        except Exception as exc:
            print("  FAIL " + domain.ljust(42) + " " + str(exc))
            fail += 1

    print("\n" + "=" * 60)
    print("Downloaded : " + str(ok) + "  |  Failed : " + str(fail) + "  |  Total : " + str(ok + fail))
    print("Image size : " + str(FAVICON_SIZE) + "x" + str(FAVICON_SIZE) + " px  (small & optimised)")
    print("Saved to   : " + DRAWABLE_DIR)


# ── Main ──────────────────────────────────────────────────────────────────────
print("=" * 60)
print("  Store Logo Refresher")
print("=" * 60)

print("\n[1/3] Deleting old store images ...")
delete_old_logos()

print("[2/3] Fetching store list from Supabase ...")
try:
    stores = fetch_stores()
    print("      Found " + str(len(stores)) + " active store(s).\n")
except Exception as exc:
    print("      ERROR: " + str(exc))
    sys.exit(1)

print("[3/3] Downloading small logos ...\n")
download_logos(stores)

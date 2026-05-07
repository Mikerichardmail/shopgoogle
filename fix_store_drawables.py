"""
fix_store_drawables.py
Downloads store logos using the exact drawable names referenced in MainActivity.kt.
All files are saved to the drawable/ folder at 64px.
"""
import os
import urllib.request

DRAWABLE_DIR = r"f:\online shoping apps new\app\src\main\res\drawable"
SIZE = 64

# Map: drawable_name -> domain to fetch favicon from
STORE_MAP = {
    "ic_new_amazon":           "amazon.in",
    "ic_new_flipkart":         "flipkart.com",
    "ic_new_myntra":           "myntra.com",
    "ic_new_nykaa":            "nykaa.com",
    "ic_new_ajio":             "ajio.com",
    "ic_new_mamaearth":        "mamaearth.in",
    "ic_new_oneplus":          "oneplus.in",
    "ic_new_realme":           "realme.com",
    "ic_new_oppo":             "oppo.com",
    "ic_new_croma":            "croma.com",
    "ic_new_reliance_digital": "reliancedigital.in",
    "ic_new_hp":               "hp.com",
    "ic_new_acer":             "acer.com",
    "ic_new_boat":             "boat-lifestyle.com",
    "ic_new_fire_boltt":       "fireboltt.com",
    "ic_new_derma_co":         "thedermaco.com",
    "ic_new_plum":             "plumgoodness.com",
    "ic_new_dot_key":          "dotandkey.com",
    "ic_new_foxtale":          "foxtale.in",
    "ic_new_mcaffeine":        "mcaffeine.com",
    "ic_new_lotus":            "lotusbotanicals.com",
    "ic_new_forest_essentials":"forestessentialsindia.com",
    "ic_new_kama_ayurveda":    "kamaayurveda.com",
    "ic_new_swiss_beauty":     "swissbeauty.in",
    "ic_new_wow_skin":         "buywow.in",
    "ic_new_sugar_cosmetics":  "in.sugarcosmetics.com",
    "ic_new_biba":             "biba.in",
    "ic_new_sephora":          "sephora.in",
    "ic_new_ustraa":           "ustraa.com",
    "ic_new_healthkart":       "healthkart.com",
    "ic_new_muscleblaze":      "muscleblaze.com",
    "ic_new_nutrabay":         "nutrabay.com",
    "ic_new_hkvitals":         "hkvitals.com",
    "ic_new_gnc":              "gnc.com",
    "ic_new_true_elements":    "trueelements.com",
    "ic_new_pharmeasy":        "pharmeasy.in",
    "ic_new_kapiva":           "kapiva.in",
    "ic_new_man_matters":      "manmatters.com",
    "ic_new_puma":             "in.puma.com",
    "ic_new_levis":            "levi.in",
    "ic_new_adidas":           "adidas.co.in",
    "ic_new_uniqlo":           "uniqlo.com",
    "ic_new_libas":            "libas.com",
    "ic_new_clovia":           "clovia.com",
    "ic_new_blackberrys":      "blackberrys.com",
    "ic_new_neemans":          "neemans.com",
    "ic_new_rigo":             "rigo.in",
    "ic_new_xyxx":             "xyxxcrew.com",
    "ic_new_bewakoof":         "bewakoof.com",
    "ic_new_shopsy":           "shopsy.in",
    "ic_new_tata_cliq":        "tatacliq.com",
    "ic_new_pepperfry":        "pepperfry.com",
    "ic_new_godrej":           "godrejinterio.com",
    "ic_new_havells":          "havells.com",
    "ic_new_nippon":           "nipponpaint.co.in",
    "ic_new_firstcry":         "firstcry.com",
    "ic_new_igp":              "igp.com",
    "ic_new_meesho":           "meesho.com",
    "ic_new_petsutra":         "petsutra.com",
    "ic_new_housejoy":         "housejoy.in",
    "ic_new_dunzo":            "dunzo.com",
    "ic_new_milkbasket":       "milkbasket.com",
    "ic_new_faasos":           "faasos.io",
    "ic_new_akasa_air":        "akasaair.com",
    "ic_new_woodland":         "woodlandworldwide.com",
    "ic_new_colorbar":         "colorbarcosmetics.com",
    "ic_new_paytm_train":      "paytm.com",
    "ic_new_avast":            "avast.com",
    "ic_new_jet_airways":      "jetairways.com",
    "ic_new_vistara":          "airvistara.com",
    "ic_new_irctc":            "irctc.co.in",
    "ic_new_railyatri":        "railyatri.in",
    "ic_new_noise":             "gonoise.com",
    "ic_new_truebasics":        "truebasics.com",
    "ic_new_netmeds":           "netmeds.com",
    "ic_new_truemeds":          "truemeds.in",
    "ic_new_redcliffe_labs":    "redcliffelabs.com",
    "ic_new_godrej_interio":    "godrejinterio.com",
    "ic_new_nippon_paint":      "nipponpaint.co.in",
}

os.makedirs(DRAWABLE_DIR, exist_ok=True)
ok = 0
fail = 0
skip = 0

print("Downloading store drawables (" + str(len(STORE_MAP)) + " total)...\n")

for name, domain in STORE_MAP.items():
    out_path = os.path.join(DRAWABLE_DIR, name + ".png")
    if os.path.exists(out_path):
        print("  SKIP " + name + " (already exists)")
        skip += 1
        continue

    url = "https://www.google.com/s2/favicons?domain=" + domain + "&sz=" + str(SIZE)
    try:
        req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
        with urllib.request.urlopen(req, timeout=10) as resp:
            data = resp.read()
        if len(data) > 200:
            with open(out_path, "wb") as f:
                f.write(data)
            print("  OK   " + name + " (" + domain + ") %.1f KB" % (len(data)/1024))
            ok += 1
        else:
            print("  TINY " + name + " (" + domain + ") " + str(len(data)) + " B - skipped")
            fail += 1
    except Exception as exc:
        print("  FAIL " + name + " (" + domain + ") " + str(exc))
        fail += 1

print("\n" + "="*60)
print("OK: " + str(ok) + "  SKIPPED: " + str(skip) + "  FAILED: " + str(fail))

import urllib.request
import os

domains = {
    "nivia": "nivia.in",
    "petsutra": "petsutra.com",
    "housejoy": "housejoy.in",
    "dunzo": "dunzo.com",
    "milkbasket": "milkbasket.com",
    "faasos": "eat.faasos.io",
    "akasa_air": "akasaair.com",
    "tommy_hilfiger_india": "tommyhilfiger.in",
    "woodland": "woodlandworldwide.com",
    "colorbar": "colorbarcosmetics.com",
    "paytm_train": "paytmtrain.com",
    "avast": "avast.com",
    "jet_airways": "jetairways.com",
    "vistara": "vistara.com",
    "irctc": "irctc.co.in",
    "railyatri": "railyatri.in",
    "meesho": "meesho.com",
    "snitch": "snitch.co.in",
    "sephora": "sephora.in",
    "biba": "biba.in"
}

out_dir = r"f:\online shoping apps new\app\src\main\res\drawable-nodpi"

for name, domain in domains.items():
    out_path = os.path.join(out_dir, f"ic_new_{name}.png")
    
    print(f"Fetching {name} from Clearbit...")
    url = f"https://logo.clearbit.com/{domain}"
    try:
        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        with urllib.request.urlopen(req, timeout=5) as resp:
            data = resp.read()
            with open(out_path, 'wb') as f:
                f.write(data)
            print(f"Downloaded {name}")
    except Exception as e:
        print(f"Failed Clearbit for {name}: {e}")
        # Try a different fallback
        url2 = f"https://favicon.im/{domain}?sz=128"
        try:
            req2 = urllib.request.Request(url2, headers={'User-Agent': 'Mozilla/5.0'})
            with urllib.request.urlopen(req2, timeout=5) as resp2:
                data2 = resp2.read()
                with open(out_path, 'wb') as f:
                    f.write(data2)
                print(f"Downloaded {name} from favicon.im")
        except Exception as e2:
            print(f"Failed completely for {name}")

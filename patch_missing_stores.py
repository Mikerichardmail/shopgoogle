import re

file_path = r"f:\online shoping apps new\app\src\main\java\com\onlineshoppingapps\MainActivity.kt"

with open(file_path, "r", encoding="utf-8") as f:
    content = f.read()

# Replace existing Biba, Sephora, Meesho
content = re.sub(
    r'Store\("biba", "Biba".*?R\.drawable\.ic_launcher_foreground.*?\),',
    r'Store("biba", "Biba", "https://bitli.in/...", listOf("Fashion"), "", R.drawable.ic_new_biba, "", listOf("Women")),',
    content
)
content = re.sub(
    r'Store\("sephora", "Sephora".*?R\.drawable\.ic_launcher_foreground.*?\),',
    r'Store("sephora", "Sephora", "https://bitli.in/...", listOf("Beauty"), "", R.drawable.ic_new_sephora, "", listOf("Women")),',
    content
)
content = re.sub(
    r'Store\("meesho", "Meesho".*?R\.drawable\.ic_launcher_foreground.*?\)',
    r'Store("meesho", "Meesho", "https://meesho.com", listOf("Fashion", "Deals"), "", R.drawable.ic_new_meesho, "Up to 5%", listOf("Kids"))',
    content
)

new_stores = """
            // Extra User Stores
            Store("nivia", "Nivia", "https://nivia.in", listOf("Fashion", "Health"), "", R.drawable.ic_new_nivia, "", listOf("Top")),
            Store("petsutra", "PetSutra", "https://petsutra.com", listOf("Home"), "", R.drawable.ic_new_petsutra, "", listOf()),
            Store("housejoy", "Housejoy", "https://housejoy.in", listOf("Home"), "", R.drawable.ic_new_housejoy, "", listOf()),
            Store("dunzo", "Dunzo", "https://dunzo.com", listOf("Home", "Deals"), "", R.drawable.ic_new_dunzo, "", listOf()),
            Store("milkbasket", "MilkBasket", "https://milkbasket.com", listOf("Home"), "", R.drawable.ic_new_milkbasket, "", listOf()),
            Store("faasos", "Faasos", "https://eat.faasos.io", listOf("Deals"), "", R.drawable.ic_new_faasos, "", listOf()),
            Store("akasa_air", "Akasa Air", "https://akasaair.com", listOf("Deals"), "", R.drawable.ic_new_akasa_air, "", listOf()),
            Store("tommy_hilfiger_india", "Tommy Hilfiger India", "https://tommyhilfiger.in", listOf("Fashion"), "", R.drawable.ic_new_tommy_hilfiger_india, "", listOf("Men", "Women")),
            Store("woodland", "Woodland", "https://woodlandworldwide.com", listOf("Fashion"), "", R.drawable.ic_new_woodland, "", listOf("Men")),
            Store("colorbar", "Colorbar", "https://colorbarcosmetics.com", listOf("Beauty"), "", R.drawable.ic_new_colorbar, "", listOf("Women")),
            Store("paytm_train", "Paytm train", "https://paytmtrain.com", listOf("Deals"), "", R.drawable.ic_new_paytm_train, "", listOf()),
            Store("avast", "Avast", "https://avast.com", listOf("Electronics"), "", R.drawable.ic_new_avast, "", listOf()),
            Store("jet_airways", "Jet Airways", "https://jetairways.com", listOf("Deals"), "", R.drawable.ic_new_jet_airways, "", listOf()),
            Store("vistara", "Vistara", "https://vistara.com", listOf("Deals"), "", R.drawable.ic_new_vistara, "", listOf()),
            Store("irctc", "IRCTC", "https://irctc.co.in", listOf("Deals"), "", R.drawable.ic_new_irctc, "", listOf()),
            Store("railyatri", "RailYatri", "https://railyatri.in", listOf("Deals"), "", R.drawable.ic_new_railyatri, "", listOf()),
            Store("snitch", "Snitch", "https://snitch.co.in", listOf("Fashion"), "", R.drawable.ic_new_snitch, "", listOf("Men")),
"""

content = content.replace('Store("meesho", "Meesho", "https://meesho.com", listOf("Fashion", "Deals"), "", R.drawable.ic_new_meesho, "Up to 5%", listOf("Kids"))', 
                          'Store("meesho", "Meesho", "https://meesho.com", listOf("Fashion", "Deals"), "", R.drawable.ic_new_meesho, "Up to 5%", listOf("Kids")),' + new_stores)

with open(file_path, "w", encoding="utf-8") as f:
    f.write(content)

print("Patched MainActivity.kt successfully!")

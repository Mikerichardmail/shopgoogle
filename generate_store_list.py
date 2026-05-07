master_list = '''Amazon, Flipkart, Myntra, Nykaa, AJIO, Mamaearth, OnePlus, Realme, Oppo, Croma, Reliance Digital, Boat, Fire-Boltt, Noise, HealthKart, MuscleBlaze, Nutrabay, HK Vitals, GNC, TrueBasics, True Elements, Netmeds, Truemeds, PharmEasy, Kapiva, Puma, Adidas, Levi's, Uniqlo, Libas, Clovia, Blackberrys, Neemans, Rigo, XYXX, Bewakoof, Shopsy, Tata CLiQ, Pepperfry, Godrej Interio, Havells, Nippon Paint, FirstCry, IGP, SUGAR, WOW, The Derma Co, Plum, Dot & Key, Aqualogica, Foxtale, mCaffeine, Lotus Botanicals, Forest Essentials, Kama Ayurveda, Swiss Beauty, Ustraa, Sephora, Biba, Lenskart, Meesho'''.split(', ')

women = '''Nykaa, Myntra, AJIO, Mamaearth, Sephora, Biba, Plum, The Derma Co, SUGAR, WOW, Clovia'''.split(', ')
men = '''Amazon, Flipkart, Puma, Adidas, Levi's, Boat, OnePlus, Realme, Ustraa, Myntra, AJIO'''.split(', ')
kids = '''FirstCry, Amazon, Flipkart, Meesho'''.split(', ')

electronics = '''Amazon, Flipkart, OnePlus, Realme, Oppo, Croma, Boat'''.split(', ')
beauty = '''Nykaa, Mamaearth, Plum, The Derma Co, SUGAR, WOW, mCaffeine'''.split(', ')
fashion = '''Myntra, AJIO, Puma, Adidas, Levi's, Zara'''.split(', ')
health = '''HealthKart, MuscleBlaze, Nutrabay, Netmeds, PharmEasy'''.split(', ')
home = '''Pepperfry, Godrej Interio, Havells'''.split(', ')
deals = '''Amazon, Flipkart, Myntra, Nykaa, Boat'''.split(', ')

out = []
for s in master_list:
    tabs = []
    if s in women: tabs.append('Women')
    if s in men: tabs.append('Men')
    if s in kids: tabs.append('Kids')
    cats = []
    if s in electronics: cats.append('Electronics')
    if s in beauty: cats.append('Beauty')
    if s in fashion: cats.append('Fashion')
    if s in health: cats.append('Health')
    if s in home: cats.append('Home')
    if s in deals: cats.append('Deals')
    
    id_s = s.lower().replace(' ', '_').replace('&', '').replace('-', '_').replace('\'', '')
    id_s = ' '.join(id_s.split())
    out.append(f'Store("{id_s}", "{s}", "https://{id_s}.com", listOf({", ".join(f"{repr(c)}" for c in cats)}), "", R.drawable.ic_launcher_foreground, "", listOf({", ".join(f"{repr(t)}" for t in tabs)}))')

print('listOf(' + ',\n            '.join(out).replace("'", '"') + ')')

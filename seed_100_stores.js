const SUPABASE_URL = "https://fwhzasbjexillgfrvksx.supabase.co"; 
const SUPABASE_ANON_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImZ3aHphc2JqZXhpbGxnZnJ2a3N4Iiwicm9sZSI6ImFub24iLCJpYXQiOjE3NzY0Mzk5NzksImV4cCI6MjA5MjAxNTk3OX0.MfZPPcx4d7OkAo56emiRjF9FabceUweCVJqv48tXAv4";

const stores = [
  // E-commerce / Marketplaces
  { name: 'Amazon India', domain: 'amazon.in', category: 'E-commerce', logo_url: 'https://logo.clearbit.com/amazon.in' },
  { name: 'Flipkart', domain: 'flipkart.com', category: 'E-commerce', logo_url: 'https://logo.clearbit.com/flipkart.com' },
  { name: 'Tata CLiQ', domain: 'tatacliq.com', category: 'E-commerce', logo_url: 'https://logo.clearbit.com/tatacliq.com' },
  { name: 'JioMart', domain: 'jiomart.com', category: 'E-commerce', logo_url: 'https://logo.clearbit.com/jiomart.com' },
  { name: 'Snapdeal', domain: 'snapdeal.com', category: 'E-commerce', logo_url: 'https://logo.clearbit.com/snapdeal.com' },
  { name: 'Meesho', domain: 'meesho.com', category: 'E-commerce', logo_url: 'https://logo.clearbit.com/meesho.com' },
  { name: 'Shopclues', domain: 'shopclues.com', category: 'E-commerce', logo_url: 'https://logo.clearbit.com/shopclues.com' },
  { name: 'Paytm Mall', domain: 'paytmmall.com', category: 'E-commerce', logo_url: 'https://logo.clearbit.com/paytmmall.com' },

  // Fashion / Apparel
  { name: 'Myntra', domain: 'myntra.com', category: 'Fashion', logo_url: 'https://logo.clearbit.com/myntra.com' },
  { name: 'Ajio', domain: 'ajio.com', category: 'Fashion', logo_url: 'https://logo.clearbit.com/ajio.com' },
  { name: 'Nykaa Fashion', domain: 'nykaafashion.com', category: 'Fashion', logo_url: 'https://logo.clearbit.com/nykaafashion.com' },
  { name: 'Biba', domain: 'biba.in', category: 'Fashion', logo_url: 'https://logo.clearbit.com/biba.in' },
  { name: 'W for Woman', domain: 'wforwoman.com', category: 'Fashion', logo_url: 'https://logo.clearbit.com/wforwoman.com' },
  { name: 'FabIndia', domain: 'fabindia.com', category: 'Fashion', logo_url: 'https://logo.clearbit.com/fabindia.com' },
  { name: 'H&M India', domain: 'hm.com', category: 'Fashion', logo_url: 'https://logo.clearbit.com/hm.com' },
  { name: 'Zara India', domain: 'zara.com', category: 'Fashion', logo_url: 'https://logo.clearbit.com/zara.com' },
  { name: 'Marks & Spencer', domain: 'marksandspencer.in', category: 'Fashion', logo_url: 'https://logo.clearbit.com/marksandspencer.in' },
  { name: 'Lifestyle Stores', domain: 'lifestylestores.com', category: 'Fashion', logo_url: 'https://logo.clearbit.com/lifestylestores.com' },
  { name: 'Shoppers Stop', domain: 'shoppersstop.com', category: 'Fashion', logo_url: 'https://logo.clearbit.com/shoppersstop.com' },
  { name: 'Pantaloons', domain: 'pantaloons.com', category: 'Fashion', logo_url: 'https://logo.clearbit.com/pantaloons.com' },
  { name: 'Max Fashion', domain: 'maxfashion.in', category: 'Fashion', logo_url: 'https://logo.clearbit.com/maxfashion.in' },
  { name: 'Clovia', domain: 'clovia.com', category: 'Fashion', logo_url: 'https://logo.clearbit.com/clovia.com' },
  { name: 'Zivame', domain: 'zivame.com', category: 'Fashion', logo_url: 'https://logo.clearbit.com/zivame.com' },
  { name: 'Nykd', domain: 'nykd.com', category: 'Fashion', logo_url: 'https://logo.clearbit.com/nykd.com' },
  { name: 'XYXX', domain: 'xyxxcrew.com', category: 'Fashion', logo_url: 'https://logo.clearbit.com/xyxxcrew.com' },
  { name: 'Bewakoof', domain: 'bewakoof.com', category: 'Fashion', logo_url: 'https://logo.clearbit.com/bewakoof.com' },
  { name: 'Snitch', domain: 'snitch.co.in', category: 'Fashion', logo_url: 'https://logo.clearbit.com/snitch.co.in' },
  { name: 'The Souled Store', domain: 'thesouledstore.com', category: 'Fashion', logo_url: 'https://logo.clearbit.com/thesouledstore.com' },

  // Beauty / Personal Care
  { name: 'Nykaa', domain: 'nykaa.com', category: 'Beauty', logo_url: 'https://logo.clearbit.com/nykaa.com' },
  { name: 'Purplle', domain: 'purplle.com', category: 'Beauty', logo_url: 'https://logo.clearbit.com/purplle.com' },
  { name: 'Mamaearth', domain: 'mamaearth.in', category: 'Beauty', logo_url: 'https://logo.clearbit.com/mamaearth.in' },
  { name: 'Wow Skin Science', domain: 'buywow.in', category: 'Beauty', logo_url: 'https://logo.clearbit.com/buywow.in' },
  { name: 'Plum Goodness', domain: 'plumgoodness.com', category: 'Beauty', logo_url: 'https://logo.clearbit.com/plumgoodness.com' },
  { name: 'Sugar Cosmetics', domain: 'sugarcosmetics.com', category: 'Beauty', logo_url: 'https://logo.clearbit.com/sugarcosmetics.com' },
  { name: 'Man Matters', domain: 'manmatters.com', category: 'Beauty', logo_url: 'https://logo.clearbit.com/manmatters.com' },
  { name: 'Beardo', domain: 'beardo.in', category: 'Beauty', logo_url: 'https://logo.clearbit.com/beardo.in' },
  { name: 'The Man Company', domain: 'themancompany.com', category: 'Beauty', logo_url: 'https://logo.clearbit.com/themancompany.com' },
  { name: 'Bombay Shaving Company', domain: 'bombayshavingcompany.com', category: 'Beauty', logo_url: 'https://logo.clearbit.com/bombayshavingcompany.com' },
  { name: 'Ustraa', domain: 'ustraa.com', category: 'Beauty', logo_url: 'https://logo.clearbit.com/ustraa.com' },
  { name: 'Kapiva', domain: 'kapiva.in', category: 'Beauty', logo_url: 'https://logo.clearbit.com/kapiva.in' },
  { name: 'mCaffeine', domain: 'mcaffeine.com', category: 'Beauty', logo_url: 'https://logo.clearbit.com/mcaffeine.com' },
  { name: 'BBlunt', domain: 'bblunt.com', category: 'Beauty', logo_url: 'https://logo.clearbit.com/bblunt.com' },

  // Electronics
  { name: 'Reliance Digital', domain: 'reliancedigital.in', category: 'Electronics', logo_url: 'https://logo.clearbit.com/reliancedigital.in' },
  { name: 'Croma', domain: 'croma.com', category: 'Electronics', logo_url: 'https://logo.clearbit.com/croma.com' },
  { name: 'Dell India', domain: 'dell.com', category: 'Electronics', logo_url: 'https://logo.clearbit.com/dell.com' },
  { name: 'Lenovo India', domain: 'lenovo.com', category: 'Electronics', logo_url: 'https://logo.clearbit.com/lenovo.com' },
  { name: 'HP India', domain: 'hp.com', category: 'Electronics', logo_url: 'https://logo.clearbit.com/hp.com' },
  { name: 'Apple India', domain: 'apple.com', category: 'Electronics', logo_url: 'https://logo.clearbit.com/apple.com' },
  { name: 'Samsung India', domain: 'samsung.com', category: 'Electronics', logo_url: 'https://logo.clearbit.com/samsung.com' },
  { name: 'OnePlus India', domain: 'oneplus.in', category: 'Electronics', logo_url: 'https://logo.clearbit.com/oneplus.in' },
  { name: 'Xiaomi India', domain: 'mi.com', category: 'Electronics', logo_url: 'https://logo.clearbit.com/mi.com' },
  { name: 'Realme India', domain: 'realme.com', category: 'Electronics', logo_url: 'https://logo.clearbit.com/realme.com' },
  { name: 'Vivo India', domain: 'vivo.com', category: 'Electronics', logo_url: 'https://logo.clearbit.com/vivo.com' },
  { name: 'Oppo India', domain: 'oppo.com', category: 'Electronics', logo_url: 'https://logo.clearbit.com/oppo.com' },
  { name: 'Boat', domain: 'boat-lifestyle.com', category: 'Electronics', logo_url: 'https://logo.clearbit.com/boat-lifestyle.com' },
  { name: 'Noise', domain: 'gonoise.com', category: 'Electronics', logo_url: 'https://logo.clearbit.com/gonoise.com' },
  { name: 'Boult Audio', domain: 'boultaudio.com', category: 'Electronics', logo_url: 'https://logo.clearbit.com/boultaudio.com' },
  { name: 'Fire-Boltt', domain: 'fireboltt.com', category: 'Electronics', logo_url: 'https://logo.clearbit.com/fireboltt.com' },

  // Travel / Flight
  { name: 'MakeMyTrip', domain: 'makemytrip.com', category: 'Travel', logo_url: 'https://logo.clearbit.com/makemytrip.com' },
  { name: 'Cleartrip', domain: 'cleartrip.com', category: 'Travel', logo_url: 'https://logo.clearbit.com/cleartrip.com' },
  { name: 'Goibibo', domain: 'goibibo.com', category: 'Travel', logo_url: 'https://logo.clearbit.com/goibibo.com' },
  { name: 'Yatra', domain: 'yatra.com', category: 'Travel', logo_url: 'https://logo.clearbit.com/yatra.com' },
  { name: 'EaseMyTrip', domain: 'easemytrip.com', category: 'Travel', logo_url: 'https://logo.clearbit.com/easemytrip.com' },
  { name: 'Abhibus', domain: 'abhibus.com', category: 'Travel', logo_url: 'https://logo.clearbit.com/abhibus.com' },
  { name: 'Redbus', domain: 'redbus.in', category: 'Travel', logo_url: 'https://logo.clearbit.com/redbus.in' },
  { name: 'Oyo Rooms', domain: 'oyorooms.com', category: 'Travel', logo_url: 'https://logo.clearbit.com/oyorooms.com' },
  { name: 'Airbnb India', domain: 'airbnb.co.in', category: 'Travel', logo_url: 'https://logo.clearbit.com/airbnb.co.in' },
  { name: 'Agoda', domain: 'agoda.com', category: 'Travel', logo_url: 'https://logo.clearbit.com/agoda.com' },
  { name: 'Booking.com', domain: 'booking.com', category: 'Travel', logo_url: 'https://logo.clearbit.com/booking.com' },
  { name: 'Ixigo', domain: 'ixigo.com', category: 'Travel', logo_url: 'https://logo.clearbit.com/ixigo.com' },

  // Food / Grocery
  { name: 'Zomato', domain: 'zomato.com', category: 'Food & Grocery', logo_url: 'https://logo.clearbit.com/zomato.com' },
  { name: 'Swiggy', domain: 'swiggy.com', category: 'Food & Grocery', logo_url: 'https://logo.clearbit.com/swiggy.com' },
  { name: 'Dominos India', domain: 'dominos.co.in', category: 'Food & Grocery', logo_url: 'https://logo.clearbit.com/dominos.co.in' },
  { name: 'Pizza Hut India', domain: 'pizzahut.co.in', category: 'Food & Grocery', logo_url: 'https://logo.clearbit.com/pizzahut.co.in' },
  { name: 'BigBasket', domain: 'bigbasket.com', category: 'Food & Grocery', logo_url: 'https://logo.clearbit.com/bigbasket.com' },
  { name: 'Blinkit', domain: 'blinkit.com', category: 'Food & Grocery', logo_url: 'https://logo.clearbit.com/blinkit.com' },
  { name: 'Zepto', domain: 'zeptonow.com', category: 'Food & Grocery', logo_url: 'https://logo.clearbit.com/zeptonow.com' },
  { name: 'EatFit', domain: 'eatfit.in', category: 'Food & Grocery', logo_url: 'https://logo.clearbit.com/eatfit.in' },
  { name: 'Licious', domain: 'licious.in', category: 'Food & Grocery', logo_url: 'https://logo.clearbit.com/licious.in' },
  { name: 'FreshToHome', domain: 'freshtohome.com', category: 'Food & Grocery', logo_url: 'https://logo.clearbit.com/freshtohome.com' },

  // Pharmacy / Health
  { name: '1mg', domain: '1mg.com', category: 'Health', logo_url: 'https://logo.clearbit.com/1mg.com' },
  { name: 'Netmeds', domain: 'netmeds.com', category: 'Health', logo_url: 'https://logo.clearbit.com/netmeds.com' },
  { name: 'PharmEasy', domain: 'pharmeasy.in', category: 'Health', logo_url: 'https://logo.clearbit.com/pharmeasy.in' },
  { name: 'Apollo Pharmacy', domain: 'apollopharmacy.in', category: 'Health', logo_url: 'https://logo.clearbit.com/apollopharmacy.in' },
  { name: 'Healthkart', domain: 'healthkart.com', category: 'Health', logo_url: 'https://logo.clearbit.com/healthkart.com' },

  // Home / Furniture
  { name: 'Pepperfry', domain: 'pepperfry.com', category: 'Home & Furniture', logo_url: 'https://logo.clearbit.com/pepperfry.com' },
  { name: 'Urban Ladder', domain: 'urbanladder.com', category: 'Home & Furniture', logo_url: 'https://logo.clearbit.com/urbanladder.com' },
  { name: 'IKEA India', domain: 'ikea.com', category: 'Home & Furniture', logo_url: 'https://logo.clearbit.com/ikea.com' },
  { name: 'Wooden Street', domain: 'woodenstreet.com', category: 'Home & Furniture', logo_url: 'https://logo.clearbit.com/woodenstreet.com' },
  { name: 'Wakefit', domain: 'wakefit.co', category: 'Home & Furniture', logo_url: 'https://logo.clearbit.com/wakefit.co' },
  { name: 'SleepyCat', domain: 'sleepycat.in', category: 'Home & Furniture', logo_url: 'https://logo.clearbit.com/sleepycat.in' },

  // Footwear / Sports
  { name: 'Nike India', domain: 'nike.com', category: 'Sports & Footwear', logo_url: 'https://logo.clearbit.com/nike.com' },
  { name: 'Adidas India', domain: 'adidas.co.in', category: 'Sports & Footwear', logo_url: 'https://logo.clearbit.com/adidas.co.in' },
  { name: 'Puma India', domain: 'in.puma.com', category: 'Sports & Footwear', logo_url: 'https://logo.clearbit.com/in.puma.com' },
  { name: 'Reebok India', domain: 'reebok.in', category: 'Sports & Footwear', logo_url: 'https://logo.clearbit.com/reebok.in' },
  { name: 'Decathlon India', domain: 'decathlon.in', category: 'Sports & Footwear', logo_url: 'https://logo.clearbit.com/decathlon.in' },
  { name: 'Cult.fit', domain: 'cult.fit', category: 'Sports & Footwear', logo_url: 'https://logo.clearbit.com/cult.fit' },
  { name: 'Bata India', domain: 'bata.in', category: 'Sports & Footwear', logo_url: 'https://logo.clearbit.com/bata.in' },
  { name: 'Metro Shoes', domain: 'metroshoes.com', category: 'Sports & Footwear', logo_url: 'https://logo.clearbit.com/metroshoes.com' },

  // Others / Accessories / Gifting
  { name: 'Lenskart', domain: 'lenskart.com', category: 'Accessories', logo_url: 'https://logo.clearbit.com/lenskart.com' },
  { name: 'Titan', domain: 'titan.co.in', category: 'Accessories', logo_url: 'https://logo.clearbit.com/titan.co.in' },
  { name: 'FirstCry', domain: 'firstcry.com', category: 'Baby & Kids', logo_url: 'https://logo.clearbit.com/firstcry.com' },
  { name: 'Ferns N Petals', domain: 'fnp.com', category: 'Gifting', logo_url: 'https://logo.clearbit.com/fnp.com' },
  { name: 'IGP', domain: 'igp.com', category: 'Gifting', logo_url: 'https://logo.clearbit.com/igp.com' },
  { name: 'Floweraura', domain: 'floweraura.com', category: 'Gifting', logo_url: 'https://logo.clearbit.com/floweraura.com' },
  { name: 'Vistaprint', domain: 'vistaprint.in', category: 'Gifting', logo_url: 'https://logo.clearbit.com/vistaprint.in' },
  { name: 'GIVA', domain: 'giva.co', category: 'Jewelry', logo_url: 'https://logo.clearbit.com/giva.co' },
  { name: 'CaratLane', domain: 'caratlane.com', category: 'Jewelry', logo_url: 'https://logo.clearbit.com/caratlane.com' },
  { name: 'Melorra', domain: 'melorra.com', category: 'Jewelry', logo_url: 'https://logo.clearbit.com/melorra.com' },
  { name: 'Blue Tokai', domain: 'bluetokaicoffee.com', category: 'Food & Beverage', logo_url: 'https://logo.clearbit.com/bluetokaicoffee.com' },
  { name: 'Sleepy Owl', domain: 'sleepyowl.co', category: 'Food & Beverage', logo_url: 'https://logo.clearbit.com/sleepyowl.co' },
  { name: 'Phool', domain: 'phool.co', category: 'Gifting', logo_url: 'https://logo.clearbit.com/phool.co' },

  // Entertainment / Booking
  { name: 'BookMyShow', domain: 'in.bookmyshow.com', category: 'Entertainment', logo_url: 'https://logo.clearbit.com/in.bookmyshow.com' }
];

async function seedData() {
    console.log(`Starting data seed to Supabase... (Total: ${stores.length} stores)`);
    let insertedCount = 0;
    
    for (const store of stores) {
        // Attempt to insert
        let res = await fetch(`${SUPABASE_URL}/rest/v1/stores`, {
            method: 'POST',
            headers: {
                'apikey': SUPABASE_ANON_KEY,
                'Authorization': `Bearer ${SUPABASE_ANON_KEY}`,
                'Content-Type': 'application/json',
                'Prefer': 'return=representation'
            },
            body: JSON.stringify(store)
        });
        
        let responseJson;
        if (!res.ok) {
            const errBody = await res.json();
            // If conflict (domain unique constraint), it's already there
            if (errBody.code === '23505') {
               console.log(`Store ${store.domain} already exists. Skipping.`);
               continue;
            } else {
               console.error(`Failed to insert store ${store.domain}`, errBody);
               continue;
            }
        } else {
            responseJson = await res.json();
            console.log(`Inserted store: ${store.domain}`);
            insertedCount++;
        }
    }
    
    console.log(`\nDONE! Successfully inserted ${insertedCount} new Indian stores.`);
}

seedData().catch(console.error);

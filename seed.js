const SUPABASE_URL = "https://fwhzasbjexillgfrvksx.supabase.co"; 
const SUPABASE_ANON_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImZ3aHphc2JqZXhpbGxnZnJ2a3N4Iiwicm9sZSI6ImFub24iLCJpYXQiOjE3NzY0Mzk5NzksImV4cCI6MjA5MjAxNTk3OX0.MfZPPcx4d7OkAo56emiRjF9FabceUweCVJqv48tXAv4";

const stores = [
    { name: "Ajio", domain: "ajio.com" },
    { name: "Amazon India", domain: "amazon.in" },
    { name: "Flipkart", domain: "flipkart.com" },
    { name: "Myntra", domain: "myntra.com" },
    { name: "Nykaa", domain: "nykaa.com" },
    { name: "TataCLiQ", domain: "tatacliq.com" }
];

const mockCoupons = {
    "ajio.com": [
        { code: "SAVE500", title: "₹500 Off on orders above ₹1499", success_score: 82 },
        { code: "NEW20", title: "20% Off for new users", success_score: 75 },
        { code: "FREEDEL", title: "Free Delivery on fashion", success_score: 95 },
        { code: "AJIO10", title: "Extra 10% on prepaid orders", success_score: 60 }
    ],
    "amazon.in": [
        { code: "HDFC10", title: "10% Instant Discount on HDFC Cards", success_score: 90 },
        { code: "AMZ100", title: "Flat ₹100 Cashback on UPI", success_score: 85 },
        { code: "FRESH50", title: "₹50 Off on Amazon Fresh", success_score: 70 }
    ],
    "flipkart.com": [
        { code: "BBD24", title: "Big Billion Days Special offer", success_score: 88 },
        { code: "AXIS5", title: "5% Unlimited Cashback on Axis", success_score: 92 },
        { code: "FLIP10", title: "10% Off on Groceries", success_score: 65 }
    ],
    "myntra.com": [
        { code: "MYNTRA20", title: "Flat 20% Off on Apparel", success_score: 80 },
        { code: "FIRST10", title: "10% Off on first order", success_score: 90 },
        { code: "FLAT300", title: "₹300 Off on ₹1999+", success_score: 76 }
    ],
    "nykaa.com": [
        { code: "BEAUTY15", title: "15% Off Cosmetics", success_score: 85 },
        { code: "NYKNEW", title: "₹200 Off for New Customers", success_score: 95 }
    ],
    "tatacliq.com": [
        { code: "CLIQ500", title: "Flat ₹500 Off", success_score: 78 },
        { code: "TATA20", title: "20% off on electronics", success_score: 88 }
    ]
};

async function seedData() {
    console.log("Starting data seed to Supabase...");
    let insertedCount = 0;
    
    for (const store of stores) {
        console.log(`Processing Store: ${store.domain}`);
        
        // Insert Store and Upsert implicitly handled in standard fetch via ignoring errors
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
        
        if (!res.ok) {
            console.error(`Failed to insert store ${store.domain}`, await res.text());
            continue;
        }
        
        const storeResponse = await res.json();
        const storeId = storeResponse[0].id;
        
        const couponsToInsert = mockCoupons[store.domain];
        if (couponsToInsert) {
            for (const c of couponsToInsert) {
                const payload = {
                    store_id: storeId,
                    code: c.code,
                    title: c.title,
                    success_score: c.success_score,
                    status: 'active'
                };
                
                let cropRes = await fetch(`${SUPABASE_URL}/rest/v1/coupons`, {
                    method: 'POST',
                    headers: {
                        'apikey': SUPABASE_ANON_KEY,
                        'Authorization': `Bearer ${SUPABASE_ANON_KEY}`,
                        'Content-Type': 'application/json'
                    },
                    body: JSON.stringify(payload)
                });
                
                if (cropRes.ok) insertedCount++;
            }
        }
    }
    console.log(`\nDONE! Inserted ${insertedCount} coupons successfully into the live Supabase.`);
}

seedData();

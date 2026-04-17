// --- SUPABASE CONFIGURATION ---
const SUPABASE_URL = "https://fwhzasbjexillgfrvksx.supabase.co"; 
const SUPABASE_ANON_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImZ3aHphc2JqZXhpbGxnZnJ2a3N4Iiwicm9sZSI6ImFub24iLCJpYXQiOjE3NzY0Mzk5NzksImV4cCI6MjA5MjAxNTk3OX0.MfZPPcx4d7OkAo56emiRjF9FabceUweCVJqv48tXAv4";
const USE_REAL_BACKEND = true; // Toggle this to true once you add your keys above

chrome.runtime.onInstalled.addListener(() => {
    // Initialize default local storage schema
    chrome.storage.local.get(null, (data) => {
        const defaultStorage = {
            enabled: true,
            theme: "light",
            disabledSites: [],
            couponCache: {},
            lastShown: {},
            cooldowns: {}
        };
        const newData = { ...defaultStorage, ...data };
        chrome.storage.local.set(newData);
        console.log("Extension installed and storage initialized.");
    });
});

// Function to check and update cache
const CACHE_DURATION_MS = 6 * 60 * 60 * 1000; // 6 hours

async function getCouponsForDomain(domain) {
    return new Promise((resolve) => {
        chrome.storage.local.get(['couponCache'], (result) => {
            const cache = result.couponCache || {};
            const siteCache = cache[domain];
            
            const now = Date.now();
            
            // Return cached if valid
            if (siteCache && siteCache.timestamp && (now - siteCache.timestamp < CACHE_DURATION_MS)) {
                console.log("Serving coupons from cache for", domain);
                return resolve(siteCache.data);
            }
            
            if (USE_REAL_BACKEND && SUPABASE_URL !== "YOUR_SUPABASE_PROJECT_URL") {
                console.log("Fetching coupons from Supabase DB for", domain);
                fetch(`${SUPABASE_URL}/rest/v1/coupons?select=*,stores!inner(domain)&stores.domain=eq.${domain}&status=eq.active&order=success_score.desc`, {
                    headers: {
                        'apikey': SUPABASE_ANON_KEY,
                        'Authorization': `Bearer ${SUPABASE_ANON_KEY}`
                    }
                })
                .then(res => res.json())
                .then(data => {
                    cache[domain] = { timestamp: now, data: data };
                    chrome.storage.local.set({ couponCache: cache }, () => resolve(data));
                })
                .catch(err => {
                    console.error("Supabase Error:", err);
                    resolve([]); // graceful degrade 
                });
                return;
            }

            // Fallback: Local "Mock" database
            console.log("Fetching new coupons for", domain);
            const mockCoupons = {
                "ajio.com": [
                    {id: "aj1", code: "SAVE500", title: "₹500 Off on orders above ₹1499", score: 82},
                    {id: "aj2", code: "NEW20", title: "20% Off for new users", score: 75},
                    {id: "aj3", code: "FREEDEL", title: "Free Delivery on fashion", score: 95},
                    {id: "aj4", code: "AJIO10", title: "Extra 10% on prepaid orders", score: 60}
                ],
                "amazon.in": [
                    {id: "am1", code: "HDFC10", title: "10% Instant Discount on HDFC Cards", score: 90},
                    {id: "am2", code: "AMZ100", title: "Flat ₹100 Cashback on UPI", score: 85},
                    {id: "am3", code: "FRESH50", title: "₹50 Off on Amazon Fresh", score: 70}
                ],
                "flipkart.com": [
                    {id: "fk1", code: "BBD24", title: "Big Billion Days Special offer", score: 88},
                    {id: "fk2", code: "AXIS5", title: "5% Unlimited Cashback on Axis", score: 92},
                    {id: "fk3", code: "FLIP10", title: "10% Off on Groceries", score: 65}
                ],
                "myntra.com": [
                    {id: "my1", code: "MYNTRA20", title: "Flat 20% Off on Apparel", score: 80},
                    {id: "my2", code: "FIRST10", title: "10% Off on first order", score: 90},
                    {id: "my3", code: "FLAT300", title: "₹300 Off on ₹1999+", score: 76}
                ],
                "nykaa.com": [
                    {id: "ny1", code: "BEAUTY15", title: "15% Off Cosmetics", score: 85},
                    {id: "ny2", code: "NYKNEW", title: "₹200 Off for New Customers", score: 95}
                ],
                "tatacliq.com": [
                    {id: "tc1", code: "CLIQ500", title: "Flat ₹500 Off", score: 78},
                    {id: "tc2", code: "TATA20", title: "20% off on electronics", score: 88}
                ]
            };
            
            const freshCoupons = mockCoupons[domain] || [];
            
            // Save to cache
            cache[domain] = {
                timestamp: now,
                data: freshCoupons
            };
            
            chrome.storage.local.set({ couponCache: cache }, () => {
                resolve(freshCoupons);
            });
        });
    });
}

// Listen for messages from content scripts or popups
chrome.runtime.onMessage.addListener((message, sender, sendResponse) => {
    console.log("Received message:", message);
    
    if (message.action === 'fetchCoupons') {
        const domain = message.domain;
        getCouponsForDomain(domain).then(coupons => {
            sendResponse({ success: true, coupons });
        });
        
        // Required for async sendResponse
        return true; 
    }
    
    if (message.action === 'voteCoupon') {
        const { id, vote } = message;
        console.log(`Vote received for coupon ${id}: ${vote}`);
        // In the future: Send this vote to Supabase/API
        sendResponse({ success: true });
        return false;
    }
    
    if (message.action === 'triggerNotification') {
        const { title, message: body } = message;
        chrome.notifications.create({
            type: 'basic',
            iconUrl: 'assets/icon128.png', 
            title: title,
            message: body,
            priority: 2
        });
        sendResponse({ success: true });
        return false;
    }
    
    if (message.action === 'submitCoupon') {
        const { store, code, title } = message;
        if (USE_REAL_BACKEND && SUPABASE_URL !== "YOUR_SUPABASE_PROJECT_URL") {
            fetch(`${SUPABASE_URL}/rest/v1/submissions`, {
                method: 'POST',
                headers: {
                    'apikey': SUPABASE_ANON_KEY,
                    'Authorization': `Bearer ${SUPABASE_ANON_KEY}`,
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({ store_domain: store, code: code, title: title, status: 'pending' })
            }).then(() => sendResponse({ success: true }))
              .catch(err => {
                  console.error("Submission Error:", err);
                  sendResponse({ success: false });
              });
            return true; // Keep message channel open for async
        } else {
            console.log("Mock Submission received:", store, code, title);
            sendResponse({ success: true });
            return false;
        }
    }
});

const fs = require('fs');

const SUPABASE_URL = "https://fwhzasbjexillgfrvksx.supabase.co"; 
const SUPABASE_ANON_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImZ3aHphc2JqZXhpbGxnZnJ2a3N4Iiwicm9sZSI6ImFub24iLCJpYXQiOjE3NzY0Mzk5NzksImV4cCI6MjA5MjAxNTk3OX0.MfZPPcx4d7OkAo56emiRjF9FabceUweCVJqv48tXAv4";

async function run() {
    console.log("Starting safe affiliate link update...");
    
    const text = fs.readFileSync('../links.txt', 'utf-8');
    const lines = text.split('\n').map(l => l.trim()).filter(l => l.length > 0);
    
    let affiliateMap = {};
    
    // Parse the file safely
    for (let i = 0; i < lines.length; i++) {
        let line = lines[i];
        
        // Exclude headers
        if (line.includes('Mobiles') || line.includes('Beauty') || line.includes('Health') || line.includes('Fashion') || line.includes('Home')) {
            continue;
        }

        if (line.includes('http')) {
            // Check for format: Store -> Link or Store - Link
            let match = line.match(/(.*?)(?:→|-|–|—)\s*(https?:\/\/[^\s]+)/);
            if (match) {
                let name = match[1].trim();
                let link = match[2].trim();
                if (name) affiliateMap[name.toLowerCase()] = link;
            } else if (i > 0) {
                // Check format: Line 1: Store, Line 2: Link
                let prevLine = lines[i-1];
                if (!prevLine.includes('http')) {
                    // Clean previous line to be just letters/numbers
                    let name = prevLine.replace(/[^a-zA-Z0-9\s]/g, '').trim().toLowerCase();
                    if (name) affiliateMap[name] = line;
                }
            }
        }
    }
    
    console.log(`Parsed ${Object.keys(affiliateMap).length} clean affiliate pairs from text.`);
    
    // Fetch stores
    let res = await fetch(`${SUPABASE_URL}/rest/v1/stores?select=id,name,domain`, {
        headers: {
            'apikey': SUPABASE_ANON_KEY,
            'Authorization': `Bearer ${SUPABASE_ANON_KEY}`
        }
    });

    if (!res.ok) {
        console.error("Failed to connect to Supabase");
        return;
    }

    let stores = await res.json();
    let updatedCount = 0;
    
    for (const store of stores) {
        let targetLink = null;
        let sName = store.name.toLowerCase();
        
        if (affiliateMap[sName]) {
            targetLink = affiliateMap[sName];
        } else {
             // Fallback partial match
            for (let [key, val] of Object.entries(affiliateMap)) {
                if (sName.includes(key) || key.includes(sName)) {
                    targetLink = val;
                    break;
                }
            }
        }
        
        if (targetLink) {
            console.log(`Matching: ${store.name} => ${targetLink}`);
            let updateRes = await fetch(`${SUPABASE_URL}/rest/v1/stores?id=eq.${store.id}`, {
                method: 'PATCH',
                headers: {
                    'apikey': SUPABASE_ANON_KEY,
                    'Authorization': `Bearer ${SUPABASE_ANON_KEY}`,
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({ affiliate_url: targetLink })
            });
            
            if (updateRes.ok) {
                updatedCount++;
            }
        }
    }
    
    console.log(`\n✅ Safe update complete. Total stores updated securely with affiliate links: ${updatedCount}`);
}

run().catch(console.error);

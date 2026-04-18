require('dotenv').config();
const axios = require('axios');
const cheerio = require('cheerio');
const { GoogleGenerativeAI } = require('@google/generative-ai');

// --- Configuration ---
const SUPABASE_URL = process.env.SUPABASE_URL || "https://fwhzasbjexillgfrvksx.supabase.co"; 
const SUPABASE_ANON_KEY = process.env.SUPABASE_ANON_KEY || "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImZ3aHphc2JqZXhpbGxnZnJ2a3N4Iiwicm9sZSI6ImFub24iLCJpYXQiOjE3NzY0Mzk5NzksImV4cCI6MjA5MjAxNTk3OX0.MfZPPcx4d7OkAo56emiRjF9FabceUweCVJqv48tXAv4";
const GEMINI_API_KEY = process.env.GEMINI_API_KEY || "YOUR_GEMINI_API_KEY"; // Ensure user sets this in .env

// If user hasn't set Gemini Key, gracefully warn
if (GEMINI_API_KEY === "YOUR_GEMINI_API_KEY") {
    console.warn("⚠️ WARNING: GEMINI_API_KEY is not set in .env! AI Extraction will not work. Continuing with mock data just for testing if needed or will fail at AI step.");
}

const genAI = new GoogleGenerativeAI(GEMINI_API_KEY);

// User-Agent to avoid basic blocks
const headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8'
};

// Utilities
const sleep = ms => new Promise(r => setTimeout(r, ms));

async function fetchStoreDomains() {
    console.log("Fetching stores from Supabase...");
    let res = await fetch(`${SUPABASE_URL}/rest/v1/stores?select=id,domain,name`, {
        headers: {
            'apikey': SUPABASE_ANON_KEY,
            'Authorization': `Bearer ${SUPABASE_ANON_KEY}`
        }
    });

    if (!res.ok) {
        console.error("Failed to fetch stores", await res.text());
        return [];
    }

    return await res.json();
}

async function scrapeCouponPage(storeConfig) {
    // Generate an aggregator URL based on the domain/name
    // Example: GrabOn often uses "storename-coupons"
    const storeSlug = storeConfig.name.toLowerCase().replace(/[^a-z0-9]/g, '');
    const url = `https://www.grabon.in/${storeSlug}-coupons/`;

    console.log(`[${storeConfig.domain}] Scraping ${url}...`);

    try {
        const response = await axios.get(url, { headers, timeout: 10000 });
        const $ = cheerio.load(response.data);
        
        // Remove scripts, styles, nav, footer to save token size
        $('script, style, nav, footer, header').remove();
        
        // Grab remaining visible text
        let rawText = $('body').text().replace(/\s+/g, ' ').trim();
        
        // Truncate to save tokens (e.g., first 10000 characters is usually enough)
        rawText = rawText.substring(0, 10000);
        return rawText;
    } catch (e) {
        console.log(`[${storeConfig.domain}] Scrape failed (might be 404 or blocked). Error: ${e.message}`);
        return null;
    }
}

async function extractCouponsWithAI(rawText, domain) {
    console.log(`[${domain}] Passing raw text to Gemini AI for extraction...`);
    
    const prompt = `
        You are a smart system that extracts shopping coupon codes. 
        I have scraped the webpage for a store (${domain}).
        Extract all the valid coupon/promo codes and their short titles/descriptions from the following text.
        Return ONLY a JSON array with no markdown formatting.
        Format: [{'code': 'STRING', 'title': 'STRING'}]
        If no distinct codes are found, return [].
        Do not include deals that don't have a specific alphanumeric code.
        
        TEXT:
        ${rawText}
    `;

    try {
        const model = genAI.getGenerativeModel({ model: "gemini-1.5-flash" });
        const result = await model.generateContent(prompt);
        let textResult = result.response.text().trim();
        
        // Clean up markdown in case it included ```json ... ```
        if (textResult.startsWith('```json')) textResult = textResult.replace('```json', '');
        if (textResult.startsWith('```')) textResult = textResult.replace('```', '');
        if (textResult.endsWith('```')) textResult = textResult.replace(/```$/, '');

        const parsed = JSON.parse(textResult.trim());
        return Array.isArray(parsed) ? parsed : [];
    } catch (e) {
        console.error(`[${domain}] AI Extraction failed:`, e.message);
        return [];
    }
}

async function getExistingCodes(storeId) {
    let res = await fetch(`${SUPABASE_URL}/rest/v1/coupons?select=code&store_id=eq.${storeId}`, {
        headers: {
            'apikey': SUPABASE_ANON_KEY,
            'Authorization': `Bearer ${SUPABASE_ANON_KEY}`
        }
    });

    if (!res.ok) return [];
    const data = await res.json();
    return data.map(d => d.code.toUpperCase());
}

async function insertNewCoupons(storeId, domain, newCoupons) {
    const existing = await getExistingCodes(storeId);
    
    const toInsert = newCoupons.filter(c => c.code && !existing.includes(c.code.toUpperCase())).map(c => ({
        store_id: storeId,
        code: c.code.toUpperCase(),
        title: c.title,
        status: 'active',
        success_score: 50, // default
        source: 'ai_bot'
    }));

    if (toInsert.length === 0) {
        console.log(`[${domain}] No new unique coupons found to insert.`);
        return;
    }

    // Insert payload
    let res = await fetch(`${SUPABASE_URL}/rest/v1/coupons`, {
        method: 'POST',
        headers: {
            'apikey': SUPABASE_ANON_KEY,
            'Authorization': `Bearer ${SUPABASE_ANON_KEY}`,
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(toInsert)
    });

    if (res.ok) {
        console.log(`[${domain}] ✅ Successfully inserted ${toInsert.length} new coupons!`);
    } else {
        console.error(`[${domain}] ❌ Failed to insert coupons.`, await res.text());
    }
}

async function runPipeline() {
    console.log("🚀 Starting Daily Coupon Scraping Pipeline...");
    
    const stores = await fetchStoreDomains();
    
    // Shuffle all stores randomly so we process different websites every day
    const shuffledStores = stores.sort(() => 0.5 - Math.random());
    
    // SAFETY LIMIT: Cap to 350 random stores so it never runs more than ~45 mins, 
    // keeping it strictly under Github's 2000 free monthly minutes.
    const targetStores = shuffledStores.slice(0, 350);
    
    console.log(`Loaded ${stores.length} total stores. Randomly selected ${targetStores.length} stores to respect free-tier time limits...`);
    
    for (const store of targetStores) {
        if (!store.name) continue;
        
        const rawHtmlText = await scrapeCouponPage(store);
        
        if (rawHtmlText && GEMINI_API_KEY !== "YOUR_GEMINI_API_KEY") {
            const aiExtracted = await extractCouponsWithAI(rawHtmlText, store.domain);
            
            if (aiExtracted.length > 0) {
                console.log(`[${store.domain}] AI found ${aiExtracted.length} valid codes.`);
                await insertNewCoupons(store.id, store.domain, aiExtracted);
            } else {
                console.log(`[${store.domain}] AI did not find any valid string codes.`);
            }
        }
        
        // Wait 3 seconds to avoid aggressively pinging servers
        await sleep(3000);
    }
    
    console.log("🏁 Pipeline Finished!");
}

runPipeline();

require('dotenv').config();
const axios = require('axios');
const cheerio = require('cheerio');
const { GoogleGenerativeAI } = require('@google/generative-ai');
const fs = require('fs');
const path = require('path');

// --- Configuration ---
const SUPABASE_URL = process.env.SUPABASE_URL || "https://fwhzasbjexillgfrvksx.supabase.co"; 
const SUPABASE_ANON_KEY = process.env.SUPABASE_ANON_KEY || "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImZ3aHphc2JqZXhpbGxnZnJ2a3N4Iiwicm9sZSI6ImFub24iLCJpYXQiOjE3NzY0Mzk5NzksImV4cCI6MjA5MjAxNTk3OX0.MfZPPcx4d7OkAo56emiRjF9FabceUweCVJqv48tXAv4";
const GEMINI_API_KEY = process.env.GEMINI_API_KEY || "YOUR_GEMINI_API_KEY"; // Ensure user sets this in .env

// If user hasn't set Gemini Key, gracefully warn
if (GEMINI_API_KEY === "YOUR_GEMINI_API_KEY") {
    console.warn("⚠️ WARNING: GEMINI_API_KEY is not set in .env! AI Extraction will not work. Continuing with mock data just for testing if needed or will fail at AI step.");
}

const genAI = new GoogleGenerativeAI(GEMINI_API_KEY);

const STATE_FILE = path.join(__dirname, 'scraper_state.json');

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
    // Generate potential slugs
    const nameSlug = storeConfig.name ? storeConfig.name.toLowerCase().replace(/[^a-z0-9]/g, '') : '';
    const domainSlug = storeConfig.domain ? storeConfig.domain.split('.')[0].toLowerCase().replace(/[^a-z0-9]/g, '') : '';
    
    // Try multiple GrabOn URL formats sequentially
    const urlsToTry = [
        `https://www.grabon.in/${nameSlug}-coupons/`,
        `https://www.grabon.in/${domainSlug}-coupons/`,
        `https://www.grabon.in/${nameSlug}india-coupons/`,
        `https://www.grabon.in/${domainSlug}india-coupons/`
    ].filter(url => !url.includes('//-coupons')); // Remove empty slugs

    const uniqueUrls = [...new Set(urlsToTry)];

    for (const url of uniqueUrls) {
        console.log(`[${storeConfig.domain}] Scraping ${url}...`);
        try {
            const response = await axios.get(url, { headers, timeout: 10000 });
            const $ = cheerio.load(response.data);
            
            // Remove scripts, styles, nav, footer to save token size
            $('script, style, nav, footer, header').remove();
            let rawText = $('body').text().replace(/\s+/g, ' ').trim();
            
            // Truncate to save tokens (e.g., first 10000 characters is usually enough)
            return rawText.substring(0, 10000);
        } catch (e) {
            // Silently try next URL if 404 not found
            if (e.response && e.response.status === 404) {
                 console.log(`[${storeConfig.domain}] 404 Not Found for ${url}, trying next (if any)...`);
            } else {
                 console.log(`[${storeConfig.domain}] Scrape failed for ${url}. Error: ${e.message}`);
            }
        }
    }
    
    console.log(`[${storeConfig.domain}] ❌ Could not find valid coupon page after trying multiple URLs. Skiping.`);
    return null;
}

async function extractCouponsWithAI(rawText, domain, retries = 3) {
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

    for (let attempt = 1; attempt <= retries; attempt++) {
        try {
            const model = genAI.getGenerativeModel({ model: "gemini-2.5-flash" });
            const result = await model.generateContent(prompt);
            let textResult = result.response.text().trim();
            
            // Clean up markdown in case it included ```json ... ```
            if (textResult.startsWith('```json')) textResult = textResult.replace('```json', '');
            if (textResult.startsWith('```')) textResult = textResult.replace('```', '');
            if (textResult.endsWith('```')) textResult = textResult.replace(/```$/, '');

            const parsed = JSON.parse(textResult.trim());
            return Array.isArray(parsed) ? parsed : [];
        } catch (e) {
            if (e.status === 429 || e.message.includes('429') || e.message.includes('Quota')) {
                console.warn(`[${domain}] Rate limit hit (429). Exiting today's run to respect API quota limits.`);
                throw new Error("RATE_LIMIT");
            } else {
                console.error(`[${domain}] AI Extraction failed:`, e.message);
                return [];
            }
        }
    }
    
    console.error(`[${domain}] Failed up to ${retries} times due to Rate Limits.`);
    return [];
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
    
    // 1. Get State
    let state = { lastProcessedIndex: 0 };
    if (fs.existsSync(STATE_FILE)) {
        try {
            state = JSON.parse(fs.readFileSync(STATE_FILE, 'utf8'));
        } catch (e) { 
            console.error("Could not parse state file, starting from 0"); 
        }
    }
    
    const stores = await fetchStoreDomains();
    if (stores.length === 0) {
        console.log("No stores found in database.");
        return;
    }
    
    // Sort all stores consistently so we can paginate through them day by day
    stores.sort((a, b) => a.id - b.id);
    
    let startIndex = state.lastProcessedIndex;
    if (startIndex >= stores.length) {
        startIndex = 0; // Reset to beginning if we've scanned all domains
    }
    
    // SAFETY LIMIT: Scan 50 websites block per run
    const BATCH_SIZE = 50;
    const targetStores = stores.slice(startIndex, startIndex + BATCH_SIZE);
    
    console.log(`Loaded ${stores.length} total stores. Resuming from index ${startIndex}.`);
    console.log(`Targeting ${targetStores.length} stores for today's scan...`);
    
    let processedCount = 0;

    for (let i = 0; i < targetStores.length; i++) {
        const store = targetStores[i];
        if (!store.name) continue;
        
        processedCount++;
        const rawHtmlText = await scrapeCouponPage(store);
        
        if (rawHtmlText && GEMINI_API_KEY !== "YOUR_GEMINI_API_KEY") {
            try {
                const aiExtracted = await extractCouponsWithAI(rawHtmlText, store.domain);
                
                if (aiExtracted.length > 0) {
                    console.log(`[${store.domain}] AI found ${aiExtracted.length} valid codes.`);
                    await insertNewCoupons(store.id, store.domain, aiExtracted);
                } else {
                    console.log(`[${store.domain}] AI did not find any valid string codes.`);
                }
            } catch (err) {
                if (err.message === "RATE_LIMIT") {
                    console.log("🛑 Rate Limit encountered. Saving progress and pausing pipeline until the next run.");
                    state.lastProcessedIndex = startIndex + i;
                    fs.writeFileSync(STATE_FILE, JSON.stringify(state, null, 2));
                    console.log("Current state saved. Exiting gracefully.");
                    process.exit(0);
                }
                console.error(`Error processing ${store.domain}:`, err.message);
            }
        }
        
        // Wait 12 seconds to drastically slow down and avoid IP bans/rate limits
        await sleep(12000);
    }
    
    // Update state to the next batch
    state.lastProcessedIndex = startIndex + processedCount;
    if (state.lastProcessedIndex >= stores.length) {
        state.lastProcessedIndex = 0; // Cycle back to the start!
    }
    fs.writeFileSync(STATE_FILE, JSON.stringify(state, null, 2));
    
    console.log(`🏁 Pipeline Finished! Next run will start at website index ${state.lastProcessedIndex}.`);
}

runPipeline();

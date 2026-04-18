require('dotenv').config();
const { GoogleGenerativeAI } = require('@google/generative-ai');

const SUPABASE_URL = process.env.SUPABASE_URL || "https://fwhzasbjexillgfrvksx.supabase.co"; 
const SUPABASE_ANON_KEY = process.env.SUPABASE_ANON_KEY || "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImZ3aHphc2JqZXhpbGxnZnJ2a3N4Iiwicm9sZSI6ImFub24iLCJpYXQiOjE3NzY0Mzk5NzksImV4cCI6MjA5MjAxNTk3OX0.MfZPPcx4d7OkAo56emiRjF9FabceUweCVJqv48tXAv4";
const GEMINI_API_KEY = process.env.GEMINI_API_KEY || "YOUR_GEMINI_API_KEY";

const genAI = new GoogleGenerativeAI(GEMINI_API_KEY);

async function fetchExistingDomains() {
    console.log("Fetching existing stores from Supabase...");
    let res = await fetch(`${SUPABASE_URL}/rest/v1/stores?select=domain`, {
        headers: {
            'apikey': SUPABASE_ANON_KEY,
            'Authorization': `Bearer ${SUPABASE_ANON_KEY}`
        }
    });

    if (!res.ok) {
        console.error("Failed to fetch stores", await res.text());
        return [];
    }
    const data = await res.json();
    return data.map(s => s.domain.toLowerCase());
}

async function askAIToFindStores(existingDomains) {
    console.log("Asking Gemini AI to intelligently discover new Indian e-commerce sites...");
    
    // We pass a few existing ones so the AI understands what we already have and avoids them
    const sampleExisting = existingDomains.slice(0, 50).join(", ");

    const prompt = `
        You are an AI tasked with finding new online shopping websites in India that often have discount coupons or promo codes.
        Here are some examples of domains we ALREADY have: ${sampleExisting}

        Please brainstorm and return a JSON list of 15 totally different, popular, or trending e-commerce domains in India.
        Include fashion, electronics, food delivery, beauty, travel, and lifestyle sites.
        IMPORTANT: Only return a strict JSON array of objects. No intro text, no markdown block quotes.
        Format must be exactly:
        [
            {"domain": "zomato.com", "name": "Zomato"},
            {"domain": "croma.com", "name": "Croma"}
        ]
    `;

    try {
        const model = genAI.getGenerativeModel({ model: "gemini-pro" });
        const result = await model.generateContent(prompt);
        let textResult = result.response.text().trim();
        
        if (textResult.startsWith('```json')) textResult = textResult.replace('```json', '');
        if (textResult.startsWith('```')) textResult = textResult.replace('```', '');
        if (textResult.endsWith('```')) textResult = textResult.replace(/```$/, '');

        const parsedStores = JSON.parse(textResult.trim());
        return Array.isArray(parsedStores) ? parsedStores : [];
    } catch (e) {
        console.error("AI Store Discovery failed:", e.message);
        return [];
    }
}

async function addNewStores(newStores) {
    if (newStores.length === 0) return;

    console.log(`Sending ${newStores.length} new discovered stores to Supabase...`);
    
    // Format the payload for Supabase
    const payload = newStores.map(store => ({
        domain: store.domain.toLowerCase().replace('www.', ''),
        name: store.name,
        category: 'general',
        status: 'active'
    }));

    let res = await fetch(`${SUPABASE_URL}/rest/v1/stores`, {
        method: 'POST',
        headers: {
            'apikey': SUPABASE_ANON_KEY,
            'Authorization': `Bearer ${SUPABASE_ANON_KEY}`,
            'Content-Type': 'application/json',
            'Prefer': 'resolution=ignore-duplicates' // Suppress errors if unique constraint is hit
        },
        body: JSON.stringify(payload)
    });

    if (res.ok) {
        console.log(`✅ Magic! AI successfully found and injected ${newStores.length} new websites to your database!`);
    } else {
        console.error(`❌ Failed to insert new websites.`, await res.text());
    }
}

async function runDiscovery() {
    if (GEMINI_API_KEY === "YOUR_GEMINI_API_KEY") {
        console.error("Missing Gemini API Key. Cannot run auto-discovery.");
        return;
    }

    const existingDomains = await fetchExistingDomains();
    console.log(`Database currently has ${existingDomains.length} stores.`);

    const newlyDiscovered = await askAIToFindStores(existingDomains);
    
    // Filter out ones we definitely already have
    const uniqueNewStores = newlyDiscovered.filter(store => {
        let cleanDomain = store.domain.toLowerCase().replace('www.', '');
        return !existingDomains.includes(cleanDomain);
    });

    console.log(`AI brainstormed ${newlyDiscovered.length} stores, ${uniqueNewStores.length} are brand new to us!`);
    
    await addNewStores(uniqueNewStores);
}

runDiscovery();

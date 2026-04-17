document.addEventListener('DOMContentLoaded', () => {
    const searchInput = document.getElementById('search-input');
    const resultsDiv = document.getElementById('results');
    const defaultView = document.getElementById('default-view');
    const submitView = document.getElementById('submit-view');
    const btnOptions = document.getElementById('btn-options');
    
    const trendingList = document.getElementById('trending-list');
    const btnShowSubmit = document.getElementById('btn-show-submit');
    const btnSubmitCoupon = document.getElementById('btn-submit-coupon');
    const btnCancelSubmit = document.getElementById('btn-cancel-submit');

    // Apply dark mode if setting enabled
    chrome.storage.local.get(['theme'], (result) => {
        if (result.theme === 'dark') document.body.classList.add('theme-dark');
    });

    btnOptions.addEventListener('click', () => {
        if (chrome.runtime.openOptionsPage) {
            chrome.runtime.openOptionsPage();
        } else {
            window.open(chrome.runtime.getURL('options.html'));
        }
    });

    // Detect Current Site
    chrome.tabs.query({active: true, currentWindow: true}, (tabs) => {
        if (tabs.length > 0 && typeof normalizeDomain === 'function') {
            try {
                const url = new URL(tabs[0].url);
                if (url.protocol.startsWith('http')) {
                    const domain = normalizeDomain(url.hostname);
                    chrome.runtime.sendMessage({ action: 'fetchCoupons', domain: domain }, (response) => {
                        if (response && response.success && response.coupons.length > 0) {
                            showSiteCoupons(domain, response.coupons);
                        }
                    });
                }
            } catch (e) {
                console.error("Invalid URL", e);
            }
        }
    });

    function showSiteCoupons(domain, coupons) {
        defaultView.style.display = 'none';
        submitView.style.display = 'none';
        resultsDiv.style.display = 'block';

        let html = `
            <div style="background: #ff3366; color: #fff; padding: 10px; border-radius: 6px; margin-bottom: 15px; text-align: center;">
                <h4 style="margin: 0; font-size: 14px;">${coupons.length} Deals found for ${domain}</h4>
            </div>
            <div style="max-height: 250px; overflow-y: auto;">
        `;

        coupons.forEach(coupon => {
            html += `
                <div style="border: 1px solid #eee; padding: 10px; margin-bottom: 10px; border-radius: 6px; box-shadow: 0 1px 3px rgba(0,0,0,0.05); background: #fff;">
                    <div style="font-size: 13px; margin-bottom: 5px; color: #555; text-align: left;">${coupon.title}</div>
                    <div style="display: flex; justify-content: space-between; align-items: center;">
                        <strong style="color: #ff3366; font-size: 15px; border: 1px dashed #ff3366; padding: 4px 8px; background: #fff1f4; border-radius: 4px;">${coupon.code}</strong>
                        <button class="popup-btn-copy" data-code="${coupon.code}" style="font-size: 12px; padding: 6px 12px; cursor: pointer; background: #007bff; color: #fff; border: none; border-radius: 4px; font-weight: bold;">Copy</button>
                    </div>
                </div>
            `;
        });
        
        html += `</div>`;
        resultsDiv.innerHTML = html;

        // Add copy logic
        resultsDiv.querySelectorAll('.popup-btn-copy').forEach(btn => {
            btn.addEventListener('click', (e) => {
                const code = e.target.getAttribute('data-code');
                navigator.clipboard.writeText(code).then(() => {
                    const originalText = e.target.innerText;
                    e.target.innerText = "Copied!";
                    e.target.style.background = "#28a745";
                    setTimeout(() => {
                        e.target.innerText = originalText;
                        e.target.style.background = "#007bff";
                    }, 2000);
                });
            });
        });
    }

    // Mock Trending Deals
    const trendingDeals = [
        { store: "amazon.in", text: "Sale on Electronics!" },
        { store: "ajio.com", text: "New Users 20% Off" },
        { store: "flipkart.com", text: "BBD Pre-deals" }
    ];

    trendingList.innerHTML = trendingDeals.map(d => `<a href="https://${d.store}" target="_blank" style="display: block; text-decoration: none; color: inherit; padding: 5px; border-bottom: 1px solid #eee; font-size: 13px; cursor: pointer; text-align: left;"><strong>${d.store}</strong> • ${d.text} <span style="float:right; color:#007bff;">&rarr;</span></a>`).join('');

    // Navigation Logic
    btnShowSubmit.addEventListener('click', () => {
        defaultView.style.display = 'none';
        resultsDiv.style.display = 'none';
        submitView.style.display = 'block';
    });

    btnCancelSubmit.addEventListener('click', () => {
        submitView.style.display = 'none';
        defaultView.style.display = 'block';
        searchInput.value = '';
    });

    btnSubmitCoupon.addEventListener('click', () => {
        const store = document.getElementById('sub-store').value.trim();
        const code = document.getElementById('sub-code').value.trim();
        const title = document.getElementById('sub-title').value.trim();

        if (!store || !code) {
            alert("Please fill your store domain and code.");
            return;
        }

        btnSubmitCoupon.disabled = true;
        btnSubmitCoupon.textContent = "Submitting...";

        chrome.runtime.sendMessage({ action: 'submitCoupon', store: store, code: code, title: title }, (response) => {
            alert("Thanks! Your coupon has been securely submitted for verification.");
            submitView.style.display = 'none';
            defaultView.style.display = 'block';
            
            // Reset form
            btnSubmitCoupon.disabled = false;
            btnSubmitCoupon.textContent = "Submit for Review";
            document.getElementById('sub-store').value = '';
            document.getElementById('sub-code').value = '';
            document.getElementById('sub-title').value = '';
        });
    });

    searchInput.addEventListener('input', (e) => {
        const query = e.target.value.toLowerCase().trim();
        if (!query) {
            defaultView.style.display = 'block';
            resultsDiv.style.display = 'none';
            return;
        }

        defaultView.style.display = 'none';
        submitView.style.display = 'none';
        resultsDiv.style.display = 'block';

        const matched = typeof SUPPORTED_STORES !== 'undefined' ? SUPPORTED_STORES.filter(store => store.includes(query)) : [];
        
        if (matched.length > 0) {
            resultsDiv.innerHTML = '<ul class="search-list" style="padding: 0; list-style: none; margin: 0; text-align: left;">' + matched.map(s => `<li><a href="https://${s}" target="_blank" style="display: block; padding: 8px 0; border-bottom: 1px solid #eee; text-decoration: none; color: #007bff; font-weight: 500;">Open ${s} &rarr;</a></li>`).join('') + '</ul>';
        } else {
            resultsDiv.innerHTML = '<div class="empty-state"><p>No stores found.</p><button id="suggest-btn">Suggest this store?</button></div>';
            const suggestBtn = document.getElementById('suggest-btn');
            if (suggestBtn) suggestBtn.addEventListener('click', () => {
                alert('Thanks for suggesting ' + query + '!');
            });
        }
    });
});

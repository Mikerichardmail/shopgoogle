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
            <div style="background: var(--primary-gradient); color: #fff; padding: 12px; border-radius: 8px; margin-bottom: 15px; text-align: center; box-shadow: var(--shadow-sm);">
                <h4 style="margin: 0; font-size: 14px; color: white; letter-spacing: 0;">🎉 ${coupons.length} Deals found for ${domain}</h4>
            </div>
            <div style="max-height: 280px; overflow-y: auto; padding-right: 4px; padding-bottom: 10px;">
        `;

        coupons.forEach(coupon => {
            html += `
                <div class="coupon-card">
                    <div class="coupon-title">${coupon.title}</div>
                    <div style="display: flex; justify-content: space-between; align-items: center; margin-top: 4px;">
                        <strong>${coupon.code}</strong>
                        <button class="copy-btn popup-btn-copy" data-code="${coupon.code}">
                            <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" style="margin-right: 4px; vertical-align: middle;"><rect x="9" y="9" width="13" height="13" rx="2" ry="2"></rect><path d="M5 15H4a2 2 0 0 1-2-2V4a2 2 0 0 1 2-2h9a2 2 0 0 1 2 2v1"></path></svg>
                            Copy
                        </button>
                    </div>
                </div>
            `;
        });
        
        html += `</div>`;
        resultsDiv.innerHTML = html;

        // Add copy logic
        resultsDiv.querySelectorAll('.popup-btn-copy').forEach(btn => {
            btn.addEventListener('click', (e) => {
                const targetBtn = e.currentTarget;
                const code = targetBtn.getAttribute('data-code');
                navigator.clipboard.writeText(code).then(() => {
                    const originalHTML = targetBtn.innerHTML;
                    targetBtn.innerHTML = `
                      <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" style="margin-right: 4px; vertical-align: middle;"><polyline points="20 6 9 17 4 12"></polyline></svg>
                      Copied!
                    `;
                    targetBtn.style.background = "var(--accent-success)";
                    targetBtn.style.color = "#fff";
                    targetBtn.style.borderColor = "var(--accent-success)";
                    
                    setTimeout(() => {
                        targetBtn.innerHTML = originalHTML;
                        targetBtn.style.background = "";
                        targetBtn.style.color = "";
                        targetBtn.style.borderColor = "";
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

    trendingList.innerHTML = trendingDeals.map(d => `
        <a href="https://${d.store}" target="_blank" style="display: flex; justify-content: space-between; align-items: center; text-decoration: none; color: inherit; padding: 10px 0; border-bottom: 1px solid var(--border-color); font-size: 13px; cursor: pointer; transition: color 0.2s;">
            <span><strong style="color: var(--text-main); font-weight: 600;">${d.store}</strong> • <span style="color: var(--text-muted);">${d.text}</span></span>
            <span style="color: #FF416C; font-weight: 600;">&rarr;</span>
        </a>
    `).join('');

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
            btnSubmitCoupon.innerHTML = "Submit for Review";
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
            resultsDiv.innerHTML = '<ul style="padding: 0; list-style: none; margin: 0;">' + 
                matched.map(s => `<li><a href="https://${s}" target="_blank" style="display: flex; justify-content: space-between; padding: 12px 10px; margin-bottom: 8px; border: 1px solid var(--border-color); border-radius: 8px; text-decoration: none; color: var(--text-main); font-weight: 500; background: var(--bg-secondary); transition: all 0.2s;">Open ${s} <span style="color: #FF416C;">&rarr;</span></a></li>`).join('') 
                + '</ul>';
        } else {
            resultsDiv.innerHTML = '<div class="empty-state"><p>No stores found matching "'+query+'"</p><button id="suggest-btn" style="background:#FF416C; color:white; border:none;">Suggest this store?</button></div>';
            const suggestBtn = document.getElementById('suggest-btn');
            if (suggestBtn) suggestBtn.addEventListener('click', () => {
                alert('Thanks for suggesting ' + query + '!');
            });
        }
    });
});

// Content script runs on every page

(function() {
    function initApp() {
        const rawHostname = window.location.hostname;
        const domain = typeof normalizeDomain === 'function' ? normalizeDomain(rawHostname) : rawHostname.replace('www.', '');

        console.log("India Coupon Ext: Checking domain - ", domain);

        chrome.storage.local.get(['enabled', 'disabledSites'], (result) => {
            if (!result.enabled || (result.disabledSites && result.disabledSites.includes(domain))) {
                console.log("India Coupon Ext: Disabled globally or for this site.");
                return;
            }

            if (typeof isSupportedStore === 'function' && isSupportedStore(domain)) {
                console.log("India Coupon Ext: Supported store detected!", domain);
                initCouponWidget(domain);
            } else {
                // Check for strong shopping signals as fallback
                detectShoppingSiteFallback(domain);
            }
        });
    }

    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', initApp);
    } else {
        initApp();
    }

    function detectShoppingSiteFallback(domain) {
        if (!document.body) return; // Safety check
        // Quick DOM scan for shopping-related keywords and symbols
        const text = document.body.innerText.toLowerCase();
        const hasPriceSymbols = /[\u20B9₹$€]/.test(text) || text.includes('rs.');
        const hasCartWords = text.includes('add to cart') || text.includes('buy now') || text.includes('checkout');
        
        if (hasPriceSymbols && hasCartWords) {
            console.log("India Coupon Ext: Strong shopping signals detected on unknown site.");
            // Wait a few seconds so it's not aggressive
            setTimeout(() => {
                showFallbackPrompt(domain);
            }, 3000);
        }
    }

    function showFallbackPrompt(domain) {
        if (document.getElementById('ic-fallback-prompt')) return;
        
        const prompt = document.createElement('div');
        prompt.id = 'ic-fallback-prompt';
        prompt.style.cssText = `
            position: fixed;
            bottom: 20px;
            right: 20px;
            background: #fff;
            border: 1px solid #ffd54f;
            border-left: 4px solid #ffb300;
            border-radius: 4px;
            padding: 12px;
            box-shadow: 0 4px 12px rgba(0,0,0,0.1);
            z-index: 999998;
            font-family: sans-serif;
            font-size: 13px;
            color: #333;
            animation: ic-slide-up 0.4s ease forwards;
        `;
        prompt.innerHTML = `
            <div style="font-weight: bold; margin-bottom: 5px;">Looking for deals here?</div>
            <div style="color: #666; margin-bottom: 8px;">We can look for coupons for ${domain}.</div>
            <button id="ic-fallback-yes" style="background:#007bff; color:#fff; border:none; padding:4px 8px; border-radius:3px; cursor:pointer;">Search</button>
            <button id="ic-fallback-no" style="background:#eee; border:none; padding:4px 8px; border-radius:3px; cursor:pointer; margin-left: 5px;">Close</button>
        `;
        document.body.appendChild(prompt);

        document.getElementById('ic-fallback-no').addEventListener('click', () => prompt.remove());
        document.getElementById('ic-fallback-yes').addEventListener('click', () => {
            prompt.innerHTML = `<div style="font-weight:bold;">No known coupons yet!</div><div style="color:#666; font-size:12px;">Go to the extension popup to submit one.</div><button id="ic-fallback-no-2" style="background:#eee; border:none; padding:4px 8px; border-radius:3px; cursor:pointer; margin-top:5px; width:100%;">Close</button>`;
            document.getElementById('ic-fallback-no-2').addEventListener('click', () => prompt.remove());
        });
    }

    function initCouponWidget(domain) {
        // Build style block for animations
        if (!document.getElementById('ic-animations')) {
            const style = document.createElement('style');
            style.id = 'ic-animations';
            style.innerHTML = `
                @keyframes ic-slide-up {
                    0% { transform: translateY(50px); opacity: 0; }
                    100% { transform: translateY(0); opacity: 1; }
                }
                .ic-widget-anim {
                    animation: ic-slide-up 0.4s cubic-bezier(0.175, 0.885, 0.32, 1.275) forwards;
                }
            `;
            document.head.appendChild(style);
        }

        // Send message to background to fetch coupons
        try {
            chrome.runtime.sendMessage({ action: 'fetchCoupons', domain: domain }, (response) => {
                if (chrome.runtime.lastError) {
                    console.error("India Coupon Ext Error:", chrome.runtime.lastError);
                    return;
                }
                if (response && response.success && response.coupons.length > 0) {
                    renderWidget(domain, response.coupons);
                } else {
                    console.log("India Coupon Ext: No coupons available currently for this store.");
                }
            });
        } catch(e) {
            console.error("India Coupon Ext failed to fetch:", e);
        }
    }

    function renderWidget(domain, coupons) {
        // Advanced DOM rendering with modern, premium styling
        const widget = document.createElement('div');
        widget.id = 'india-coupon-widget';
        widget.className = 'ic-widget-anim';
        widget.style.cssText = `
            position: fixed;
            bottom: 24px;
            right: 24px;
            width: 320px;
            background: #ffffff;
            border: 1px solid rgba(229, 231, 235, 1);
            border-radius: 16px;
            box-shadow: 0 10px 25px -5px rgba(0, 0, 0, 0.1), 0 8px 10px -6px rgba(0, 0, 0, 0.1);
            z-index: 999999;
            font-family: 'Inter', -apple-system, system-ui, sans-serif;
            color: #111827;
            overflow: hidden;
        `;
        
        // Import Inter Font if not present
        if (!document.getElementById('ic-modern-font')) {
            const fontLink = document.createElement('link');
            fontLink.id = 'ic-modern-font';
            fontLink.href = 'https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap';
            fontLink.rel = 'stylesheet';
            document.head.appendChild(fontLink);
        }

        let html = `
            <div style="background: linear-gradient(135deg, #FF416C 0%, #FF4B2B 100%); color: #fff; padding: 16px 20px; display: flex; justify-content: space-between; align-items: center;">
                <h4 style="margin: 0; font-size: 15px; font-weight: 600; letter-spacing: -0.3px;">🎁 Deals for ${domain}</h4>
                <div style="display: flex; gap: 10px; align-items: center;">
                    <button id="ic-btn-track" style="background: rgba(255,255,255,0.2); color: #fff; border: 1px solid rgba(255,255,255,0.4); font-size: 11px; font-weight: 600; border-radius: 6px; padding: 4px 8px; cursor: pointer; transition: all 0.2s;">Track Price</button>
                    <button id="india-coupon-close" style="background: none; border: none; color: #fff; cursor: pointer; font-size: 18px; margin-left: 2px; opacity: 0.8; transition: opacity 0.2s;">&times;</button>
                </div>
            </div>
            <div style="padding: 16px 16px 4px; max-height: 350px; overflow-y: auto; background-color: #f4f5f7;">
        `;
        
        coupons.forEach(coupon => {
            html += \`
                <div class="ic-coupon-card" data-code="\${coupon.code}" data-id="\${coupon.id || coupon.code}" style="background: #ffffff; border: 1px solid #e5e7eb; padding: 16px; margin-bottom: 12px; border-radius: 12px; box-shadow: 0 1px 2px rgba(0,0,0,0.05); transition: transform 0.2s;">
                    <div style="font-size: 14px; font-weight: 500; margin-bottom: 8px; color: #111827; line-height: 1.4;">\${coupon.title}</div>
                    <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 10px;">
                        <strong style="color: #FF416C; font-size: 15px; font-weight: 700; background: rgba(255, 65, 108, 0.1); padding: 4px 8px; border-radius: 6px;">\${coupon.code}</strong>
                        <button class="ic-btn-copy" style="font-size: 12px; font-weight: 600; padding: 6px 12px; cursor: pointer; background: #e5e7eb; color: #111827; border: none; border-radius: 6px; transition: background 0.2s;">Copy</button>
                    </div>
                    <div style="display: flex; gap: 8px; font-size: 11px; font-weight: 600;">
                        <button class="ic-btn-vote-up" style="flex: 1; padding: 6px; cursor: pointer; background: #f0fdf4; color: #166534; border: 1px solid #bbf7d0; border-radius: 6px; transition: all 0.2s;">👍 Worked</button>
                        <button class="ic-btn-vote-down" style="flex: 1; padding: 6px; cursor: pointer; background: #fef2f2; color: #991b1b; border: 1px solid #fecaca; border-radius: 6px; transition: all 0.2s;">👎 Failed</button>
                    </div>
                </div>
            \`;
        });
        
        html += \`</div>\`;
        widget.innerHTML = html;
        document.body.appendChild(widget);

        document.getElementById('india-coupon-close').addEventListener('click', () => {
            widget.remove();
        });

        document.getElementById('ic-btn-track').addEventListener('click', (e) => {
            e.target.innerText = "Tracking...";
            e.target.disabled = true;
            // Native mock notification for Chrome
            chrome.runtime.sendMessage({ action: 'triggerNotification', title: 'Price Tracker Active', message: `We are now watching prices on ${domain} for you.` });
        });

        // Copy events
        widget.querySelectorAll('.ic-btn-copy').forEach(btn => {
            btn.addEventListener('click', (e) => {
                const card = e.target.closest('.ic-coupon-card');
                const code = card.getAttribute('data-code');
                navigator.clipboard.writeText(code).then(() => {
                    e.target.innerText = "Copied!";
                    e.target.style.background = "#28a745";
                    setTimeout(() => {
                        e.target.innerText = "Copy";
                        e.target.style.background = "#007bff";
                    }, 2000);
                });
            });
        });

        // Vote events
        widget.querySelectorAll('.ic-btn-vote-up').forEach(btn => {
            btn.addEventListener('click', (e) => {
                const card = e.target.closest('.ic-coupon-card');
                const id = card.getAttribute('data-id');
                chrome.runtime.sendMessage({ action: 'voteCoupon', id: id, vote: 'worked' });
                e.target.innerText = "Thanks!";
                e.target.disabled = true;
            });
        });
        
        widget.querySelectorAll('.ic-btn-vote-down').forEach(btn => {
            btn.addEventListener('click', (e) => {
                const card = e.target.closest('.ic-coupon-card');
                const id = card.getAttribute('data-id');
                chrome.runtime.sendMessage({ action: 'voteCoupon', id: id, vote: 'failed' });
                e.target.innerText = "Thanks!";
                e.target.disabled = true;
            });
        });
    }
})();

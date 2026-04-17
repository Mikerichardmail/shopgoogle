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
        // Advanced DOM rendering with copy & voting UI
        const widget = document.createElement('div');
        widget.id = 'india-coupon-widget';
        widget.className = 'ic-widget-anim';
        widget.style.cssText = `
            position: fixed;
            bottom: 20px;
            right: 20px;
            width: 280px;
            background: #fff;
            border: 1px solid #e0e0e0;
            border-radius: 8px;
            box-shadow: 0 8px 24px rgba(0,0,0,0.12);
            z-index: 999999;
            font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
            color: #333;
            transition: all 0.3s ease;
        `;
        
        let html = `
            <div style="background: #ff3366; color: #fff; padding: 10px; border-radius: 8px 8px 0 0; display: flex; justify-content: space-between; align-items: center;">
                <h4 style="margin: 0; font-size: 14px;">Deals for ${domain}</h4>
                <div style="display: flex; gap: 8px; align-items: center;">
                    <button id="ic-btn-track" style="background: #fff; color: #ff3366; border: none; font-size: 10px; font-weight: bold; border-radius: 4px; padding: 2px 6px; cursor: pointer;">Track Price</button>
                    <button id="india-coupon-close" style="background: none; border: none; color: #fff; cursor: pointer; font-size: 16px; margin-left: 2px;">&times;</button>
                </div>
            </div>
            <div style="padding: 10px; max-height: 300px; overflow-y: auto;">
        `;
        
        coupons.forEach(coupon => {
            html += \`
                <div class="ic-coupon-card" data-code="\${coupon.code}" data-id="\${coupon.id || coupon.code}" style="border: 1px solid #eee; padding: 10px; margin-bottom: 10px; border-radius: 6px; box-shadow: 0 1px 3px rgba(0,0,0,0.05);">
                    <div style="font-size: 13px; margin-bottom: 5px; color: #555;">\${coupon.title}</div>
                    <div style="display: flex; gap: 5px; align-items: center; margin-bottom: 8px;">
                        <strong style="color: #ff3366; font-size: 15px; border: 1px dashed #ff3366; padding: 2px 6px; background: #fff1f4; border-radius: 4px;">\${coupon.code}</strong>
                        <button class="ic-btn-copy" style="font-size: 11px; padding: 4px 8px; cursor: pointer; background: #007bff; color: #fff; border: none; border-radius: 4px;">Copy</button>
                    </div>
                    <div style="display: flex; gap: 5px; font-size: 11px;">
                        <button class="ic-btn-vote-up" style="flex: 1; padding: 4px; cursor: pointer; background: #e8f5e9; color: #2e7d32; border: 1px solid #c8e6c9; border-radius: 4px;">Worked</button>
                        <button class="ic-btn-vote-down" style="flex: 1; padding: 4px; cursor: pointer; background: #ffebee; color: #c62828; border: 1px solid #ffcdd2; border-radius: 4px;">Failed</button>
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

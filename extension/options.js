document.addEventListener('DOMContentLoaded', () => {
    const enableCheckbox = document.getElementById('enable-extension');
    const darkModeCheckbox = document.getElementById('dark-mode');
    const notifCheckbox = document.getElementById('enable-notifications');
    const clearCacheBtn = document.getElementById('clear-cache');
    const statusDiv = document.getElementById('status');

    // Load current settings
    chrome.storage.local.get(['enabled', 'theme'], (result) => {
        enableCheckbox.checked = result.enabled !== false;
        darkModeCheckbox.checked = result.theme === 'dark';
        if (result.theme === 'dark') document.body.classList.add('theme-dark');
    });

    chrome.permissions.contains({ permissions: ['notifications'] }, (hasPerm) => {
        notifCheckbox.checked = hasPerm;
    });

    // Save settings on change
    enableCheckbox.addEventListener('change', () => {
        chrome.storage.local.set({ enabled: enableCheckbox.checked }, () => {
            showStatus('Extension status saved.');
        });
    });

    darkModeCheckbox.addEventListener('change', () => {
        const theme = darkModeCheckbox.checked ? 'dark' : 'light';
        chrome.storage.local.set({ theme: theme }, () => {
            if (theme === 'dark') document.body.classList.add('theme-dark');
            else document.body.classList.remove('theme-dark');
            showStatus('Theme saved.');
        });
    });

    notifCheckbox.addEventListener('change', (e) => {
        if (e.target.checked) {
            chrome.permissions.request({ permissions: ['notifications'] }, (granted) => {
                if (granted) {
                    showStatus("Notifications enabled!");
                } else {
                    e.target.checked = false;
                    showStatus("Permission denied.");
                }
            });
        } else {
            chrome.permissions.remove({ permissions: ['notifications'] }, (removed) => {
                showStatus("Notifications disabled.");
            });
        }
    });

    clearCacheBtn.addEventListener('click', () => {
        chrome.storage.local.set({ couponCache: {} }, () => {
            showStatus('Coupon cache cleared.');
        });
    });

    function showStatus(msg) {
        statusDiv.textContent = msg;
        setTimeout(() => {
            statusDiv.textContent = '';
        }, 2000);
    }
});

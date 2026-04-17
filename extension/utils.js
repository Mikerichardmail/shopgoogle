// Utility functions for the extension

/**
 * Normalizes hostnames (e.g. www.ajio.com -> ajio.com)
 * @param {string} hostname
 * @returns {string}
 */
function normalizeDomain(hostname) {
    let domain = hostname.toLowerCase();
    if (domain.startsWith("www.")) {
        domain = domain.replace("www.", "");
    } else if (domain.startsWith("m.")) {
        domain = domain.replace("m.", "");
    } else if (domain.startsWith("checkout.")) {
        domain = domain.replace("checkout.", "");
    }
    return domain;
}

const SUPPORTED_STORES = [
    "amazon.in",
    "flipkart.com",
    "ajio.com",
    "myntra.com",
    "nykaa.com",
    "tatacliq.com"
];

function isSupportedStore(domain) {
    return SUPPORTED_STORES.some(store => domain === store || domain.endsWith('.' + store));
}

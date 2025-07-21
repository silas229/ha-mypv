/**
 * MyPV Proxy Adapter
 * This script modifies the original MyPV interface to use the Home Assistant addon proxy
 * instead of direct device communication. Supports Home Assistant Ingress.
 */

(function() {
    'use strict';
    
    // Detect if running under Home Assistant Ingress
    const isIngress = window.location.pathname.includes('/api/hassio_ingress/');
    const ingressPath = isIngress ? window.location.pathname.split('/api/hassio_ingress/')[1].split('/')[0] : '';
    const basePath = isIngress ? `/api/hassio_ingress/${ingressPath}` : '';
    
    console.log('MyPV Proxy Adapter: Ingress detected:', isIngress);
    if (isIngress) {
        console.log('MyPV Proxy Adapter: Base path:', basePath);
    }
    
    // Override the XMLHttpRequest to intercept MyPV API calls
    const originalOpen = XMLHttpRequest.prototype.open;
    const originalSend = XMLHttpRequest.prototype.send;
    
    XMLHttpRequest.prototype.open = function(method, url, async, user, password) {
        // Store the original URL
        this._originalUrl = url;
        
        // Check if this is a MyPV API call
        if (url && (url.includes('.jsn') || url.includes('/api/'))) {
            // Replace the URL with our proxy
            this._proxiedUrl = proxyUrl(url);
            
            console.log('MyPV Proxy: Intercepted API call:', url, '-> Proxied to:', this._proxiedUrl);
            return originalOpen.call(this, method, this._proxiedUrl, async, user, password);
        }
        
        // For non-API calls, use original URL
        return originalOpen.call(this, method, url, async, user, password);
    };
    
    // Override fetch API as well
    const originalFetch = window.fetch;
    window.fetch = function(url, options) {
        if (typeof url === 'string' && (url.includes('.jsn') || url.includes('/api/'))) {
            const proxiedUrl = proxyUrl(url);
            
            console.log('MyPV Proxy: Intercepted fetch call:', url, '-> Proxied to:', proxiedUrl);
            return originalFetch.call(this, proxiedUrl, options);
        }
        
        return originalFetch.call(this, url, options);
    };
    
    // Override jQuery AJAX if available
    if (typeof $ !== 'undefined' && $.ajax) {
        const originalAjax = $.ajax;
        $.ajax = function(settings) {
            if (typeof settings === 'string') {
                // URL as first parameter
                const url = settings;
                if (url.includes('.jsn') || url.includes('/api/')) {
                    arguments[0] = proxyUrl(url);
                    console.log('MyPV Proxy: Intercepted jQuery AJAX call:', url, '-> Proxied to:', arguments[0]);
                }
            } else if (settings && settings.url) {
                // Settings object
                const url = settings.url;
                if (url.includes('.jsn') || url.includes('/api/')) {
                    settings.url = proxyUrl(url);
                    console.log('MyPV Proxy: Intercepted jQuery AJAX call:', url, '-> Proxied to:', settings.url);
                }
            }
            
            return originalAjax.apply(this, arguments);
        };
    }
    
    function proxyUrl(url) {
        let proxiedUrl = url;
        
        if (url.startsWith('/') || url.includes('.jsn')) {
            proxiedUrl = url;
        } else if (url.startsWith('http://') || url.startsWith('https://')) {
            try {
                const urlObj = new URL(url);
                proxiedUrl = urlObj.pathname + urlObj.search;
            } catch (e) {
                proxiedUrl = url;
            }
        }
        
        // Add Ingress base path if running under Ingress
        if (isIngress && !proxiedUrl.startsWith(basePath)) {
            proxiedUrl = basePath + proxiedUrl;
        }
        
        return proxiedUrl;
    }
    
    // Add a status indicator to show proxy is active
    function addProxyStatusIndicator() {
        const indicator = document.createElement('div');
        indicator.id = 'proxy-status-indicator';
        indicator.style.cssText = `
            position: fixed;
            top: 10px;
            right: 10px;
            background: #28a745;
            color: white;
            padding: 5px 10px;
            border-radius: 4px;
            font-size: 12px;
            z-index: 10000;
            box-shadow: 0 2px 4px rgba(0,0,0,0.2);
        `;
        indicator.textContent = isIngress ? 'HA Ingress Active' : 'Proxy Active';
        document.body.appendChild(indicator);
        
        // Hide after 3 seconds
        setTimeout(() => {
            indicator.style.opacity = '0.3';
        }, 3000);
    }
    
    // Wait for DOM to be ready
    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', addProxyStatusIndicator);
    } else {
        addProxyStatusIndicator();
    }
    
    console.log('MyPV Proxy Adapter loaded and ready');
})();

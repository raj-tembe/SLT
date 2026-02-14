/**
 * Sign Language Translator - Main JavaScript
 * Handles UI interactions, search, TTS, and general functionality
 */

// Initialize on DOM load
document.addEventListener('DOMContentLoaded', function() {
    initializeApp();
});

/**
 * Initialize the application
 */
function initializeApp() {
    console.log('Sign Language Translator App Initialized');
    
    // Check browser support for features
    checkBrowserSupport();
    
    // Initialize modules
    initializeTTS();
}

/**
 * Check browser support for required features
 */
function checkBrowserSupport() {
    const features = {
        getUserMedia: !!navigator.mediaDevices && !!navigator.mediaDevices.getUserMedia,
        speechSynthesis: !!window.speechSynthesis,
        localStorage: typeof(Storage) !== 'undefined'
    };

    if (!features.getUserMedia) {
        console.warn('Camera access not available in this browser');
    }
    if (!features.speechSynthesis) {
        console.warn('Text-to-speech not supported in this browser');
    }
}

/**
 * Initialize Text-to-Speech functionality
 */
function initializeTTS() {
    if (!window.speechSynthesis) {
        console.warn('Text-to-Speech not supported');
        return;
    }

    window.speakText = function(text) {
        // Cancel any ongoing speech
        window.speechSynthesis.cancel();

        const utterance = new SpeechSynthesisUtterance(text);
        utterance.rate = 0.9;
        utterance.pitch = 1.0;
        utterance.volume = 1.0;
        utterance.lang = 'en-US';

        window.speechSynthesis.speak(utterance);
    };
}

/**
 * Utility: Get all visible sign cards
 */
function getVisibleSigns() {
    const cards = document.querySelectorAll('.sign-card');
    const visible = [];
    cards.forEach(card => {
        if (card.style.display !== 'none') {
            visible.push(card.dataset.sign);
        }
    });
    return visible;
}

/**
 * Utility: Debounce function for search
 */
function debounce(fn, delay = 300) {
    let timeoutId;
    return function(...args) {
        clearTimeout(timeoutId);
        timeoutId = setTimeout(() => fn.apply(this, args), delay);
    };
}

/**
 * Utility: Capitalize first letter
 */
function capitalize(str) {
    return str.charAt(0).toUpperCase() + str.slice(1);
}

/**
 * Utility: Format text for speech
 */
function formatTextForSpeech(text) {
    return text.toLowerCase().replace(/[^a-z\s]/g, '');
}

/**
 * Analytics: Track user actions
 */
function trackAction(action, data = {}) {
    console.log(`[Analytics] ${action}`, data);
    
    // Store in localStorage for potential future use
    if (typeof(Storage) !== 'undefined') {
        const timestamp = new Date().toISOString();
        const actionLog = {
            action,
            data,
            timestamp
        };
        
        // You could send this to a server endpoint later
        let actions = JSON.parse(localStorage.getItem('appActions') || '[]');
        actions.push(actionLog);
        
        // Keep only last 50 actions to avoid excessive storage
        if (actions.length > 50) {
            actions = actions.slice(-50);
        }
        
        localStorage.setItem('appActions', JSON.stringify(actions));
    }
}

/**
 * Utility: Escape HTML to prevent XSS
 */
function escapeHtml(text) {
    const map = {
        '&': '&amp;',
        '<': '&lt;',
        '>': '&gt;',
        '"': '&quot;',
        "'": '&#039;'
    };
    return text.replace(/[&<>"']/g, m => map[m]);
}

/**
 * UI: Add smooth scroll behavior
 */
document.querySelectorAll('a[href^="#"]').forEach(anchor => {
    anchor.addEventListener('click', function(e) {
        e.preventDefault();
        const target = document.querySelector(this.getAttribute('href'));
        if (target) {
            target.scrollIntoView({
                behavior: 'smooth'
            });
        }
    });
});

/**
 * Keyboard shortcuts
 */
document.addEventListener('keydown', function(e) {
    // Ctrl/Cmd + K: Focus search
    if ((e.ctrlKey || e.metaKey) && e.key.toLowerCase() === 'k') {
        e.preventDefault();
        const searchInput = document.getElementById('search-input');
        if (searchInput) {
            searchInput.focus();
        }
    }

    // Escape: Close modal
    if (e.key === 'Escape') {
        const modal = document.getElementById('sign-modal');
        if (modal && modal.style.display === 'flex') {
            modal.style.display = 'none';
        }
    }
});

/**
 * Performance: Lazy load images
 */
if ('IntersectionObserver' in window) {
    const imageObserver = new IntersectionObserver((entries, observer) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                const img = entry.target;
                if (img.dataset.src) {
                    img.src = img.dataset.src;
                    img.removeAttribute('data-src');
                    observer.unobserve(img);
                }
            }
        });
    });

    document.querySelectorAll('img[data-src]').forEach(img => {
        imageObserver.observe(img);
    });
}

/**
 * Service Worker registration for offline support (optional)
 * Disabled: Service worker file not included
 */
// if ('serviceWorker' in navigator) {
//     navigator.serviceWorker.register('/static/js/sw.js').catch(err => {
//         console.log('Service Worker registration failed:', err);
//     });
// }

// Export functions for use in templates
window.appUtils = {
    trackAction,
    speakText: window.speakText,
    formatTextForSpeech,
    getVisibleSigns,
    capitalize,
    escapeHtml
};

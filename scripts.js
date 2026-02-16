// ============================================
// CyberOS - Web Interface Scripts
// ============================================

/**
 * Initialize CyberOS Dashboard
 */
document.addEventListener('DOMContentLoaded', function() {
    console.log('CyberOS Dashboard Loaded');
    initializeNavigation();
    initializeScrollBehavior();
    initializeButtons();
    loadDashboardData();
});

/**
 * Navigation and scroll-to-top functionality
 */
function initializeNavigation() {
    const navLinks = document.querySelectorAll('nav a[href^="#"]');
    
    navLinks.forEach(link => {
        link.addEventListener('click', function(e) {
            const targetId = this.getAttribute('href');
            if (targetId === '#') return;
            
            const targetElement = document.querySelector(targetId);
            if (targetElement) {
                e.preventDefault();
                targetElement.scrollIntoView({ behavior: 'smooth' });
            }
        });
    });
}

/**
 * Scroll behavior tracking
 */
function initializeScrollBehavior() {
    window.addEventListener('scroll', function() {
        const scrollTop = window.scrollY;
        const header = document.querySelector('.header');
        
        if (scrollTop > 100) {
            header.style.boxShadow = '0 4px 12px rgba(0,0,0,0.15)';
        } else {
            header.style.boxShadow = '0 1px 3px rgba(0,0,0,0.12), 0 1px 2px rgba(0,0,0,0.24)';
        }
    });
}

/**
 * Button interactions
 */
function initializeButtons() {
    const buttons = document.querySelectorAll('.btn');
    
    buttons.forEach(button => {
        button.addEventListener('mouseenter', function() {
            this.style.transform = 'translateY(-2px)';
        });
        
        button.addEventListener('mouseleave', function() {
            this.style.transform = 'translateY(0)';
        });
    });
}

/**
 * Load and display dashboard data
 */
function loadDashboardData() {
    const dashboardData = {
        version: '0.1.0',
        status: 'alpha',
        releaseDate: 'February 28, 2025',
        downloadSize: '~180 MB',
        bootTime: '< 10 seconds',
        minRAM: '256 MB',
        recRAM: '1 GB',
        minDisk: '512 MB',
        recDisk: '5 GB'
    };
    
    console.log('Dashboard Data:', dashboardData);
    
    // Update version info if element exists
    const versionElement = document.querySelector('[data-version]');
    if (versionElement) {
        versionElement.textContent = dashboardData.version;
    }
}

/**
 * Copy code to clipboard
 */
function copyToClipboard(elementId) {
    const element = document.getElementById(elementId);
    if (!element) {
        console.error('Element not found: ' + elementId);
        return;
    }
    
    const text = element.textContent;
    
    if (navigator.clipboard) {
        navigator.clipboard.writeText(text).then(() => {
            showNotification('Copied to clipboard!', 'success');
        }).catch(() => {
            fallbackCopyToClipboard(text);
        });
    } else {
        fallbackCopyToClipboard(text);
    }
}

/**
 * Fallback copy to clipboard for older browsers
 */
function fallbackCopyToClipboard(text) {
    const textarea = document.createElement('textarea');
    textarea.value = text;
    textarea.style.position = 'fixed';
    textarea.style.opacity = '0';
    document.body.appendChild(textarea);
    textarea.select();
    
    try {
        document.execCommand('copy');
        showNotification('Copied to clipboard!', 'success');
    } catch (err) {
        showNotification('Failed to copy', 'error');
    } finally {
        document.body.removeChild(textarea);
    }
}

/**
 * Show notification toast
 */
function showNotification(message, type = 'info') {
    const notification = document.createElement('div');
    notification.className = `notification notification-${type}`;
    notification.textContent = message;
    
    // Create styles if they don't exist
    if (!document.getElementById('notification-styles')) {
        const style = document.createElement('style');
        style.id = 'notification-styles';
        style.textContent = `
            .notification {
                position: fixed;
                bottom: 20px;
                right: 20px;
                padding: 12px 20px;
                border-radius: 4px;
                color: white;
                font-weight: 500;
                z-index: 9999;
                animation: slideIn 0.3s ease-out;
            }
            
            .notification-success {
                background-color: #34a853;
            }
            
            .notification-error {
                background-color: #d33b27;
            }
            
            .notification-info {
                background-color: #1a73e8;
            }
            
            @keyframes slideIn {
                from {
                    transform: translateX(400px);
                    opacity: 0;
                }
                to {
                    transform: translateX(0);
                    opacity: 1;
                }
            }
        `;
        document.head.appendChild(style);
    }
    
    document.body.appendChild(notification);
    
    // Remove after 3 seconds
    setTimeout(() => {
        notification.style.animation = 'slideOut 0.3s ease-in forwards';
        setTimeout(() => {
            document.body.removeChild(notification);
        }, 300);
    }, 3000);
}

/**
 * Add external links to open in new window
 */
window.addEventListener('load', function() {
    const links = document.querySelectorAll('a[target="_blank"]');
    
    links.forEach(link => {
        // Add visual indicator for external links
        if (!link.querySelector('svg')) {
            link.style.position = 'relative';
        }
    });
});

/**
 * Add keyboard shortcuts
 */
document.addEventListener('keydown', function(e) {
    // Alt + H: Go to Home/Hero section
    if (e.altKey && e.key === 'h') {
        document.querySelector('.hero').scrollIntoView({ behavior: 'smooth' });
        e.preventDefault();
    }
    
    // Alt + D: Go to Documentation
    if (e.altKey && e.key === 'd') {
        const doc = document.getElementById('documentation');
        if (doc) {
            doc.scrollIntoView({ behavior: 'smooth' });
            e.preventDefault();
        }
    }
});

/**
 * Dynamic theme switcher
 */
function toggleTheme() {
    const html = document.documentElement;
    const currentTheme = html.getAttribute('data-theme');
    const newTheme = currentTheme === 'dark' ? 'light' : 'dark';
    
    html.setAttribute('data-theme', newTheme);
    localStorage.setItem('theme', newTheme);
}

/**
 * Initialize theme from localStorage
 */
function initializeTheme() {
    const savedTheme = localStorage.getItem('theme') || 'light';
    document.documentElement.setAttribute('data-theme', savedTheme);
}

/**
 * Smooth scroll polyfill for older browsers
 */
if (!('scrollBehavior' in document.documentElement.style)) {
    function smoothScrollPolyfill(element) {
        const target = element.getAttribute('href');
        if (!target.startsWith('#')) return;
        
        const destination = document.querySelector(target);
        if (!destination) return;
        
        const start = window.scrollY;
        const end = destination.getBoundingClientRect().top + start;
        const duration = 1000;
        let start_time = null;
        
        function easeInOutQuad(t, b, c, d) {
            t /= d / 2;
            if (t < 1) return c / 2 * t * t + b;
            t--;
            return -c / 2 * (t * (t - 2) - 1) + b;
        }
        
        function scroll(timestamp) {
            if (!start_time) start_time = timestamp;
            const elapsed = timestamp - start_time;
            const position = easeInOutQuad(elapsed, start, end - start, duration);
            
            window.scrollTo(0, position);
            
            if (elapsed < duration) {
                requestAnimationFrame(scroll);
            }
        }
        
        requestAnimationFrame(scroll);
    }
}

/**
 * Log system information
 */
function logSystemInfo() {
    console.log('%c=== CyberOS Dashboard System Info ===', 'color: #1a73e8; font-weight: bold; font-size: 14px;');
    console.log('Version: 0.1.0 (Alpha - Genesis)');
    console.log('Release Date: February 28, 2025');
    console.log('Repository: https://github.com/XL-Elite/CyberOS');
    console.log('Browser: ' + navigator.userAgent);
    console.log('Viewport: ' + window.innerWidth + 'x' + window.innerHeight);
    console.log('%c======================================', 'color: #1a73e8; font-weight: bold;');
}

// Log system info on page load
logSystemInfo();

/**
 * Performance monitoring
 */
window.addEventListener('load', function() {
    if (window.performance && window.performance.timing) {
        const perfData = window.performance.timing;
        const pageLoadTime = perfData.loadEventEnd - perfData.navigationStart;
        console.log('Page Load Time: ' + pageLoadTime + 'ms');
    }
});

/**
 * Service Worker Registration (if available)
 */
if ('serviceWorker' in navigator) {
    // Service worker registration can be added here in the future
    // navigator.serviceWorker.register('sw.js').then(reg => {
    //     console.log('Service Worker registered', reg);
    // });
}

/**
 * Utility: Get build status
 */
function getBuildStatus() {
    return {
        version: '0.1.0-alpha',
        status: 'in-progress',
        completionPercentage: 60,
        lastUpdate: new Date().toLocaleString()
    };
}

/**
 * Utility: Format file size
 */
function formatFileSize(bytes) {
    if (bytes === 0) return '0 Bytes';
    const k = 1024;
    const sizes = ['Bytes', 'KB', 'MB', 'GB'];
    const i = Math.floor(Math.log(bytes) / Math.log(k));
    return Math.round((bytes / Math.pow(k, i)) * 100) / 100 + ' ' + sizes[i];
}

/**
 * Utility: Format date
 */
function formatDate(date) {
    const options = { year: 'numeric', month: 'long', day: 'numeric' };
    return new Date(date).toLocaleDateString(undefined, options);
}

/**
 * Export functions for external use
 */
window.CyberOS = {
    copyToClipboard: copyToClipboard,
    toggleTheme: toggleTheme,
    getBuildStatus: getBuildStatus,
    formatFileSize: formatFileSize,
    formatDate: formatDate
};

console.log('CyberOS utilities loaded. Access via window.CyberOS');

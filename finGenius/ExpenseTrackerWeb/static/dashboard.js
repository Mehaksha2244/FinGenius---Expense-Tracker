// Common dashboard functions

// Show notification message
function showNotification(message, type = 'info') {
    // Create notification element
    const notification = document.createElement('div');
    notification.className = `notification notification-${type}`;
    notification.innerHTML = `
        <div class="notification-content">
            <span class="notification-message">${message}</span>
            <button class="notification-close" onclick="this.parentElement.parentElement.remove()">&times;</button>
        </div>
    `;

    // Add to document
    document.body.appendChild(notification);

    // Auto remove after 3 seconds
    setTimeout(() => {
        if (notification.parentElement) {
            notification.remove();
        }
    }, 3000);
}

// Format currency
function formatCurrency(amount, currency = '₹') {
    return `${currency}${parseFloat(amount).toFixed(2)}`;
}

// Get current theme - Default to DARK
function getCurrentTheme() {
    return localStorage.getItem('fingenius-theme') || 'dark';
}

// Apply theme
function applyTheme(theme) {
    document.documentElement.setAttribute('data-theme', theme);
    localStorage.setItem('fingenius-theme', theme);
}

// Initialize theme on page load
document.addEventListener('DOMContentLoaded', function () {
    const savedTheme = getCurrentTheme();
    applyTheme(savedTheme);

    // Initialize Scroll Reveal
    initScrollReveal();

    // Initialize CountUp for stats
    initCountUp();

    // Check for success alerts to trigger confetti
    const successAlert = document.querySelector('.alert-success');
    if (successAlert) {
        createConfetti();
    }
});

// Scroll Reveal Animation with Intersection Observer
function initScrollReveal() {
    const observer = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.classList.add('active');
            }
        });
    }, {
        threshold: 0.1,
        rootMargin: "0px 0px -50px 0px"
    });

    document.querySelectorAll('.reveal-on-scroll').forEach((elem) => {
        observer.observe(elem);
    });
}

// Count Up Animation
function animateValue(obj, start, end, duration, currency = '') {
    let startTimestamp = null;
    const step = (timestamp) => {
        if (!startTimestamp) startTimestamp = timestamp;
        const progress = Math.min((timestamp - startTimestamp) / duration, 1);
        const value = progress * (end - start) + start;

        // Format with commas and 2 decimal places if it's a float
        let formattedValue = value.toLocaleString(undefined, {
            minimumFractionDigits: 2,
            maximumFractionDigits: 2
        });

        // Remove .00 if original was integer-like (simplified check)
        if (end % 1 === 0) {
            formattedValue = Math.floor(value).toLocaleString();
        }

        obj.innerHTML = currency + formattedValue;
        if (progress < 1) {
            window.requestAnimationFrame(step);
        }
    };
    window.requestAnimationFrame(step);
}

function initCountUp() {
    const statValues = document.querySelectorAll('.count-up');
    statValues.forEach(el => {
        const target = parseFloat(el.getAttribute('data-target'));
        const currency = el.getAttribute('data-currency') || '';
        if (!isNaN(target)) {
            animateValue(el, 0, target, 1500, currency);
        }
    });
}

// Confetti Animation
function createConfetti() {
    const colors = ['#ff0000', '#00ff00', '#0000ff', '#ffff00', '#00ffff', '#ff00ff'];
    for (let i = 0; i < 50; i++) {
        const confetti = document.createElement('div');
        confetti.className = 'confetti';
        confetti.style.left = Math.random() * 100 + 'vw';
        confetti.style.backgroundColor = colors[Math.floor(Math.random() * colors.length)];
        confetti.style.animationDuration = (Math.random() * 2 + 2) + 's';
        confetti.style.opacity = Math.random();
        document.body.appendChild(confetti);

        // Clean up
        setTimeout(() => {
            confetti.remove();
        }, 4000);
    }
}

// Chart.js Global Defaults for Animation
if (window.Chart) {
    Chart.defaults.animation.duration = 2000;
    Chart.defaults.animation.easing = 'easeOutQuart';
}

// Export functions
window.showNotification = showNotification;
window.formatCurrency = formatCurrency;
window.getCurrentTheme = getCurrentTheme;
window.applyTheme = applyTheme;
window.createConfetti = createConfetti;

// Floating Background Animation
class FloatingBackground {
    constructor() {
        this.container = document.getElementById('floating-background');
        this.items = ['💰', '💸', '💳', '🧾', '📊', '💹', '🏦', '💎', '🪙', '📐', '✒️', '📅', '💵', '💶', '💷'];
        this.floatingElements = [];
        this.itemCount = 80; // Increased count
        this.radius = 25; // approx radius of items

        if (this.container) {
            this.init();
        }
    }

    init() {
        this.container.innerHTML = '';
        this.floatingElements = [];

        // Create elements
        for (let i = 0; i < this.itemCount; i++) {
            this.createItem();
        }

        this.animate();
        window.addEventListener('resize', () => {
            this.handleResize();
        });
    }

    createItem() {
        const el = document.createElement('div');
        el.className = 'floating-item';
        el.textContent = this.items[Math.floor(Math.random() * this.items.length)];

        let x, y;
        const width = window.innerWidth;
        const height = window.innerHeight;

        // Corner bias logic for nice distribution
        if (Math.random() > 0.4) {
            const corner = Math.floor(Math.random() * 4);
            switch (corner) {
                case 0: x = Math.random() * (width * 0.3); y = Math.random() * (height * 0.3); break;
                case 1: x = width - Math.random() * (width * 0.3); y = Math.random() * (height * 0.3); break;
                case 2: x = Math.random() * (width * 0.3); y = height - Math.random() * (height * 0.3); break;
                case 3: x = width - Math.random() * (width * 0.3); y = height - Math.random() * (height * 0.3); break;
            }
        } else {
            x = Math.random() * (width - 60);
            y = Math.random() * (height - 60);
        }

        const speed = 0.2 + Math.random() * 0.6; // Slower, calmer movement
        const angle = Math.random() * Math.PI * 2;

        el.style.left = `${x}px`;
        el.style.top = `${y}px`;
        this.container.appendChild(el);

        this.floatingElements.push({
            element: el,
            x: x,
            y: y,
            vx: Math.cos(angle) * speed,
            vy: Math.sin(angle) * speed,
            rotation: Math.random() * 360,
            rotSpeed: (Math.random() - 0.5) * 2,
            radius: this.radius
        });
    }

    animate() {
        const width = window.innerWidth;
        const height = window.innerHeight;

        // Collision logic
        for (let i = 0; i < this.floatingElements.length; i++) {
            let item = this.floatingElements[i];

            // 1. Update Position
            item.x += item.vx;
            item.y += item.vy;
            item.rotation += item.rotSpeed;

            // 2. Wall Collisions
            // Use a slightly smaller boundary to avoid sticking to exact edges
            if (item.x <= 0) {
                item.vx = Math.abs(item.vx) * (0.8 + Math.random() * 0.4);
                item.x = 0;
            } else if (item.x >= width - 40) {
                item.vx = -Math.abs(item.vx) * (0.8 + Math.random() * 0.4);
                item.x = width - 40;
            }

            if (item.y <= 0) {
                item.vy = Math.abs(item.vy) * (0.8 + Math.random() * 0.4);
                item.y = 0;
            } else if (item.y >= height - 40) {
                item.vy = -Math.abs(item.vy) * (0.8 + Math.random() * 0.4);
                item.y = height - 40;
            }

            // 3. Obstacle Collisions - REMOVED for global smoothness (pass through)

            // 4. Peer Collisions - REMOVED per user request to allow overlapping

            // Apply
            item.element.style.transform = `translate(${item.x}px, ${item.y}px) rotate(${item.rotation}deg)`;
        }

        requestAnimationFrame(() => this.animate());
    }

    handleResize() {
        // Optional: Reset positions if window gets too small, or just let them bounce back naturally
    }
}

// Initialize floating background on load
document.addEventListener('DOMContentLoaded', function () {
    new FloatingBackground();
});
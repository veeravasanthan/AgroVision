// Modern JavaScript for AgroVision - No image dependencies
document.addEventListener('DOMContentLoaded', function() {
    // Mobile menu functionality
    const mobileMenu = document.querySelector('.mobile-menu');
    const navLinks = document.querySelector('.nav-links');
    
    if (mobileMenu) {
        mobileMenu.addEventListener('click', function() {
            navLinks.classList.toggle('active');
            this.classList.toggle('active');
        });
    }
    
    // Header scroll effect
    const header = document.querySelector('header');
    window.addEventListener('scroll', function() {
        if (window.scrollY > 100) {
            header.classList.add('scrolled');
        } else {
            header.classList.remove('scrolled');
        }
    });
    
    // Smooth scrolling for anchor links
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function (e) {
            e.preventDefault();
            const target = document.querySelector(this.getAttribute('href'));
            if (target) {
                target.scrollIntoView({
                    behavior: 'smooth',
                    block: 'start'
                });
                
                // Close mobile menu if open
                if (navLinks.classList.contains('active')) {
                    navLinks.classList.remove('active');
                    mobileMenu.classList.remove('active');
                }
            }
        });
    });
    
    // Enhanced form validation
    const forms = document.querySelectorAll('form');
    forms.forEach(form => {
        form.addEventListener('submit', function(e) {
            const inputs = form.querySelectorAll('input[required]');
            let valid = true;
            
            inputs.forEach(input => {
                if (!input.value.trim()) {
                    valid = false;
                    showInputError(input, 'This field is required');
                } else if (input.type === 'number') {
                    const value = parseFloat(input.value);
                    const min = parseFloat(input.min);
                    const max = parseFloat(input.max);
                    
                    if (min && value < min) {
                        showInputError(input, `Value must be at least ${min}`);
                        valid = false;
                    } else if (max && value > max) {
                        showInputError(input, `Value must be at most ${max}`);
                        valid = false;
                    } else {
                        clearInputError(input);
                    }
                } else {
                    clearInputError(input);
                }
            });
            
            if (!valid) {
                e.preventDefault();
            }
        });
    });
    
    // Input validation helpers
    function showInputError(input, message) {
        input.style.borderColor = 'var(--accent)';
        input.style.animation = 'shake 0.5s ease-in-out';
        
        // Remove existing error message
        const existingError = input.parentNode.querySelector('.error-message');
        if (existingError) {
            existingError.remove();
        }
        
        // Add error message
        const errorElement = document.createElement('div');
        errorElement.className = 'error-message';
        errorElement.style.color = 'var(--accent)';
        errorElement.style.fontSize = '0.8rem';
        errorElement.style.marginTop = '0.25rem';
        errorElement.textContent = message;
        input.parentNode.appendChild(errorElement);
        
        setTimeout(() => {
            input.style.animation = '';
        }, 500);
    }
    
    function clearInputError(input) {
        input.style.borderColor = '';
        const errorElement = input.parentNode.querySelector('.error-message');
        if (errorElement) {
            errorElement.remove();
        }
    }
    
    // Add real-time validation
    document.querySelectorAll('input[required]').forEach(input => {
        input.addEventListener('blur', function() {
            if (!this.value.trim()) {
                showInputError(this, 'This field is required');
            } else {
                clearInputError(this);
            }
        });
        
        input.addEventListener('input', function() {
            if (this.value.trim()) {
                clearInputError(this);
            }
        });
    });
    
    // Add loading state to buttons
    document.querySelectorAll('.btn, .submit-btn, .action-btn').forEach(button => {
        button.addEventListener('click', function() {
            if (!this.classList.contains('loading')) {
                this.classList.add('loading');
                setTimeout(() => {
                    this.classList.remove('loading');
                }, 2000);
            }
        });
    });
    
    // Intersection Observer for animations
    const observerOptions = {
        threshold: 0.1,
        rootMargin: '0px 0px -50px 0px'
    };
    
    const observer = new IntersectionObserver(function(entries) {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.classList.add('fade-in');
            }
        });
    }, observerOptions);
    
    // Observe elements for animation
    document.querySelectorAll('.feature-card, .step, .form-container, .result-container, .parameter-card').forEach(el => {
        observer.observe(el);
    });
    
    // Add floating animation to hero cards
    const floatingCards = document.querySelectorAll('.floating-card');
    floatingCards.forEach((card, index) => {
        card.style.animationDelay = `${index * 0.5}s`;
    });
});

// Add shake animation for form validation
const style = document.createElement('style');
style.textContent = `
    @keyframes shake {
        0%, 100% { transform: translateX(0); }
        25% { transform: translateX(-5px); }
        75% { transform: translateX(5px); }
    }
    
    .btn.loading, .submit-btn.loading, .action-btn.loading {
        position: relative;
        color: transparent;
    }
    
    .btn.loading::after, .submit-btn.loading::after, .action-btn.loading::after {
        content: '';
        position: absolute;
        width: 20px;
        height: 20px;
        top: 50%;
        left: 50%;
        margin: -10px 0 0 -10px;
        border: 2px solid transparent;
        border-top: 2px solid currentColor;
        border-radius: 50%;
        animation: spin 1s linear infinite;
    }
`;
document.head.appendChild(style);

// Enhanced form handling for prediction page
function enhancePredictionForm() {
    const form = document.getElementById('predictionForm');
    if (form) {
        // Add input value validation and suggestions
        const inputs = form.querySelectorAll('input[type="number"]');
        inputs.forEach(input => {
            input.addEventListener('input', function() {
                const value = parseFloat(this.value);
                if (value < 0) this.value = 0;
                
                // Add visual feedback for good values
                if (this.value.trim() && !isNaN(value)) {
                    this.style.borderColor = 'var(--primary)';
                    this.style.background = 'rgba(0, 200, 151, 0.05)';
                } else {
                    this.style.borderColor = '';
                    this.style.background = '';
                }
            });
        });
    }
}

// Initialize enhancement when DOM is ready
if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', enhancePredictionForm);
} else {
    enhancePredictionForm();
}
// Smooth scrolling for navigation links
document.addEventListener('DOMContentLoaded', function() {
    // Smooth scrolling for nav links
    const navLinks = document.querySelectorAll('.nav-links a');
    
    navLinks.forEach(link => {
        const href = link.getAttribute('href');
        
        // Only add click handler for internal anchor links
        if (href && href.startsWith('#')) {
            link.addEventListener('click', function(e) {
                e.preventDefault();
                console.log('Preventing default for anchor link:', href);
                
                const targetSection = document.querySelector(href);
                
                if (targetSection) {
                    const headerHeight = document.querySelector('.nav-container').offsetHeight;
                    const offsetTop = targetSection.offsetTop - headerHeight;
                    
                    window.scrollTo({
                        top: offsetTop,
                        behavior: 'smooth'
                    });
                    
                    // Update active link
                    navLinks.forEach(link => link.classList.remove('active'));
                    this.classList.add('active');
                }
            });
        } else {
            console.log('Skipping event listener for external link:', href);
        }
    });
    
    // Update active nav link on scroll
    function updateActiveNavLink() {
        const sections = document.querySelectorAll('section');
        const scrollPosition = window.scrollY + 100;
        
        sections.forEach(section => {
            const sectionTop = section.offsetTop;
            const sectionHeight = section.offsetHeight;
            const sectionId = section.getAttribute('id');
            
            if (scrollPosition >= sectionTop && scrollPosition < sectionTop + sectionHeight) {
                navLinks.forEach(link => {
                    link.classList.remove('active');
                    if (link.getAttribute('href') === `#${sectionId}`) {
                        link.classList.add('active');
                    }
                });
            }
        });
    }
    
    window.addEventListener('scroll', updateActiveNavLink);
    
    // Resume toggle functionality
    const resumeToggleBtn = document.getElementById('resume-toggle-btn');
    const resumeContent = document.getElementById('resume-content');
    
    if (resumeToggleBtn && resumeContent) {
        resumeToggleBtn.addEventListener('click', function() {
            const isVisible = resumeContent.style.display !== 'none';
            
            if (isVisible) {
                resumeContent.style.display = 'none';
                this.textContent = 'View Resume';
            } else {
                resumeContent.style.display = 'block';
                this.textContent = 'Hide Resume';
            }
        });
    }
    
    // Mobile menu functionality
    const mobileMenuBtn = document.querySelector('.mobile-menu-btn');
    const mobileNavLinks = document.querySelector('.nav-links');
    
    if (mobileMenuBtn && mobileNavLinks) {
        mobileMenuBtn.addEventListener('click', function() {
            mobileNavLinks.classList.toggle('active');
            this.classList.toggle('active');
        });
        
        // Close mobile menu when clicking on a nav link
        mobileNavLinks.querySelectorAll('a').forEach(link => {
            link.addEventListener('click', function() {
                mobileNavLinks.classList.remove('active');
                mobileMenuBtn.classList.remove('active');
            });
        });
        
        // Close mobile menu when clicking outside
        document.addEventListener('click', function(e) {
            if (!mobileMenuBtn.contains(e.target) && !mobileNavLinks.contains(e.target)) {
                mobileNavLinks.classList.remove('active');
                mobileMenuBtn.classList.remove('active');
            }
        });
    }
    
    // Intersection Observer for fade-in animations
    const observerOptions = {
        threshold: 0.1,
        rootMargin: '0px 0px -50px 0px'
    };
    
    const observer = new IntersectionObserver(function(entries) {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.classList.add('fade-in', 'visible');
            }
        });
    }, observerOptions);
    
    // Observe project cards
    const projectCards = document.querySelectorAll('.project-card');
    projectCards.forEach(card => {
        observer.observe(card);
    });
    
    // Observe sections for additional animations
    const sections = document.querySelectorAll('section');
    sections.forEach(section => {
        observer.observe(section);
    });
    
    // Add loading animation
    document.body.classList.add('loading');
    
    // Project card hover effects
    projectCards.forEach(card => {
        card.addEventListener('mouseenter', function() {
            this.style.transform = 'translateY(-8px) scale(1.02)';
        });
        
        card.addEventListener('mouseleave', function() {
            this.style.transform = 'translateY(0) scale(1)';
        });
    });
    
    // Add click tracking for project links
    const projectLinks = document.querySelectorAll('.project-link');
    projectLinks.forEach(link => {
        link.addEventListener('click', function(e) {
            // Could add analytics tracking here
            console.log('Project link clicked:', this.href);
        });
    });
    
    // Header background on scroll
    const header = document.querySelector('header');
    function updateHeader() {
        if (window.scrollY > 50) {
            header.style.backgroundColor = 'rgba(15, 23, 42, 0.98)';
            header.style.boxShadow = '0 2px 10px rgba(0, 0, 0, 0.1)';
        } else {
            header.style.backgroundColor = 'rgba(15, 23, 42, 0.95)';
            header.style.boxShadow = 'none';
        }
    }
    
    window.addEventListener('scroll', updateHeader);
    
    // Typing effect for hero subtitle (optional enhancement)
    const heroSubtitle = document.querySelector('.hero-subtitle');
    if (heroSubtitle) {
        const text = heroSubtitle.textContent;
        heroSubtitle.textContent = '';
        let i = 0;
        
        function typeWriter() {
            if (i < text.length) {
                heroSubtitle.textContent += text.charAt(i);
                i++;
                setTimeout(typeWriter, 100);
            }
        }
        
        // Start typing effect after a delay
        setTimeout(typeWriter, 1000);
    }
    
    // Add particle effect to hero (subtle)
    function createParticles() {
        const hero = document.querySelector('.hero');
        const particleCount = 20;
        
        for (let i = 0; i < particleCount; i++) {
            const particle = document.createElement('div');
            particle.className = 'particle';
            particle.style.cssText = `
                position: absolute;
                width: 4px;
                height: 4px;
                background: rgba(99, 102, 241, 0.3);
                border-radius: 50%;
                pointer-events: none;
                animation: float-particle ${Math.random() * 10 + 10}s linear infinite;
                left: ${Math.random() * 100}%;
                top: ${Math.random() * 100}%;
                animation-delay: ${Math.random() * 10}s;
            `;
            
            hero.appendChild(particle);
        }
    }
    
    createParticles();
    
    // Add CSS for particle animation
    const style = document.createElement('style');
    style.textContent = `
        @keyframes float-particle {
            0% {
                transform: translateY(0px) translateX(0px);
                opacity: 0;
            }
            10% {
                opacity: 1;
            }
            90% {
                opacity: 1;
            }
            100% {
                transform: translateY(-100vh) translateX(${Math.random() * 200 - 100}px);
                opacity: 0;
            }
        }
    `;
    document.head.appendChild(style);
    
    // Performance optimization: Debounce scroll events
    function debounce(func, wait) {
        let timeout;
        return function executedFunction(...args) {
            const later = () => {
                clearTimeout(timeout);
                func(...args);
            };
            clearTimeout(timeout);
            timeout = setTimeout(later, wait);
        };
    }
    
    // Apply debounced scroll handlers
    window.addEventListener('scroll', debounce(updateActiveNavLink, 10));
    window.addEventListener('scroll', debounce(updateHeader, 10));
    
    // Add keyboard navigation support
    document.addEventListener('keydown', function(e) {
        if (e.key === 'Escape') {
            // Close any open modals or menus (future enhancement)
            console.log('Escape pressed');
        }
    });
    
    // Add touch support for mobile
    let touchStartY = 0;
    document.addEventListener('touchstart', function(e) {
        touchStartY = e.touches[0].clientY;
    });
    
    document.addEventListener('touchmove', function(e) {
        const touchY = e.touches[0].clientY;
        const deltaY = touchStartY - touchY;
        
        // Prevent overscroll on mobile
        if ((window.scrollY === 0 && deltaY < 0) || 
            (window.innerHeight + window.scrollY >= document.body.offsetHeight && deltaY > 0)) {
            e.preventDefault();
        }
    }, { passive: false });
    
    console.log('Portfolio website loaded successfully!');
});
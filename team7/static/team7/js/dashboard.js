/**
 * Language Academy - Dashboard Page JavaScript
 * Dashboard-specific functionality and interactions
 */

// ==================== Sidebar Menu Handlers ====================
/**
 * Initialize sidebar menu item click handlers
 */
function initializeSidebarMenu() {
    const menuItems = document.querySelectorAll('.menu-item');
    
    menuItems.forEach(item => {
        item.addEventListener('click', function() {
            // Remove active class from all items
            menuItems.forEach(i => i.classList.remove('active'));
            // Add active class to clicked item
            this.classList.add('active');
            
            const menuText = this.querySelector('span').textContent;
            console.log('Navigating to:', menuText);
        });
    });
}

// ==================== Start Exam Button Handlers ====================
/**
 * Initialize start exam button handlers
 */
function initializeStartExamButtons() {
    const startButtons = document.querySelectorAll('.btn-start');
    
    startButtons.forEach(button => {
        button.addEventListener('click', function() {
            const examType = this.closest('.access-card')?.querySelector('.access-title')?.textContent;
            console.log('Starting exam:', examType);
            
            // Add visual feedback
            this.style.transform = 'scale(0.95)';
            setTimeout(() => {
                this.style.transform = '';
            }, 150);
        });
    });
}

// ==================== Card Hover Effects ====================
/**
 * Initialize hover effects for dashboard cards
 */
function initializeCardHoverEffects() {
    const cards = document.querySelectorAll('.status-card, .chart-card, .exam-card, .stat-card');
    
    cards.forEach(card => {
        card.addEventListener('mouseenter', function() {
            this.style.transform = 'translateY(-4px)';
            this.style.transition = 'transform 0.3s ease';
        });
        
        card.addEventListener('mouseleave', function() {
            this.style.transform = 'translateY(0)';
        });
    });
}

// ==================== Intersection Observer ====================
/**
 * Initialize intersection observer for dashboard sections
 */
function initializeDashboardAnimations() {
    const observerOptions = {
        threshold: 0.1,
        rootMargin: '0px 0px -50px 0px'
    };

    const observerCallback = (entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.style.opacity = '1';
                entry.target.style.transform = 'translateY(0)';
            }
        });
    };

    const observer = new IntersectionObserver(observerCallback, observerOptions);

    // Observe sections for animation
    const sections = document.querySelectorAll(
        '.status-section, .charts-section, .exams-section, .access-section, .statistics-section'
    );
    
    sections.forEach(section => {
        section.style.opacity = '0';
        section.style.transform = 'translateY(20px)';
        section.style.transition = 'opacity 0.6s ease, transform 0.6s ease';
        observer.observe(section);
    });
}

// ==================== Exam Card Click Handlers ====================
/**
 * Initialize exam card click handlers
 */
function initializeExamCardHandlers() {
    const examCards = document.querySelectorAll('.exam-card');
    
    examCards.forEach(card => {
        card.addEventListener('click', function() {
            const examTitle = this.querySelector('.exam-title')?.textContent;
            const examScore = this.querySelector('.score-value')?.textContent;
            console.log('Viewing exam:', examTitle, 'Score:', examScore);
            
            // Add visual effect
            this.style.outline = '2px solid #587ce6';
            setTimeout(() => {
                this.style.outline = '';
            }, 500);
        });
    });
}

// ==================== Stat Card Click Handlers ====================
/**
 * Initialize stat card click handlers
 */
function initializeStatCardHandlers() {
    const statCards = document.querySelectorAll('.stat-card');
    
    statCards.forEach(card => {
        card.addEventListener('click', function() {
            const statTitle = this.querySelector('.stat-title')?.textContent;
            const statValue = this.querySelector('.stat-value')?.textContent;
            console.log('Viewing stat:', statTitle, 'Value:', statValue);
        });
    });
}

// ==================== Initialize Dashboard ====================
/**
 * Initialize all dashboard page specific functionality
 */
function initializeDashboardPage() {
    initializeSidebarMenu();
    initializeStartExamButtons();
    initializeCardHoverEffects();
    initializeDashboardAnimations();
    initializeExamCardHandlers();
    initializeStatCardHandlers();
}

// Run initialization when DOM is ready
document.addEventListener('DOMContentLoaded', initializeDashboardPage);

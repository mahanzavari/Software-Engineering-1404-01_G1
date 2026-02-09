/**
 * Language Academy - Exam Page JavaScript
 * Page-specific functionality for exams
 */

// ==================== Carousel Handlers ====================
/**
 * Initialize carousel functionality
 */
function initializeCarousels() {
    const speakingCarousel = document.getElementById('speakingCarousel');
    const writingCarousel = document.getElementById('writingCarousel');
    
    if (speakingCarousel) {
        setupCarouselControls('speakingCarousel');
    }
    
    if (writingCarousel) {
        setupCarouselControls('writingCarousel');
    }
}

/**
 * Setup carousel navigation controls
 */
function setupCarouselControls(carouselId) {
    const carousel = document.getElementById(carouselId);
    if (!carousel) return;
    
    const cards = carousel.querySelectorAll('.exam-card');
    const cardWidth = 530; // Active card width
    const gap = 24; // Gap between cards
    
    window[`move${carouselId}`] = function(direction) {
        const currentScroll = carousel.scrollLeft;
        const moveDistance = cardWidth + gap;
        
        if (direction > 0) {
            carousel.scrollLeft += moveDistance;
        } else {
            carousel.scrollLeft -= moveDistance;
        }
    };
}

/**
 * Move speaking carousel
 */
function moveSpeakingCarousel(direction) {
    const carousel = document.getElementById('speakingCarousel');
    if (!carousel) return;
    
    const moveDistance = 554; // Card width + gap
    if (direction > 0) {
        carousel.scrollLeft += moveDistance;
    } else {
        carousel.scrollLeft -= moveDistance;
    }
}

/**
 * Move writing carousel
 */
function moveWritingCarousel(direction) {
    const carousel = document.getElementById('writingCarousel');
    if (!carousel) return;
    
    const moveDistance = 554; // Card width + gap
    if (direction > 0) {
        carousel.scrollLeft += moveDistance;
    } else {
        carousel.scrollLeft -= moveDistance;
    }
}

// ==================== Exam Card Handlers ====================
/**
 * Initialize exam card click handlers
 */
function initializeExamCards() {
    const examCards = document.querySelectorAll('.exam-card');
    
    examCards.forEach(card => {
        card.addEventListener('click', function(e) {
            // Don't trigger if clicking the button
            if (e.target.closest('.card-button')) return;
            
            // Remove active class from all cards
            examCards.forEach(c => c.classList.remove('active-card'));
            c.classList.add('blur-card');
            
            // Add active class to clicked card
            this.classList.add('active-card');
            this.classList.remove('blur-card');
        });
    });
    
    // Initialize with first card active
    if (examCards.length > 0) {
        examCards[0].classList.add('active-card');
    }
}

/**
 * Initialize exam card button handlers
 */
function initializeExamButtons() {
    const examButtons = document.querySelectorAll('.card-button');
    
    examButtons.forEach(button => {
        button.addEventListener('click', function(e) {
            e.preventDefault();
            const examTitle = this.closest('.exam-card')?.querySelector('.card-title')?.textContent;
            console.log('Starting exam:', examTitle);
            
            // Add visual feedback
            this.style.transform = 'scale(0.95)';
            setTimeout(() => {
                this.style.transform = '';
            }, 150);
            
            // Navigate to exam (implement actual navigation)
            // window.location.href = `/exams/${examTitle}`;
        });
    });
}

// ==================== History Table Handlers ====================
/**
 * Initialize history table tab switching
 */
function initializeHistoryTabs() {
    const tabButtons = document.querySelectorAll('.tab-button');
    const tableRows = document.querySelectorAll('.table-row');
    
    tabButtons.forEach(button => {
        button.addEventListener('click', function() {
            // Remove active class from all tabs
            tabButtons.forEach(btn => btn.classList.remove('active'));
            // Add active class to clicked tab
            this.classList.add('active');
            
            const tabType = this.textContent.trim();
            console.log('Switched to:', tabType);
            
            // Filter table rows based on selected tab
            filterHistoryTable(tabType);
        });
    });
}

/**
 * Filter history table based on exam type
 */
function filterHistoryTable(examType) {
    const tableRows = document.querySelectorAll('.table-row');
    
    tableRows.forEach(row => {
        const rowType = row.querySelector('[data-exam-type]')?.getAttribute('data-exam-type');
        if (rowType === examType || examType === 'All') {
            row.style.display = 'grid';
        } else {
            row.style.display = 'none';
        }
    });
}

/**
 * Initialize view details button handlers
 */
function initializeViewButtons() {
    const viewButtons = document.querySelectorAll('.view-button');
    
    viewButtons.forEach(button => {
        button.addEventListener('click', function(e) {
            e.preventDefault();
            const row = this.closest('.table-row');
            const examTitle = row.querySelector('[data-title]')?.textContent;
            const score = row.querySelector('.score-badge')?.textContent;
            
            console.log('Viewing details:', examTitle, 'Score:', score);
            
            // Add visual feedback
            this.style.transform = 'scale(0.95)';
            setTimeout(() => {
                this.style.transform = '';
            }, 150);
            
            // Navigate to exam details (implement actual navigation)
            // window.location.href = `/exams/details/${examTitle}`;
        });
    });
}

// ==================== Pagination Handlers ====================
/**
 * Initialize pagination controls
 */
function initializePagination() {
    const paginationButtons = document.querySelectorAll('.pagination-button');
    
    paginationButtons.forEach(button => {
        button.addEventListener('click', function() {
            if (this.classList.contains('active')) return;
            
            // Remove active class from all buttons
            paginationButtons.forEach(btn => btn.classList.remove('active'));
            // Add active class to clicked button
            this.classList.add('active');
            
            const pageNum = this.textContent.trim();
            console.log('Navigating to page:', pageNum);
            
            // Scroll to top of history section
            document.querySelector('.history-section')?.scrollIntoView({ behavior: 'smooth' });
            
            // Load new page data (implement actual data loading)
        });
    });
}

// ==================== Start Exam Button Handlers ====================
/**
 * Initialize CTA button handlers
 */
function initializeCtaButtons() {
    const startExamButton = document.querySelector('.start-exam-button');
    const learnMoreButton = document.querySelector('.learn-more-button');
    
    if (startExamButton) {
        startExamButton.addEventListener('click', function() {
            const isAuthenticated = isUserAuthenticated();
            
            if (!isAuthenticated) {
                redirectToLogin();
            } else {
                // Scroll to exams section
                document.querySelector('.exams-section')?.scrollIntoView({ behavior: 'smooth' });
            }
        });
    }
    
    if (learnMoreButton) {
        learnMoreButton.addEventListener('click', function() {
            // Scroll to exams section
            document.querySelector('.exams-section')?.scrollIntoView({ behavior: 'smooth' });
        });
    }
}

// ==================== Chat Icon Handler ====================
/**
 * Initialize chat icon interaction
 */
function initializeChatIcon() {
    const chatIcon = document.querySelector('.chat-icon');
    
    if (chatIcon) {
        chatIcon.addEventListener('click', function() {
            console.log('Chat icon clicked');
            // Implement chat functionality
            // openChat();
        });
    }
}

// ==================== Initialize Exam Page ====================
/**
 * Initialize all exam page specific functionality
 */
function initializeExamPage() {
    initializeCarousels();
    initializeExamCards();
    initializeExamButtons();
    initializeHistoryTabs();
    initializeViewButtons();
    initializePagination();
    initializeCtaButtons();
    initializeChatIcon();
    initializeAnimations(['.hero-text', '.exam-card', '.history-container']);
}

// Run initialization when DOM is ready
document.addEventListener('DOMContentLoaded', initializeExamPage);

// Export for testing
if (typeof module !== 'undefined' && module.exports) {
    module.exports = {
        initializeCarousels,
        moveSpeakingCarousel,
        moveWritingCarousel,
        initializeExamCards,
        initializeExamButtons,
        initializeHistoryTabs,
        filterHistoryTable,
        initializeViewButtons,
        initializePagination,
        initializeCtaButtons,
        initializeChatIcon,
        initializeExamPage
    };
}

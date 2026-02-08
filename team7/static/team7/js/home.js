/**
 * Language Academy - Home Page JavaScript
 * Page-specific functionality and interactions
 */

// ==================== Initialize Home Page ====================
/**
 * Initialize all home page specific functionality
 */
function initializeHomePage() {
    initializeAnimations(['.feature-card', '.step-card', '.ai-content', '.ai-image-wrapper']);
}

// Run initialization when DOM is ready
document.addEventListener('DOMContentLoaded', initializeHomePage);

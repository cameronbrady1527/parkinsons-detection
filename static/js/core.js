// ===== GLOBAL VARIABLES =====
let currentFile = null;
let currentResults = null;

// Pagination variables
let currentPage = 1;
let resultsPerPage = 10;
let totalResults = 0;

// ===== DOM ELEMENTS =====
const elements = {
    // Status and UI
    statusIndicator: document.getElementById('statusIndicator'),
    statusDot: document.querySelector('.status-dot'),
    statusText: document.querySelector('.status-text'),
    
    // Upload elements
    uploadArea: document.getElementById('uploadArea'),
    fileInput: document.getElementById('fileInput'),
    uploadBtn: document.getElementById('uploadBtn'),
    
    // Results elements
    resultsSection: document.getElementById('resultsSection'),
    resultsSummary: document.getElementById('resultsSummary'),
    resultsGrid: document.getElementById('resultsGrid'),
    
    // Models elements
    modelsGrid: document.getElementById('modelsGrid'),
    
    // Modals
    loadingModal: document.getElementById('loadingModal'),
    successModal: document.getElementById('successModal'),
    errorModal: document.getElementById('errorModal'),
    errorMessage: document.getElementById('errorMessage'),
    progressFill: document.getElementById('progressFill'),
    
    // Demo button
    demoBtn: document.getElementById('demoBtn')
};

// ===== INITIALIZATION =====
document.addEventListener('DOMContentLoaded', function() {
    console.log('🚀 Parkinson\'s Detection Frontend Initialized');
    
    // Initialize the application
    initializeApp();
    
    // Add entrance animations
    addEntranceAnimations();
    
    // Set up global error handling
    setupErrorHandling();
});

// ===== APP INITIALIZATION =====
async function initializeApp() {
    try {
        // Check API health
        await checkAPIHealth();
        
        // Load model information
        await loadModelInfo();
        
        // Set up event listeners
        setupEventListeners();
        
        console.log('✅ App initialized successfully');
    } catch (error) {
        console.error('❌ App initialization failed:', error);
        showNotification('Failed to initialize application', 'error');
    }
}

// ===== EVENT LISTENERS =====
function setupEventListeners() {
    // File input change
    if (elements.fileInput) {
        elements.fileInput.addEventListener('change', handleFileSelect);
    }
    
    // Drag and drop events
    if (elements.uploadArea) {
        elements.uploadArea.addEventListener('dragover', handleDragOver);
        elements.uploadArea.addEventListener('dragleave', handleDragLeave);
        elements.uploadArea.addEventListener('drop', handleDrop);
    }
    
    // Global error handling
    window.addEventListener('error', handleGlobalError);
    window.addEventListener('unhandledrejection', handleUnhandledRejection);
}

// ===== GLOBAL FUNCTIONS (for HTML onclick) =====
window.ParkinsonsDetection = {
    runDemo,
    downloadSample,
    exportResults,
    newAnalysis,
    scrollToUpload,
    closeSuccessModal,
    closeErrorModal,
    handleUpload
};

// Make functions globally available for HTML onclick attributes
window.runDemo = runDemo;
window.downloadSample = downloadSample;
window.exportResults = exportResults;
window.newAnalysis = newAnalysis;
window.scrollToUpload = scrollToUpload;
window.closeSuccessModal = closeSuccessModal;
window.closeErrorModal = closeErrorModal;
window.handleUpload = handleUpload;
window.handleFileSelect = handleFileSelect;
window.toggleDemoDropdown = toggleDemoDropdown;
window.switchModel = switchModel;
window.changePage = changePage;
window.toggleModelBreakdown = toggleModelBreakdown;

// Initialize educational section when DOM is ready
document.addEventListener('DOMContentLoaded', function() {
    // Set up keyboard navigation for accessibility
    const tabs = document.querySelectorAll('.ide-tab');
    tabs.forEach((tab, index) => {
        tab.addEventListener('keydown', function(e) {
            if (e.key === 'ArrowRight' || e.key === 'ArrowLeft') {
                e.preventDefault();
                const direction = e.key === 'ArrowRight' ? 1 : -1;
                const nextIndex = (index + direction + tabs.length) % tabs.length;
                tabs[nextIndex].click();
                tabs[nextIndex].focus();
            }
        });
        
        // Make tabs focusable
        tab.setAttribute('tabindex', '0');
    });
});
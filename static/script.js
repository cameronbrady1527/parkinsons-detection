// ===== GLOBAL VARIABLES =====
let currentFile = null;
let currentResults = null;

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

// ===== API HEALTH CHECK =====
async function checkAPIHealth() {
    try {
        const response = await fetch('/health');
        const data = await response.json();
        
        if (response.ok && data.status === 'healthy') {
            updateStatus('healthy', 'API Connected');
            console.log('✅ API health check passed');
        } else {
            throw new Error('API not healthy');
        }
    } catch (error) {
        console.error('❌ API health check failed:', error);
        updateStatus('error', 'API Disconnected');
        throw error;
    }
}

// ===== STATUS UPDATES =====
function updateStatus(type, message) {
    if (elements.statusDot && elements.statusText) {
        elements.statusDot.className = `status-dot ${type}`;
        elements.statusText.textContent = message;
    }
}

// ===== MODEL INFORMATION =====
async function loadModelInfo() {
    try {
        const response = await fetch('/info');
        const data = await response.json();
        
        if (response.ok) {
            displayModelInfo(data);
            console.log('✅ Model info loaded');
        } else {
            throw new Error('Failed to load model info');
        }
    } catch (error) {
        console.error('❌ Failed to load model info:', error);
        displayModelError();
    }
}

function displayModelInfo(data) {
    if (!elements.modelsGrid) return;
    
    const models = data.models || [];
    
    if (models.length === 0) {
        elements.modelsGrid.innerHTML = `
            <div class="model-card">
                <div class="model-name">No Models Available</div>
                <p>No trained models found in the system.</p>
            </div>
        `;
        return;
    }
    
    const modelsHTML = models.map(model => `
        <div class="model-card">
            <div class="model-name">${model.name || 'Unknown Model'}</div>
            <div class="model-stats">
                <div class="stat">
                    <div class="stat-value">${(model.accuracy * 100).toFixed(1)}%</div>
                    <div class="stat-label">Accuracy</div>
                </div>
                <div class="stat">
                    <div class="stat-value">${model.precision ? (model.precision * 100).toFixed(1) : 'N/A'}%</div>
                    <div class="stat-label">Precision</div>
                </div>
                <div class="stat">
                    <div class="stat-value">${model.recall ? (model.recall * 100).toFixed(1) : 'N/A'}%</div>
                    <div class="stat-label">Recall</div>
                </div>
            </div>
        </div>
    `).join('');
    
    elements.modelsGrid.innerHTML = modelsHTML;
}

function displayModelError() {
    if (!elements.modelsGrid) return;
    
    elements.modelsGrid.innerHTML = `
        <div class="model-card">
            <div class="model-name">Error Loading Models</div>
            <p>Failed to load model information. Please try refreshing the page.</p>
        </div>
    `;
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

// ===== FILE HANDLING =====
function handleFileSelect(event) {
    const file = event.target.files[0];
    if (file) {
        processFile(file);
    }
}

function handleDragOver(event) {
    event.preventDefault();
    elements.uploadArea.classList.add('dragover');
}

function handleDragLeave(event) {
    event.preventDefault();
    elements.uploadArea.classList.remove('dragover');
}

function handleDrop(event) {
    event.preventDefault();
    elements.uploadArea.classList.remove('dragover');
    
    const files = event.dataTransfer.files;
    if (files.length > 0) {
        processFile(files[0]);
    }
}

function processFile(file) {
    // Validate file type
    if (!file.name.toLowerCase().endsWith('.csv')) {
        showNotification('Please select a CSV file', 'error');
        return;
    }
    
    // Validate file size (max 10MB)
    if (file.size > 10 * 1024 * 1024) {
        showNotification('File size must be less than 10MB', 'error');
        return;
    }
    
    currentFile = file;
    
    // Update UI
    elements.uploadArea.innerHTML = `
        <div class="upload-content">
            <div class="upload-icon">
                <i class="fas fa-check-circle" style="color: var(--success-color);"></i>
            </div>
            <h4>File Selected</h4>
            <p>${file.name}</p>
            <div class="file-info">
                <span>Size: ${(file.size / 1024).toFixed(1)} KB</span>
            </div>
        </div>
    `;
    
    // Enable upload button
    if (elements.uploadBtn) {
        elements.uploadBtn.disabled = false;
    }
    
    showNotification('File selected successfully', 'success');
}

// ===== UPLOAD FUNCTIONALITY =====
async function handleUpload() {
    if (!currentFile) {
        showNotification('Please select a file first', 'error');
        return;
    }
    
    try {
        // Show loading modal
        showLoadingModal();
        
        // Create FormData
        const formData = new FormData();
        formData.append('file', currentFile);
        
        // Simulate progress
        simulateProgress();
        
        // Make API request
        const response = await fetch('/predict', {
            method: 'POST',
            body: formData
        });
        
        const data = await response.json();
        
        if (response.ok) {
            currentResults = data;
            hideLoadingModal();
            showSuccessModal();
            displayResults(data);
            scrollToResults();
        } else {
            throw new Error(data.detail || 'Prediction failed');
        }
    } catch (error) {
        console.error('❌ Upload failed:', error);
        hideLoadingModal();
        showErrorModal(error.message);
    }
}

// ===== RESULTS DISPLAY =====
function displayResults(data) {
    if (!elements.resultsSection || !elements.resultsSummary || !elements.resultsGrid) return;
    
    // Show results section
    elements.resultsSection.style.display = 'block';
    
    // Display summary
    const summary = createResultsSummary(data);
    elements.resultsSummary.innerHTML = summary;
    
    // Display detailed results
    const results = createResultsGrid(data);
    elements.resultsGrid.innerHTML = results;
}

function createResultsSummary(data) {
    const predictions = data.predictions || [];
    const totalSamples = predictions.length;
    const positiveCount = predictions.filter(p => p.prediction === 1).length;
    const negativeCount = totalSamples - positiveCount;
    const avgConfidence = predictions.reduce((sum, p) => sum + p.confidence, 0) / totalSamples;
    
    return `
        <div class="summary-stats">
            <div class="summary-stat">
                <div class="summary-number">${totalSamples}</div>
                <div class="summary-label">Total Samples</div>
            </div>
            <div class="summary-stat">
                <div class="summary-number">${positiveCount}</div>
                <div class="summary-label">Positive Cases</div>
            </div>
            <div class="summary-stat">
                <div class="summary-number">${negativeCount}</div>
                <div class="summary-label">Negative Cases</div>
            </div>
            <div class="summary-stat">
                <div class="summary-number">${(avgConfidence * 100).toFixed(1)}%</div>
                <div class="summary-label">Avg Confidence</div>
            </div>
        </div>
        <div class="confidence-text">
            Analysis completed with ${(avgConfidence * 100).toFixed(1)}% average confidence
        </div>
    `;
}

function createResultsGrid(data) {
    const predictions = data.predictions || [];
    
    if (predictions.length === 0) {
        return '<p>No predictions available</p>';
    }
    
    return predictions.map((prediction, index) => {
        const isPositive = prediction.prediction === 1;
        const confidencePercent = (prediction.confidence * 100).toFixed(1);
        const probabilityWidth = prediction.confidence * 100;
        
        return `
            <div class="prediction-card">
                <div class="prediction-header">
                    <div class="prediction-title">Sample ${index + 1}</div>
                    <div class="prediction-badge ${isPositive ? 'positive' : 'negative'}">
                        ${isPositive ? 'Positive' : 'Negative'}
                    </div>
                </div>
                <div class="probability-bar">
                    <div class="probability-fill ${isPositive ? 'high-risk' : ''}" 
                         style="width: ${probabilityWidth}%"></div>
                </div>
                <div class="prediction-details">
                    <p><strong>Confidence:</strong> ${confidencePercent}%</p>
                    <p><strong>Prediction:</strong> ${isPositive ? 'Likely to have Parkinson\'s' : 'Likely healthy'}</p>
                </div>
            </div>
        `;
    }).join('');
}

// ===== DEMO FUNCTIONALITY =====
function runDemo() {
    // Create demo CSV data
    const demoCSV = `MDVP:Fo(Hz),MDVP:Fhi(Hz),MDVP:Flo(Hz),MDVP:Jitter(%),MDVP:Jitter(Abs),MDVP:RAP,MDVP:PPQ,Jitter:DDP,MDVP:Shimmer,MDVP:Shimmer(dB),Shimmer:APQ3,Shimmer:APQ5,MDVP:APQ,Shimmer:DDA,NHR,HNR,status,RPDE,DFA,spread1,spread2,D2,PPE
119.992,157.302,74.997,0.00784,0.00007,0.0037,0.00554,0.01109,0.04374,0.426,0.02182,0.0313,0.02971,0.06545,0.02211,21.033,0.414783,0.815285,-4.813031,0.266482,2.301442,0.284654
122.4,148.45,113.819,0.00968,0.00008,0.00465,0.00696,0.01394,0.06134,0.626,0.03134,0.04518,0.04368,0.09403,0.01929,19.085,0.458359,0.819521,-4.075192,0.33559,2.486855,0.368674
116.682,131.111,111.555,0.0105,0.00009,0.00544,0.00781,0.01633,0.05233,0.482,0.02757,0.03858,0.0359,0.0827,0.01309,20.651,0.429895,0.825288,-4.443179,0.311173,2.342259,0.332634`;

    // Create a file object from the CSV string
    const blob = new Blob([demoCSV], { type: 'text/csv' });
    const demoFile = new File([blob], 'demo_data.csv', { type: 'text/csv' });
    
    // Process the demo file
    currentFile = demoFile;
    
    // Update UI to show demo file
    elements.uploadArea.innerHTML = `
        <div class="upload-content">
            <div class="upload-icon">
                <i class="fas fa-play-circle" style="color: var(--primary-color);"></i>
            </div>
            <h4>Demo Data Loaded</h4>
            <p>demo_data.csv (3 samples)</p>
            <div class="file-info">
                <span>Demo data ready for analysis</span>
            </div>
        </div>
    `;
    
    // Enable upload button
    if (elements.uploadBtn) {
        elements.uploadBtn.disabled = false;
    }
    
    // Scroll to upload section
    scrollToUpload();
    
    showNotification('Demo data loaded successfully', 'success');
}

// ===== UTILITY FUNCTIONS =====
function scrollToUpload() {
    const uploadSection = document.getElementById('uploadSection');
    if (uploadSection) {
        uploadSection.scrollIntoView({ behavior: 'smooth' });
    }
}

function scrollToResults() {
    if (elements.resultsSection) {
        elements.resultsSection.scrollIntoView({ behavior: 'smooth' });
    }
}

function downloadSample() {
    const sampleCSV = `MDVP:Fo(Hz),MDVP:Fhi(Hz),MDVP:Flo(Hz),MDVP:Jitter(%),MDVP:Jitter(Abs),MDVP:RAP,MDVP:PPQ,Jitter:DDP,MDVP:Shimmer,MDVP:Shimmer(dB),Shimmer:APQ3,Shimmer:APQ5,MDVP:APQ,Shimmer:DDA,NHR,HNR,status,RPDE,DFA,spread1,spread2,D2,PPE
119.992,157.302,74.997,0.00784,0.00007,0.0037,0.00554,0.01109,0.04374,0.426,0.02182,0.0313,0.02971,0.06545,0.02211,21.033,0.414783,0.815285,-4.813031,0.266482,2.301442,0.284654
122.4,148.45,113.819,0.00968,0.00008,0.00465,0.00696,0.01394,0.06134,0.626,0.03134,0.04518,0.04368,0.09403,0.01929,19.085,0.458359,0.819521,-4.075192,0.33559,2.486855,0.368674
116.682,131.111,111.555,0.0105,0.00009,0.00544,0.00781,0.01633,0.05233,0.482,0.02757,0.03858,0.0359,0.0827,0.01309,20.651,0.429895,0.825288,-4.443179,0.311173,2.342259,0.332634`;

    const blob = new Blob([sampleCSV], { type: 'text/csv' });
    const url = window.URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = 'sample_parkinsons_data.csv';
    document.body.appendChild(a);
    a.click();
    document.body.removeChild(a);
    window.URL.revokeObjectURL(url);
    
    showNotification('Sample data downloaded', 'success');
}

function exportResults() {
    if (!currentResults) {
        showNotification('No results to export', 'error');
        return;
    }
    
    const resultsText = JSON.stringify(currentResults, null, 2);
    const blob = new Blob([resultsText], { type: 'application/json' });
    const url = window.URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = 'parkinsons_analysis_results.json';
    document.body.appendChild(a);
    a.click();
    document.body.removeChild(a);
    window.URL.revokeObjectURL(url);
    
    showNotification('Results exported successfully', 'success');
}

function newAnalysis() {
    // Reset file input
    if (elements.fileInput) {
        elements.fileInput.value = '';
    }
    
    // Reset upload area
    if (elements.uploadArea) {
        elements.uploadArea.innerHTML = `
            <div class="upload-content">
                <div class="upload-icon">
                    <i class="fas fa-cloud-upload-alt"></i>
                    <div class="upload-pulse"></div>
                </div>
                <h4>Drop your CSV file here</h4>
                <p>or click to browse files</p>
                <div class="file-requirements">
                    <span class="requirement">
                        <i class="fas fa-check"></i>
                        CSV format required
                    </span>
                    <span class="requirement">
                        <i class="fas fa-check"></i>
                        Voice measurement data
                    </span>
                    <span class="requirement">
                        <i class="fas fa-check"></i>
                        Secure processing
                    </span>
                </div>
            </div>
        `;
    }
    
    // Hide results section
    if (elements.resultsSection) {
        elements.resultsSection.style.display = 'none';
    }
    
    // Disable upload button
    if (elements.uploadBtn) {
        elements.uploadBtn.disabled = true;
    }
    
    // Reset variables
    currentFile = null;
    currentResults = null;
    
    // Scroll to upload section
    scrollToUpload();
    
    showNotification('Ready for new analysis', 'success');
}

// ===== MODAL FUNCTIONS =====
function showLoadingModal() {
    if (elements.loadingModal) {
        elements.loadingModal.classList.add('show');
    }
}

function hideLoadingModal() {
    if (elements.loadingModal) {
        elements.loadingModal.classList.remove('show');
    }
}

function showSuccessModal() {
    if (elements.successModal) {
        elements.successModal.classList.add('show');
    }
}

function hideSuccessModal() {
    if (elements.successModal) {
        elements.successModal.classList.remove('show');
    }
}

function showErrorModal(message) {
    if (elements.errorModal && elements.errorMessage) {
        elements.errorMessage.textContent = message || 'An error occurred during analysis. Please try again.';
        elements.errorModal.classList.add('show');
    }
}

function hideErrorModal() {
    if (elements.errorModal) {
        elements.errorModal.classList.remove('show');
    }
}

function closeSuccessModal() {
    hideSuccessModal();
}

function closeErrorModal() {
    hideErrorModal();
}

// ===== PROGRESS SIMULATION =====
function simulateProgress() {
    if (!elements.progressFill) return;
    
    let progress = 0;
    const interval = setInterval(() => {
        progress += Math.random() * 15;
        if (progress > 90) progress = 90;
        
        elements.progressFill.style.width = `${progress}%`;
        
        if (progress >= 90) {
            clearInterval(interval);
        }
    }, 200);
}

// ===== NOTIFICATIONS =====
function showNotification(message, type = 'info') {
    // Remove existing notifications
    const existingNotifications = document.querySelectorAll('.notification');
    existingNotifications.forEach(notification => notification.remove());
    
    // Create notification element
    const notification = document.createElement('div');
    notification.className = `notification ${type}`;
    
    // Set background color based on type
    let backgroundColor;
    let icon;
    
    switch (type) {
        case 'success':
            backgroundColor = 'var(--success-color)';
            icon = 'fas fa-check-circle';
            break;
        case 'error':
            backgroundColor = 'var(--danger-color)';
            icon = 'fas fa-exclamation-circle';
            break;
        case 'warning':
            backgroundColor = 'var(--warning-color)';
            icon = 'fas fa-exclamation-triangle';
            break;
        default:
            backgroundColor = 'var(--primary-color)';
            icon = 'fas fa-info-circle';
    }
    
    notification.style.background = backgroundColor;
    
    notification.innerHTML = `
        <div class="notification-content">
            <i class="${icon}"></i>
            <span>${message}</span>
        </div>
        <button class="notification-close" onclick="this.parentElement.remove()">
            <i class="fas fa-times"></i>
        </button>
    `;
    
    document.body.appendChild(notification);
    
    // Show notification
    setTimeout(() => {
        notification.classList.add('show');
    }, 100);
    
    // Auto-hide after 5 seconds
    setTimeout(() => {
        notification.classList.remove('show');
        setTimeout(() => {
            if (notification.parentElement) {
                notification.remove();
            }
        }, 300);
    }, 5000);
}

// ===== ANIMATIONS =====
function addEntranceAnimations() {
    const observerOptions = {
        threshold: 0.1,
        rootMargin: '0px 0px -50px 0px'
    };
    
    const observer = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.style.opacity = '1';
                entry.target.style.transform = 'translateY(0)';
            }
        });
    }, observerOptions);
    
    // Observe sections for entrance animations
    const sections = document.querySelectorAll('section');
    sections.forEach(section => {
        section.style.opacity = '0';
        section.style.transform = 'translateY(30px)';
        section.style.transition = 'opacity 0.6s ease, transform 0.6s ease';
        observer.observe(section);
    });
}

// ===== ERROR HANDLING =====
function setupErrorHandling() {
    window.addEventListener('error', handleGlobalError);
    window.addEventListener('unhandledrejection', handleUnhandledRejection);
}

function handleGlobalError(event) {
    console.error('Global error:', event.error);
    showNotification('An unexpected error occurred', 'error');
}

function handleUnhandledRejection(event) {
    console.error('Unhandled promise rejection:', event.reason);
    showNotification('An unexpected error occurred', 'error');
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
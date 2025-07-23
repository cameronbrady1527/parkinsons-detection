// ===== GLOBAL VARIABLES =====
let selectedFile = null;
let isProcessing = false;
const API_BASE_URL = window.location.origin;

// ===== DOM ELEMENTS =====
const elements = {
    // Header
    statusIndicator: document.getElementById('statusIndicator'),
    statusDot: document.querySelector('.status-dot'),
    statusText: document.querySelector('.status-text'),
    demoBtn: document.getElementById('demoBtn'),
    
    // Upload
    uploadArea: document.getElementById('uploadArea'),
    fileInput: document.getElementById('fileInput'),
    uploadBtn: document.getElementById('uploadBtn'),
    
    // Results
    resultsSection: document.getElementById('resultsSection'),
    resultsSummary: document.getElementById('resultsSummary'),
    resultsGrid: document.getElementById('resultsGrid'),
    
    // Models
    modelsGrid: document.getElementById('modelsGrid'),
    
    // Modals
    loadingModal: document.getElementById('loadingModal'),
    successModal: document.getElementById('successModal'),
    errorModal: document.getElementById('errorModal'),
    progressFill: document.getElementById('progressFill'),
    errorMessage: document.getElementById('errorMessage')
};

// ===== INITIALIZATION =====
document.addEventListener('DOMContentLoaded', function() {
    console.log('🚀 Initializing Parkinson\'s Detection App...');
    initializeApp();
});

async function initializeApp() {
    try {
        // Check API health
        await checkApiHealth();
        
        // Load model information
        await loadModelInfo();
        
        // Set up event listeners
        setupEventListeners();
        
        // Add entrance animations
        addEntranceAnimations();
        
        console.log('✅ App initialized successfully');
    } catch (error) {
        console.error('❌ App initialization failed:', error);
        showNotification('Failed to initialize application', 'error');
    }
}

// ===== API HEALTH CHECK =====
async function checkApiHealth() {
    try {
        const response = await fetch(`${API_BASE_URL}/health`, {
            method: 'GET',
            headers: { 'Content-Type': 'application/json' }
        });
        
        if (!response.ok) {
            throw new Error(`HTTP ${response.status}: ${response.statusText}`);
        }
        
        const data = await response.json();
        
        if (data.status === 'healthy') {
            updateStatus('healthy', 'API Ready');
            showNotification('API is healthy and ready', 'success');
        } else if (data.status === 'degraded') {
            updateStatus('warning', 'API Degraded');
            showNotification('API is running with limited functionality', 'warning');
        } else {
            updateStatus('error', 'API Error');
            showNotification('API is experiencing issues', 'error');
        }
        
        return data;
    } catch (error) {
        console.error('Health check failed:', error);
        updateStatus('error', 'Connection Error');
        showNotification('Cannot connect to API server', 'error');
        throw error;
    }
}

function updateStatus(status, text) {
    elements.statusDot.className = `status-dot ${status}`;
    elements.statusText.textContent = text;
}

// ===== MODEL INFORMATION =====
async function loadModelInfo() {
    try {
        const response = await fetch(`${API_BASE_URL}/info`, {
            method: 'GET',
            headers: { 'Content-Type': 'application/json' }
        });
        
        if (!response.ok) {
            throw new Error(`HTTP ${response.status}: ${response.statusText}`);
        }
        
        const data = await response.json();
        
        if (data.status === 'ready') {
            displayModelInfo(data);
        } else {
            elements.modelsGrid.innerHTML = `
                <div class="loading-models">
                    <div class="spinner"></div>
                    <p>${data.message || 'Loading model information...'}</p>
                </div>
            `;
        }
    } catch (error) {
        console.error('Failed to load model info:', error);
        elements.modelsGrid.innerHTML = `
            <div class="loading-models">
                <div class="spinner"></div>
                <p>Failed to load model information</p>
                <button class="btn-primary" onclick="loadModelInfo()">Retry</button>
            </div>
        `;
    }
}

function displayModelInfo(data) {
    const models = data.models || {};
    
    let html = '';
    
    // Display individual model information
    Object.entries(models).forEach(([modelName, modelData]) => {
        const accuracy = (modelData.cv_accuracy * 100).toFixed(1);
        const std = (modelData.cv_std * 100).toFixed(1);
        
        html += `
            <div class="model-card" data-aos="fade-up">
                <div class="model-name">${formatModelName(modelName)}</div>
                <div class="model-stats">
                    <div class="stat">
                        <div class="stat-value">${accuracy}%</div>
                        <div class="stat-label">Accuracy</div>
                    </div>
                    <div class="stat">
                        <div class="stat-value">±${std}%</div>
                        <div class="stat-label">Std Dev</div>
                    </div>
                    <div class="stat">
                        <div class="stat-value">${modelData.features_count}</div>
                        <div class="stat-label">Features</div>
                    </div>
                </div>
            </div>
        `;
    });
    
    elements.modelsGrid.innerHTML = html;
}

function formatModelName(name) {
    return name.split('_').map(word => 
        word.charAt(0).toUpperCase() + word.slice(1)
    ).join(' ');
}

// ===== EVENT LISTENERS =====
function setupEventListeners() {
    // File input change
    elements.fileInput.addEventListener('change', handleFileSelect);
    
    // Upload area interactions
    elements.uploadArea.addEventListener('dragover', handleDragOver);
    elements.uploadArea.addEventListener('dragleave', handleDragLeave);
    elements.uploadArea.addEventListener('drop', handleDrop);
    
    // Modal close handlers
    document.addEventListener('click', handleModalClose);
}

// ===== FILE HANDLING =====
function handleFileSelect(event) {
    const file = event.target.files[0];
    if (file && file.type === 'text/csv') {
        selectedFile = file;
        updateUploadArea(file.name);
        elements.uploadBtn.disabled = false;
        showNotification(`File selected: ${file.name}`, 'success');
    } else {
        showNotification('Please select a valid CSV file', 'error');
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
        const file = files[0];
        if (file.type === 'text/csv') {
            selectedFile = file;
            elements.fileInput.files = files;
            updateUploadArea(file.name);
            elements.uploadBtn.disabled = false;
            showNotification(`File dropped: ${file.name}`, 'success');
        } else {
            showNotification('Please drop a valid CSV file', 'error');
        }
    }
}

function updateUploadArea(fileName) {
    const uploadContent = elements.uploadArea.querySelector('.upload-content');
    uploadContent.innerHTML = `
        <div class="upload-icon">
            <i class="fas fa-file-csv"></i>
            <div class="upload-pulse"></div>
        </div>
        <h4>Selected: ${fileName}</h4>
        <p>Click to change file</p>
        <div class="file-requirements">
            <span class="requirement">
                <i class="fas fa-check"></i>
                File ready for analysis
            </span>
        </div>
    `;
}

// ===== UPLOAD PROCESSING =====
async function handleUpload() {
    if (!selectedFile) {
        showNotification('Please select a file first', 'error');
        return;
    }
    
    if (isProcessing) {
        showNotification('Analysis already in progress', 'warning');
        return;
    }
    
    isProcessing = true;
    showLoadingModal();
    updateUploadButton(true);
    
    try {
        const formData = new FormData();
        formData.append('file', selectedFile);
        
        // Simulate progress
        simulateProgress();
        
        const response = await fetch(`${API_BASE_URL}/predict`, {
            method: 'POST',
            body: formData
        });
        
        if (!response.ok) {
            const errorText = await response.text();
            throw new Error(`HTTP ${response.status}: ${errorText}`);
        }
        
        const data = await response.json();
        
        hideLoadingModal();
        showSuccessModal();
        
        // Small delay for modal display
        setTimeout(() => {
            hideSuccessModal();
            displayResults(data);
        }, 1500);
        
    } catch (error) {
        console.error('Upload failed:', error);
        hideLoadingModal();
        showErrorModal(error.message);
    } finally {
        isProcessing = false;
        updateUploadButton(false);
    }
}

function updateUploadButton(loading) {
    const btn = elements.uploadBtn;
    const icon = btn.querySelector('i');
    const text = btn.querySelector('span');
    const loadingSpinner = btn.querySelector('.btn-loading');
    
    if (loading) {
        icon.style.display = 'none';
        text.style.display = 'none';
        loadingSpinner.style.display = 'block';
        btn.disabled = true;
    } else {
        icon.style.display = 'inline-block';
        text.style.display = 'inline-block';
        loadingSpinner.style.display = 'none';
        btn.disabled = !selectedFile;
    }
}

// ===== RESULTS DISPLAY =====
function displayResults(data) {
    const predictions = data.predictions || {};
    const probabilities = data.probabilities || {};
    const sampleCount = data.sample_count || 0;
    
    // Update summary
    elements.resultsSummary.innerHTML = `
        <div class="summary-stats">
            <div class="summary-stat">
                <div class="summary-number">${sampleCount}</div>
                <div class="summary-label">Samples Analyzed</div>
            </div>
            <div class="summary-stat">
                <div class="summary-number">${Object.keys(predictions).length}</div>
                <div class="summary-label">Models Used</div>
            </div>
            <div class="summary-stat">
                <div class="summary-number">${data.features_used?.length || 0}</div>
                <div class="summary-label">Features</div>
            </div>
        </div>
    `;
    
    // Display predictions for each model
    let resultsHtml = '';
    
    Object.entries(predictions).forEach(([modelName, predictions], index) => {
        const modelProbs = probabilities[modelName] || [];
        
        resultsHtml += `
            <div class="prediction-card" data-aos="fade-up" data-aos-delay="${index * 100}">
                <div class="prediction-header">
                    <div class="prediction-title">${formatModelName(modelName)}</div>
                </div>
        `;
        
        if (predictions.length === 1) {
            // Single prediction
            const prediction = predictions[0];
            const probability = modelProbs[0] || 0;
            const isPositive = prediction === 1;
            
            resultsHtml += `
                <div class="prediction-result">
                    <span class="prediction-badge ${isPositive ? 'positive' : 'negative'}">
                        ${isPositive ? 'High Risk' : 'Low Risk'}
                    </span>
                    <div class="probability-bar">
                        <div class="probability-fill ${isPositive ? 'high-risk' : ''}" 
                             style="width: ${(probability * 100)}%"></div>
                    </div>
                    <p class="confidence-text">Confidence: ${(probability * 100).toFixed(1)}%</p>
                </div>
            `;
        } else {
            // Multiple predictions
            resultsHtml += '<div class="predictions-list">';
            predictions.forEach((prediction, index) => {
                const probability = modelProbs[index] || 0;
                const isPositive = prediction === 1;
                
                resultsHtml += `
                    <div class="prediction-item">
                        <div class="prediction-item-header">
                            <span class="prediction-badge ${isPositive ? 'positive' : 'negative'}">
                                Sample ${index + 1}: ${isPositive ? 'High Risk' : 'Low Risk'}
                            </span>
                        </div>
                        <div class="probability-bar">
                            <div class="probability-fill ${isPositive ? 'high-risk' : ''}" 
                                 style="width: ${(probability * 100)}%"></div>
                        </div>
                        <p class="confidence-text">Confidence: ${(probability * 100).toFixed(1)}%</p>
                    </div>
                `;
            });
            resultsHtml += '</div>';
        }
        
        resultsHtml += '</div>';
    });
    
    elements.resultsGrid.innerHTML = resultsHtml;
    elements.resultsSection.style.display = 'block';
    
    // Scroll to results with smooth animation
    elements.resultsSection.scrollIntoView({ 
        behavior: 'smooth', 
        block: 'start' 
    });
    
    // Store results for export
    window.lastResults = data;
}

// ===== DEMO FUNCTIONALITY =====
async function runDemo() {
    try {
        showNotification('Loading demo data...', 'info');
        
        // Create a demo file from sample data
        const demoData = `name,MDVP:Fo(Hz),MDVP:Fhi(Hz),MDVP:Flo(Hz),MDVP:Jitter(%),MDVP:Jitter(Abs),MDVP:RAP,MDVP:PPQ,Jitter:DDP,MDVP:Shimmer,MDVP:Shimmer(dB),Shimmer:APQ3,Shimmer:APQ5,MDVP:APQ,Shimmer:DDA,NHR,HNR,status,RPDE,DFA,spread1,spread2,D2,PPE
demo_sample,119.992,157.302,74.997,0.00784,0.00007,0.0037,0.00554,0.01109,0.04374,0.426,0.02182,0.0313,0.02971,0.06545,0.02211,21.033,1,0.414783,0.815285,-4.813031,0.266482,2.301442,0.284654`;
        
        const blob = new Blob([demoData], { type: 'text/csv' });
        const file = new File([blob], 'demo_data.csv', { type: 'text/csv' });
        
        selectedFile = file;
        updateUploadArea('demo_data.csv');
        elements.uploadBtn.disabled = false;
        
        // Scroll to upload section
        document.getElementById('uploadSection').scrollIntoView({ 
            behavior: 'smooth', 
            block: 'start' 
        });
        
        showNotification('Demo file loaded! Click "Analyze Data" to continue', 'success');
        
    } catch (error) {
        console.error('Demo failed:', error);
        showNotification('Failed to load demo', 'error');
    }
}

// ===== UTILITY FUNCTIONS =====
function downloadSample() {
    const link = document.createElement('a');
    link.href = `${API_BASE_URL}/static/sample_data.csv`;
    link.download = 'sample_data.csv';
    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);
    showNotification('Sample file downloaded', 'success');
}

function scrollToUpload() {
    document.getElementById('uploadSection').scrollIntoView({ 
        behavior: 'smooth', 
        block: 'start' 
    });
}

function exportResults() {
    if (!window.lastResults) {
        showNotification('No results to export', 'warning');
        return;
    }
    
    const dataStr = JSON.stringify(window.lastResults, null, 2);
    const dataBlob = new Blob([dataStr], { type: 'application/json' });
    const url = URL.createObjectURL(dataBlob);
    
    const link = document.createElement('a');
    link.href = url;
    link.download = 'parkinsons_analysis_results.json';
    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);
    URL.revokeObjectURL(url);
    
    showNotification('Results exported successfully', 'success');
}

function newAnalysis() {
    selectedFile = null;
    elements.fileInput.value = '';
    elements.uploadBtn.disabled = true;
    elements.resultsSection.style.display = 'none';
    
    // Reset upload area
    const uploadContent = elements.uploadArea.querySelector('.upload-content');
    uploadContent.innerHTML = `
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
    `;
    
    showNotification('Ready for new analysis', 'success');
}

// ===== MODAL FUNCTIONS =====
function showLoadingModal() {
    elements.loadingModal.classList.add('show');
    simulateProgress();
}

function hideLoadingModal() {
    elements.loadingModal.classList.remove('show');
}

function showSuccessModal() {
    elements.successModal.classList.add('show');
}

function hideSuccessModal() {
    elements.successModal.classList.remove('show');
}

function showErrorModal(message) {
    elements.errorMessage.textContent = message;
    elements.errorModal.classList.add('show');
}

function hideErrorModal() {
    elements.errorModal.classList.remove('show');
}

function closeSuccessModal() {
    hideSuccessModal();
}

function closeErrorModal() {
    hideErrorModal();
}

function handleModalClose(event) {
    if (event.target.classList.contains('modal')) {
        event.target.classList.remove('show');
    }
}

// ===== PROGRESS SIMULATION =====
function simulateProgress() {
    let progress = 0;
    const interval = setInterval(() => {
        progress += Math.random() * 15;
        if (progress > 90) progress = 90;
        
        if (elements.progressFill) {
            elements.progressFill.style.width = `${progress}%`;
        }
        
        if (progress >= 90) {
            clearInterval(interval);
        }
    }, 200);
}

// ===== ANIMATIONS =====
function addEntranceAnimations() {
    // Add entrance animations to elements
    const animatedElements = document.querySelectorAll('.hero-text, .hero-visual, .upload-container, .models-container, .features-container');
    
    animatedElements.forEach((element, index) => {
        element.style.opacity = '0';
        element.style.transform = 'translateY(30px)';
        
        setTimeout(() => {
            element.style.transition = 'all 0.6s ease';
            element.style.opacity = '1';
            element.style.transform = 'translateY(0)';
        }, index * 200);
    });
}

// ===== NOTIFICATIONS =====
function showNotification(message, type = 'info') {
    // Remove existing notifications
    const existingNotifications = document.querySelectorAll('.notification');
    existingNotifications.forEach(notification => notification.remove());
    
    // Create notification element
    const notification = document.createElement('div');
    notification.className = `notification notification-${type}`;
    notification.innerHTML = `
        <div class="notification-content">
            <i class="fas fa-${getNotificationIcon(type)}"></i>
            <span>${message}</span>
        </div>
        <button class="notification-close" onclick="this.parentElement.remove()">
            <i class="fas fa-times"></i>
        </button>
    `;
    
    // Add styles
    notification.style.cssText = `
        position: fixed;
        top: 20px;
        right: 20px;
        padding: 1rem 1.5rem;
        border-radius: 12px;
        color: white;
        font-weight: 500;
        z-index: 1001;
        transform: translateX(100%);
        transition: transform 0.3s ease;
        max-width: 400px;
        display: flex;
        align-items: center;
        justify-content: space-between;
        gap: 1rem;
        box-shadow: 0 10px 25px rgba(0, 0, 0, 0.2);
    `;
    
    // Set background color based on type
    const colors = {
        success: '#10b981',
        error: '#ef4444',
        warning: '#f59e0b',
        info: '#6366f1'
    };
    
    notification.style.background = colors[type] || colors.info;
    
    // Add to page
    document.body.appendChild(notification);
    
    // Animate in
    setTimeout(() => {
        notification.style.transform = 'translateX(0)';
    }, 100);
    
    // Remove after 5 seconds
    setTimeout(() => {
        notification.style.transform = 'translateX(100%)';
        setTimeout(() => {
            if (notification.parentElement) {
                notification.remove();
            }
        }, 300);
    }, 5000);
}

function getNotificationIcon(type) {
    const icons = {
        success: 'check-circle',
        error: 'exclamation-triangle',
        warning: 'exclamation-circle',
        info: 'info-circle'
    };
    return icons[type] || 'info-circle';
}

// ===== GLOBAL FUNCTIONS =====
window.ParkinsonsDetection = {
    uploadFile: handleUpload,
    checkHealth: checkApiHealth,
    loadModelInfo: loadModelInfo,
    showNotification: showNotification,
    runDemo: runDemo,
    exportResults: exportResults,
    newAnalysis: newAnalysis,
    downloadSample: downloadSample,
    scrollToUpload: scrollToUpload
};

// ===== ERROR HANDLING =====
window.addEventListener('error', function(event) {
    console.error('Global error:', event.error);
    showNotification('An unexpected error occurred', 'error');
});

window.addEventListener('unhandledrejection', function(event) {
    console.error('Unhandled promise rejection:', event.reason);
    showNotification('An unexpected error occurred', 'error');
}); 
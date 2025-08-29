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
    
    // Check if there's an error status
    if (data.status === 'error') {
        elements.modelsGrid.innerHTML = `
            <div class="model-card">
                <div class="model-name">⚠️ Model Loading Error</div>
                <p>${data.message || 'Failed to load model information'}</p>
                <div class="model-stats">
                    <div class="stat">
                        <div class="stat-value">--</div>
                        <div class="stat-label">Accuracy</div>
                    </div>
                    <div class="stat">
                        <div class="stat-value">--</div>
                        <div class="stat-label">Precision</div>
                    </div>
                    <div class="stat">
                        <div class="stat-value">--</div>
                        <div class="stat-label">Recall</div>
                    </div>
                </div>
                <p style="color: var(--gray-600); font-size: 0.875rem; margin-top: var(--spacing-md);">
                    The API is still functional for predictions, but model performance metrics are unavailable.
                </p>
            </div>
        `;
        return;
    }
    
    const models = data.models || {};
    const modelNames = Object.keys(models);
    
    if (modelNames.length === 0) {
        elements.modelsGrid.innerHTML = `
            <div class="model-card">
                <div class="model-name">No Models Available</div>
                <p>No trained models found in the system.</p>
            </div>
        `;
        return;
    }
    
    const modelsHTML = modelNames.map(modelName => {
        const model = models[modelName];
        return `
            <div class="model-card">
                <div class="model-name">${modelName.charAt(0).toUpperCase() + modelName.slice(1)} Model</div>
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
        `;
    }).join('');
    
    elements.modelsGrid.innerHTML = modelsHTML;
}

function displayModelError() {
    if (!elements.modelsGrid) return;
    
    elements.modelsGrid.innerHTML = `
        <div class="model-card">
            <div class="model-name">⚠️ Error Loading Models</div>
            <p>Failed to load model information. The API may still be starting up.</p>
            <div class="model-stats">
                <div class="stat">
                    <div class="stat-value">--</div>
                    <div class="stat-label">Accuracy</div>
                </div>
                <div class="stat">
                    <div class="stat-value">--</div>
                    <div class="stat-label">Precision</div>
                </div>
                <div class="stat">
                    <div class="stat-value">--</div>
                    <div class="stat-label">Recall</div>
                </div>
            </div>
            <button onclick="loadModelInfo()" style="margin-top: var(--spacing-md); padding: var(--spacing-sm) var(--spacing-md); background: var(--primary-color); color: white; border: none; border-radius: var(--radius-md); cursor: pointer;">
                <i class="fas fa-sync-alt"></i> Retry Loading
            </button>
        </div>
    `;
}
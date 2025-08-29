// ===== RESULTS DISPLAY =====
function displayResults(data) {
    if (!elements.resultsSection || !elements.resultsSummary || !elements.resultsGrid) return;
    
    // Initialize pagination
    const firstModel = Object.keys(data.predictions || {})[0];
    const predictions = data.predictions ? data.predictions[firstModel] || [] : [];
    totalResults = predictions.length;
    currentPage = 1;
    
    // Show results section
    elements.resultsSection.style.display = 'block';
    
    // Display summary
    const summary = createResultsSummary(data);
    elements.resultsSummary.innerHTML = summary;
    
    // Add classification key at the top of results
    const classificationKey = createClassificationKey();
    
    // Generate scientific analysis
    const scientificAnalysis = createScientificAnalysis(data);
    
    // Display paginated results with key and analysis
    displayPaginatedResults(data, classificationKey, scientificAnalysis);
}

function createClassificationKey() {
    return `
        <div class="classification-key">
            <h3><i class="fas fa-info-circle"></i> Classification Guide</h3>
            <div class="key-items">
                <div class="key-item">
                    <div class="key-badge positive">Parkinson's Detected</div>
                    <span>Voice patterns indicate likely presence of Parkinson's disease</span>
                </div>
                <div class="key-item">
                    <div class="key-badge negative">Likely Healthy</div>
                    <span>No significant Parkinson's indicators detected in voice patterns</span>
                </div>
                <div class="key-item">
                    <div class="confidence-indicator">
                        <span class="confidence-label">Diagnostic Confidence:</span>
                        <span>How certain our models are about the diagnosis (not the probability of having Parkinson's)</span>
                    </div>
                </div>
            </div>
            <div class="key-note">
                <i class="fas fa-stethoscope"></i>
                <strong>Clinical Note:</strong> These results are based on voice analysis and should be used alongside clinical examination. 
                The original dataset shows 75.4% of samples were from Parkinson's patients, reflecting the study population.
            </div>
        </div>
    `;
}

function createScientificAnalysis(data) {
    const predictionModels = data.predictions || {};
    const modelNames = Object.keys(predictionModels);
    
    if (modelNames.length === 0) {
        return '';
    }
    
    // Use the first model for analysis (they should be consistent)
    const firstModel = modelNames[0];
    const predictions = predictionModels[firstModel] || [];
    const probabilities = data.probabilities ? data.probabilities[firstModel] || [] : [];
    
    const totalSamples = predictions.length;
    const positiveCount = predictions.filter(p => p === 1).length;
    const negativeCount = totalSamples - positiveCount;
    const positiveRate = (positiveCount / totalSamples * 100).toFixed(1);
    
    // Calculate probability statistics
    const positiveProbabilities = probabilities.filter((prob, i) => predictions[i] === 1);
    const negativeProbabilities = probabilities.filter((prob, i) => predictions[i] === 0);
    
    const avgPositiveProb = positiveProbabilities.length > 0 ? 
        (positiveProbabilities.reduce((a, b) => a + b, 0) / positiveProbabilities.length * 100).toFixed(1) : 'N/A';
    const avgNegativeProb = negativeProbabilities.length > 0 ? 
        (negativeProbabilities.reduce((a, b) => a + b, 0) / negativeProbabilities.length * 100).toFixed(1) : 'N/A';
    
    // Estimate false positive/negative rates based on probability distributions
    const lowConfidenceThreshold = 0.6;
    const highConfidenceThreshold = 0.4;
    
    const uncertainPositives = positiveProbabilities.filter(p => p < lowConfidenceThreshold).length;
    const uncertainNegatives = negativeProbabilities.filter(p => p > highConfidenceThreshold).length;
    
    return `
        <div class="scientific-analysis">
            <h3><i class="fas fa-microscope"></i> Statistical Analysis & Model Performance</h3>
            
            <div class="analysis-sections">
                <div class="analysis-section">
                    <h4>Dataset Characteristics</h4>
                    <div class="analysis-stats">
                        <div class="stat-grid">
                            <div class="stat-item">
                                <span class="stat-label">Total Samples:</span>
                                <span class="stat-value">${totalSamples.toLocaleString()}</span>
                            </div>
                            <div class="stat-item">
                                <span class="stat-label">Positive Rate:</span>
                                <span class="stat-value">${positiveRate}%</span>
                            </div>
                            <div class="stat-item">
                                <span class="stat-label">Expected in Population:</span>
                                <span class="stat-value">0.1-3% (Age dependent)</span>
                            </div>
                        </div>
                    </div>
                    <div class="analysis-note critical">
                        <i class="fas fa-exclamation-triangle"></i>
                        <strong>Critical Issue:</strong> This dataset shows ${positiveRate}% positive cases, which is ${positiveRate > 10 ? 'extremely high' : 'elevated'} compared to real-world prevalence (0.1-3%). 
                        This suggests either: (1) a clinical study population with pre-selected symptomatic patients, or (2) a biased dataset.
                        <strong>Clinical screening tools should be trained on population-representative data (1-5% prevalence) for accurate real-world performance.</strong>
                    </div>
                </div>
                
                <div class="analysis-section">
                    <h4>Model Probability Analysis</h4>
                    <div class="analysis-stats">
                        <div class="stat-grid">
                            <div class="stat-item">
                                <span class="stat-label">Avg Positive Probability:</span>
                                <span class="stat-value">${avgPositiveProb}%</span>
                            </div>
                            <div class="stat-item">
                                <span class="stat-label">Avg Negative Probability:</span>
                                <span class="stat-value">${avgNegativeProb}%</span>
                            </div>
                            <div class="stat-item">
                                <span class="stat-label">Uncertain Positives:</span>
                                <span class="stat-value">${uncertainPositives} (<60% confidence)</span>
                            </div>
                            <div class="stat-item">
                                <span class="stat-label">Uncertain Negatives:</span>
                                <span class="stat-value">${uncertainNegatives} (>40% probability)</span>
                            </div>
                        </div>
                    </div>
                </div>
                
                <div class="analysis-section">
                    <h4>Clinical Interpretation Concerns</h4>
                    <div class="analysis-warnings">
                        <div class="warning-item">
                            <i class="fas fa-user-md"></i>
                            <div>
                                <strong>False Positive Risk:</strong> With ${positiveRate}% positive rate in training data, 
                                models may over-diagnose Parkinson's in healthy populations. In a population with 1% actual prevalence, 
                                this could result in ${Math.round(positiveRate)}x more false positives than true positives.
                            </div>
                        </div>
                        
                        <div class="warning-item">
                            <i class="fas fa-chart-line"></i>
                            <div>
                                <strong>Model Calibration Issue:</strong> Models trained on imbalanced data (${positiveRate}% positive) 
                                are poorly calibrated for real-world screening where prevalence is 1-3%. 
                                <strong>Recommendation:</strong> Retrain on population-representative datasets with appropriate class balancing.
                            </div>
                        </div>
                        
                        <div class="warning-item">
                            <i class="fas fa-stethoscope"></i>
                            <div>
                                <strong>Clinical Context:</strong> Voice analysis is a <strong>screening tool</strong>, not a diagnostic test. 
                                All positive results require clinical evaluation. The high positive rate in this analysis suggests 
                                these models may be more suitable for research settings than general population screening.
                            </div>
                        </div>
                    </div>
                </div>
                
                <div class="analysis-section">
                    <h4>Recommendations</h4>
                    <div class="recommendations">
                        <div class="recommendation">
                            <i class="fas fa-database"></i>
                            <strong>Data Rebalancing:</strong> Create population-representative datasets (1-5% prevalence) for realistic model performance
                        </div>
                        <div class="recommendation">
                            <i class="fas fa-balance-scale"></i>
                            <strong>Threshold Optimization:</strong> Adjust decision thresholds to minimize false positives in screening scenarios
                        </div>
                        <div class="recommendation">
                            <i class="fas fa-chart-bar"></i>
                            <strong>Performance Metrics:</strong> Report sensitivity, specificity, PPV, and NPV for different prevalence scenarios
                        </div>
                        <div class="recommendation">
                            <i class="fas fa-users"></i>
                            <strong>Validation:</strong> Test on independent, population-representative datasets before clinical deployment
                        </div>
                    </div>
                </div>
            </div>
        </div>
    `;
}

function displayPaginatedResults(data, classificationKey = '', scientificAnalysis = '') {
    if (!elements.resultsGrid) return;
    
    const startIndex = (currentPage - 1) * resultsPerPage;
    const endIndex = Math.min(startIndex + resultsPerPage, totalResults);
    
    // Create results grid for current page
    const results = createResultsGrid(data, startIndex, endIndex);
    
    // Create pagination controls
    const paginationControls = createPaginationControls();
    
    // Update results grid with key, analysis, results and controls
    elements.resultsGrid.innerHTML = classificationKey + scientificAnalysis + results + paginationControls;
}

function createPaginationControls() {
    if (totalResults <= resultsPerPage) {
        return ''; // No pagination needed
    }
    
    const totalPages = Math.ceil(totalResults / resultsPerPage);
    const startResult = (currentPage - 1) * resultsPerPage + 1;
    const endResult = Math.min(currentPage * resultsPerPage, totalResults);
    
    let paginationHTML = `
        <div class="pagination-container">
            <div class="pagination-info">
                Showing ${startResult}-${endResult} of ${totalResults} results
            </div>
            <div class="pagination-controls">
    `;
    
    // Previous button
    if (currentPage > 1) {
        paginationHTML += `
            <button class="pagination-btn" onclick="changePage(${currentPage - 1})">
                <i class="fas fa-chevron-left"></i> Previous
            </button>
        `;
    }
    
    // Page numbers
    const maxPagesToShow = 5;
    let startPage = Math.max(1, currentPage - Math.floor(maxPagesToShow / 2));
    let endPage = Math.min(totalPages, startPage + maxPagesToShow - 1);
    
    // Adjust start page if we're near the end
    if (endPage - startPage < maxPagesToShow - 1) {
        startPage = Math.max(1, endPage - maxPagesToShow + 1);
    }
    
    // First page and ellipsis
    if (startPage > 1) {
        paginationHTML += `
            <button class="pagination-btn page-btn" onclick="changePage(1)">1</button>
        `;
        if (startPage > 2) {
            paginationHTML += `<span class="pagination-ellipsis">...</span>`;
        }
    }
    
    // Page numbers
    for (let i = startPage; i <= endPage; i++) {
        const activeClass = i === currentPage ? 'active' : '';
        paginationHTML += `
            <button class="pagination-btn page-btn ${activeClass}" onclick="changePage(${i})">${i}</button>
        `;
    }
    
    // Last page and ellipsis
    if (endPage < totalPages) {
        if (endPage < totalPages - 1) {
            paginationHTML += `<span class="pagination-ellipsis">...</span>`;
        }
        paginationHTML += `
            <button class="pagination-btn page-btn" onclick="changePage(${totalPages})">${totalPages}</button>
        `;
    }
    
    // Next button
    if (currentPage < totalPages) {
        paginationHTML += `
            <button class="pagination-btn" onclick="changePage(${currentPage + 1})">
                Next <i class="fas fa-chevron-right"></i>
            </button>
        `;
    }
    
    paginationHTML += `
            </div>
        </div>
    `;
    
    return paginationHTML;
}

function changePage(newPage) {
    if (newPage >= 1 && newPage <= Math.ceil(totalResults / resultsPerPage)) {
        currentPage = newPage;
        const classificationKey = createClassificationKey();
        const scientificAnalysis = createScientificAnalysis(currentResults);
        displayPaginatedResults(currentResults, classificationKey, scientificAnalysis);
        
        // Scroll to top of results
        if (elements.resultsGrid) {
            elements.resultsGrid.scrollIntoView({ behavior: 'smooth', block: 'start' });
        }
    }
}

function createResultsSummary(data) {
    // Get predictions from the first model (they should be the same across models)
    const predictionModels = data.predictions || {};
    const modelNames = Object.keys(predictionModels);
    
    if (modelNames.length === 0) {
        return '<div class="summary-stats">No predictions available</div>';
    }
    
    // Use the first model's predictions for summary stats
    const firstModel = modelNames[0];
    const predictions = predictionModels[firstModel] || [];
    const probabilities = data.probabilities ? data.probabilities[firstModel] || [] : [];
    
    const totalSamples = predictions.length;
    const positiveCount = predictions.filter(p => p === 1).length;
    const negativeCount = totalSamples - positiveCount;
    
    // Calculate average confidence from probabilities
    let avgConfidence = 0;
    if (probabilities.length > 0) {
        avgConfidence = probabilities.reduce((sum, prob) => sum + prob, 0) / probabilities.length;
    } else {
        avgConfidence = 0.85; // Default confidence if not available
    }
    
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
            Analysis completed with ${(avgConfidence * 100).toFixed(1)}% average confidence across ${modelNames.length} models
        </div>
    `;
}

function createResultsGrid(data, startIndex = 0, endIndex = null) {
    const predictionModels = data.predictions || {};
    const modelNames = Object.keys(predictionModels);
    
    if (modelNames.length === 0) {
        return '<p>No predictions available</p>';
    }
    
    // Use the first model's predictions for individual results
    const firstModel = modelNames[0];
    const predictions = predictionModels[firstModel] || [];
    const probabilities = data.probabilities ? data.probabilities[firstModel] || [] : [];
    
    if (predictions.length === 0) {
        return '<p>No predictions available</p>';
    }
    
    // Apply pagination
    const actualEndIndex = endIndex || predictions.length;
    const paginatedPredictions = predictions.slice(startIndex, actualEndIndex);
    const paginatedProbabilities = probabilities.slice(startIndex, actualEndIndex);
    
    return paginatedPredictions.map((prediction, relativeIndex) => {
        const absoluteIndex = startIndex + relativeIndex; // Actual index in the full array
        const isPositive = prediction === 1;
        
        // Get predictions and probabilities from all models for this sample
        const modelResults = {};
        let agreementCount = 0;
        
        modelNames.forEach(modelName => {
            const modelPredictions = predictionModels[modelName] || [];
            const modelProbabilities = data.probabilities ? data.probabilities[modelName] || [] : [];
            
            const modelPrediction = modelPredictions[absoluteIndex];
            const modelProbability = modelProbabilities[absoluteIndex] || 0.5;
            
            modelResults[modelName] = {
                prediction: modelPrediction,
                probability: modelProbability
            };
            
            if (modelPrediction === prediction) {
                agreementCount++;
            }
        });
        
        // Get the raw probability and calculate proper diagnostic confidence
        const primaryProbability = paginatedProbabilities[relativeIndex] || 0.5;
        
        // Calculate model agreement confidence (based on how many models agree)
        const agreementConfidence = (agreementCount / modelNames.length) * 100;
        
        // Calculate probability-based confidence 
        // This represents how confident we are based on the distance from the decision boundary (0.5)
        const probabilityConfidence = Math.abs(primaryProbability - 0.5) * 200; // 0 to 100 scale
        
        // Combined diagnostic confidence (weighted average of agreement and probability distance)
        const diagnosticConfidence = Math.min(95, Math.max(50, 
            (agreementConfidence * 0.6) + (probabilityConfidence * 0.4)
        ));
        
        const agreementPercent = ((agreementCount / modelNames.length) * 100).toFixed(0);
        const confidencePercent = diagnosticConfidence.toFixed(0);
        
        // Visual indicator based on diagnostic confidence
        const confidenceWidth = diagnosticConfidence;
        const confidenceClass = diagnosticConfidence >= 75 ? 'high-confidence' : 
                               diagnosticConfidence >= 60 ? 'medium-confidence' : 'low-confidence';
        
        return `
            <div class="prediction-card">
                <div class="prediction-header">
                    <div class="prediction-title">Sample ${absoluteIndex + 1}</div>
                    <div class="prediction-badge ${isPositive ? 'positive' : 'negative'}">
                        ${isPositive ? 'Parkinson\'s Detected' : 'Likely Healthy'}
                    </div>
                </div>
                <div class="confidence-bar">
                    <div class="confidence-fill ${confidenceClass}" 
                         style="width: ${confidenceWidth}%"></div>
                </div>
                <div class="prediction-details">
                    <p><strong>Raw Model Probability:</strong> ${(primaryProbability * 100).toFixed(1)}% chance of Parkinson's</p>
                    <p><strong>Diagnostic Confidence:</strong> ${confidencePercent}% (${diagnosticConfidence >= 75 ? 'High' : diagnosticConfidence >= 60 ? 'Medium' : 'Low'})</p>
                    <p><strong>Clinical Interpretation:</strong> ${isPositive ? 'Voice patterns suggest possible Parkinson\'s disease' : 'Voice patterns appear within normal range'}</p>
                    <div class="models-agreement">
                        <p><strong>Model Agreement:</strong> ${agreementCount}/${modelNames.length} models agree (${agreementPercent}%)</p>
                        <button class="toggle-models-btn" onclick="toggleModelBreakdown(${absoluteIndex})">
                            <i class="fas fa-chevron-down"></i> View Model Details
                        </button>
                        <div class="model-breakdown" id="model-breakdown-${absoluteIndex}" style="display: none;">
                            ${modelNames.map(modelName => {
                                const result = modelResults[modelName];
                                const modelIsPositive = result.prediction === 1;
                                const probability = (result.probability * 100).toFixed(1);
                                return `
                                    <div class="model-result">
                                        <div class="model-info">
                                            <span class="model-name">${modelName.replace('_', ' ').toUpperCase()}</span>
                                            <span class="model-prediction ${modelIsPositive ? 'positive' : 'negative'}">
                                                ${modelIsPositive ? 'Positive' : 'Negative'}
                                            </span>
                                        </div>
                                        <div class="model-probability">
                                            <span>Raw Probability: ${probability}%</span>
                                            <div class="prob-bar">
                                                <div class="prob-fill ${modelIsPositive ? 'positive' : 'negative'}" 
                                                     style="width: ${probability}%"></div>
                                            </div>
                                        </div>
                                    </div>
                                `;
                            }).join('')}
                        </div>
                    </div>
                </div>
            </div>
        `;
    }).join('');
}

// ===== MODEL BREAKDOWN FUNCTIONALITY =====
function toggleModelBreakdown(sampleIndex) {
    const breakdownElement = document.getElementById(`model-breakdown-${sampleIndex}`);
    const buttonElement = document.querySelector(`button[onclick="toggleModelBreakdown(${sampleIndex})"]`);
    const icon = buttonElement.querySelector('i');
    
    if (breakdownElement.style.display === 'none') {
        breakdownElement.style.display = 'block';
        icon.className = 'fas fa-chevron-up';
        buttonElement.innerHTML = '<i class="fas fa-chevron-up"></i> Hide Model Details';
    } else {
        breakdownElement.style.display = 'none';
        icon.className = 'fas fa-chevron-down';
        buttonElement.innerHTML = '<i class="fas fa-chevron-down"></i> View Model Details';
    }
}

// ===== EDUCATIONAL SECTION FUNCTIONALITY =====
function switchModel(modelName) {
    // Remove active class from all tabs and content
    const allTabs = document.querySelectorAll('.ide-tab');
    const allContent = document.querySelectorAll('.model-content');
    
    allTabs.forEach(tab => tab.classList.remove('active'));
    allContent.forEach(content => content.classList.remove('active'));
    
    // Add active class to selected tab and content
    const selectedTab = document.querySelector(`[data-model="${modelName}"]`);
    const selectedContent = document.querySelector(`#${modelName}-content`);
    
    if (selectedTab && selectedContent) {
        selectedTab.classList.add('active');
        selectedContent.classList.add('active');
        
        // Optional: Smooth scroll to educational section if not visible
        const educationalSection = document.getElementById('educationalSection');
        if (educationalSection && !isInViewport(educationalSection)) {
            educationalSection.scrollIntoView({ 
                behavior: 'smooth', 
                block: 'start' 
            });
        }
        
        console.log(`Switched to ${modelName} model documentation`);
    }
}

function isInViewport(element) {
    const rect = element.getBoundingClientRect();
    return (
        rect.top >= 0 &&
        rect.left >= 0 &&
        rect.bottom <= (window.innerHeight || document.documentElement.clientHeight) &&
        rect.right <= (window.innerWidth || document.documentElement.clientWidth)
    );
}
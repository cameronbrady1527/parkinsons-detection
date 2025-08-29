// ===== DEMO DROPDOWN FUNCTIONALITY =====
function toggleDemoDropdown() {
    const dropdown = document.querySelector('.demo-dropdown');
    const isActive = dropdown.classList.contains('active');
    
    if (isActive) {
        dropdown.classList.remove('active');
        document.removeEventListener('click', closeDemoDropdownOutside);
    } else {
        dropdown.classList.add('active');
        setTimeout(() => {
            document.addEventListener('click', closeDemoDropdownOutside);
        }, 100);
    }
}

function closeDemoDropdownOutside(event) {
    const dropdown = document.querySelector('.demo-dropdown');
    if (dropdown && !dropdown.contains(event.target)) {
        dropdown.classList.remove('active');
        document.removeEventListener('click', closeDemoDropdownOutside);
    }
}

// ===== DEMO FUNCTIONALITY =====
async function runDemo(demoType = 'default') {
    try {
        // Update demo button state
        setDemoButtonState('loading');
        updateStatus('loading', 'Loading Demo...');
        
        // Show a brief loading state for better UX
        await new Promise(resolve => setTimeout(resolve, 500));
        
        // Determine which demo file to load
        let demoFileName, demoDisplayName, demoSampleCount;
        
        switch(demoType) {
            // Realistic Screening Scenarios
            case 'general_population':
                demoFileName = 'demo_general_population.csv';
                demoDisplayName = 'General Population Screening';
                demoSampleCount = 'population samples (0.5% prevalence)';
                break;
            case 'elderly_screening':
                demoFileName = 'demo_elderly_screening.csv';
                demoDisplayName = 'Elderly Screening (65+)';
                demoSampleCount = 'elderly patients (2% prevalence)';
                break;
            case 'high_risk_screening':
                demoFileName = 'demo_high_risk_screening.csv';
                demoDisplayName = 'High-Risk Screening';
                demoSampleCount = 'high-risk patients (5% prevalence)';
                break;
            case 'symptom_based_screening':
                demoFileName = 'demo_symptom_based_screening.csv';
                demoDisplayName = 'Symptom-Based Screening';
                demoSampleCount = 'referred patients (15% prevalence)';
                break;
            case 'small_balanced_sample':
                demoFileName = 'demo_small_balanced_sample.csv';
                demoDisplayName = 'Small Balanced Sample';
                demoSampleCount = 'balanced samples (3% prevalence)';
                break;
            // Original Biased Datasets (for comparison)
            case 'early_stage':
                demoFileName = 'demo_early_stage.csv';
                demoDisplayName = 'Early Stage Detection (BIASED)';
                demoSampleCount = 'early stage patients (~75% positive)';
                break;
            case 'advanced_stage':
                demoFileName = 'demo_advanced_stage.csv';
                demoDisplayName = 'Advanced Stage (BIASED)';
                demoSampleCount = 'advanced stage patients (~75% positive)';
                break;
            case 'mixed_cohort':
                demoFileName = 'demo_mixed_cohort.csv';
                demoDisplayName = 'Mixed Patient Cohort (BIASED)';
                demoSampleCount = 'mixed cohort patients (~75% positive)';
                break;
            case 'large_dataset':
                demoFileName = 'demo_large_dataset.csv';
                demoDisplayName = 'Large Clinical Dataset (BIASED)';
                demoSampleCount = 'clinical samples (75% positive)';
                break;
            default:
                // Default demo data (original 3 samples)
                const demoCSV = `name,MDVP:Fo(Hz),MDVP:Fhi(Hz),MDVP:Flo(Hz),MDVP:Jitter(%),MDVP:Jitter(Abs),MDVP:RAP,MDVP:PPQ,Jitter:DDP,MDVP:Shimmer,MDVP:Shimmer(dB),Shimmer:APQ3,Shimmer:APQ5,MDVP:APQ,Shimmer:DDA,NHR,HNR,status,RPDE,DFA,spread1,spread2,D2,PPE
phon_R01_S01_1,119.99200,157.30200,74.99700,0.00784,0.00007,0.00370,0.00554,0.01109,0.04374,0.42600,0.02182,0.03130,0.02971,0.06545,0.02211,21.03300,1,0.414783,0.815285,-4.813031,0.266482,2.301442,0.284654
phon_R01_S01_2,122.40000,148.65000,113.81900,0.00968,0.00008,0.00465,0.00696,0.01394,0.06134,0.62600,0.03134,0.04518,0.04368,0.09403,0.01929,19.08500,1,0.458359,0.819521,-4.075192,0.335590,2.486855,0.368674
phon_R01_S01_3,116.68200,131.11100,111.55500,0.01050,0.00009,0.00544,0.00781,0.01633,0.05233,0.48200,0.02757,0.03858,0.03590,0.08270,0.01309,20.65100,1,0.429895,0.825288,-4.443179,0.311173,2.342259,0.332634`;

                const blob = new Blob([demoCSV], { type: 'text/csv' });
                const demoFile = new File([blob], 'demo_data.csv', { type: 'text/csv' });
                currentFile = demoFile;
                
                // Update UI for default demo
                const displayInfo = getDemoDisplayInfo('default');
                elements.uploadArea.innerHTML = `
                    <div class="upload-content">
                        <div class="upload-icon">
                            ${displayInfo.icon}
                            <div class="upload-pulse"></div>
                        </div>
                        <h4>${displayInfo.title}</h4>
                        <p>demo_data.csv (3 samples with voice measurements)</p>
                        <div class="file-info">
                            <span><i class="fas fa-check" style="color: var(--success-color);"></i> Demo data ready for analysis</span>
                        </div>
                    </div>
                `;
                
                setUploadButtonState('ready');
                setDemoButtonState('success');
                updateStatus('healthy', 'Demo Ready');
                scrollToUpload();
                showNotification('Demo data loaded! Click "Analyze Data" to run the analysis.', 'success');
                
                setTimeout(() => {
                    setDemoButtonState('ready');
                }, 2000);
                
                return;
        }
        
        // Load external demo file
        try {
            const response = await fetch(`/static/demo_data/${demoFileName}`);
            if (!response.ok) {
                throw new Error(`Failed to load ${demoFileName}: ${response.statusText}`);
            }
            
            const csvText = await response.text();
            const lines = csvText.trim().split('\n');
            const sampleCount = lines.length - 1; // Subtract header
            
            // Create file object from the loaded CSV
            const blob = new Blob([csvText], { type: 'text/csv' });
            const demoFile = new File([blob], demoFileName, { type: 'text/csv' });
            currentFile = demoFile;
            
            // Update UI with correct demo info
            const displayInfo = getDemoDisplayInfo(demoType);
            elements.uploadArea.innerHTML = `
                <div class="upload-content">
                    <div class="upload-icon">
                        ${displayInfo.icon}
                        <div class="upload-pulse"></div>
                    </div>
                    <h4>${displayInfo.title}</h4>
                    <p>${demoFileName} (${sampleCount} ${demoSampleCount})</p>
                    <div class="file-info">
                        <span><i class="fas fa-check" style="color: var(--success-color);"></i> Demo data ready for analysis</span>
                    </div>
                </div>
            `;
            
            setUploadButtonState('ready');
            setDemoButtonState('success');
            updateStatus('healthy', 'Demo Ready');
            scrollToUpload();
            showNotification(`${demoDisplayName} loaded! Click "Analyze Data" to run the analysis.`, 'success');
            
        } catch (fetchError) {
            console.error('Failed to load demo file:', fetchError);
            throw new Error(`Could not load ${demoDisplayName}: ${fetchError.message}`);
        }
        
        // Reset demo button after 2 seconds
        setTimeout(() => {
            setDemoButtonState('ready');
        }, 2000);
        
    } catch (error) {
        console.error('❌ Demo loading failed:', error);
        setDemoButtonState('error');
        updateStatus('error', 'Demo Failed');
        showNotification('Failed to load demo data', 'error');
        
        // Reset demo button after 2 seconds
        setTimeout(() => {
            setDemoButtonState('ready');
            updateStatus('healthy', 'Ready');
        }, 2000);
    }
}

function getDemoDisplayInfo(demoType) {
    const demoInfo = {
        // Realistic Screening Scenarios
        'general_population': {
            title: 'General Population Screening Loaded',
            icon: '<i class="fas fa-users" style="color: var(--success-color);"></i>'
        },
        'elderly_screening': {
            title: 'Elderly Screening Dataset Loaded',
            icon: '<i class="fas fa-user-clock" style="color: var(--primary-color);"></i>'
        },
        'high_risk_screening': {
            title: 'High-Risk Screening Dataset Loaded',
            icon: '<i class="fas fa-dna" style="color: var(--warning-color);"></i>'
        },
        'symptom_based_screening': {
            title: 'Symptom-Based Screening Loaded',
            icon: '<i class="fas fa-stethoscope" style="color: var(--accent-color);"></i>'
        },
        'small_balanced_sample': {
            title: 'Small Balanced Sample Loaded',
            icon: '<i class="fas fa-vial" style="color: var(--primary-color);"></i>'
        },
        // Original Biased Datasets
        'early_stage': {
            title: 'Early Stage Demo (BIASED) Loaded',
            icon: '<i class="fas fa-search-plus" style="color: var(--danger-color);"></i>'
        },
        'advanced_stage': {
            title: 'Advanced Stage Demo (BIASED) Loaded',
            icon: '<i class="fas fa-exclamation-triangle" style="color: var(--danger-color);"></i>'
        },
        'mixed_cohort': {
            title: 'Mixed Cohort Demo (BIASED) Loaded',
            icon: '<i class="fas fa-users" style="color: var(--danger-color);"></i>'
        },
        'large_dataset': {
            title: 'Large Clinical Dataset (BIASED) Loaded',
            icon: '<i class="fas fa-database" style="color: var(--danger-color);"></i>'
        },
        'default': {
            title: 'Original Demo Loaded',
            icon: '<i class="fas fa-flask" style="color: var(--accent-color);"></i>'
        }
    };
    
    return demoInfo[demoType] || demoInfo['default'];
}
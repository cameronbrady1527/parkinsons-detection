// ===== STATUS UPDATES =====
function updateStatus(type, message) {
    if (elements.statusDot && elements.statusText) {
        elements.statusDot.className = `status-dot ${type}`;
        elements.statusText.textContent = message;
    }
}

function setUploadButtonState(state) {
    if (!elements.uploadBtn) return;
    
    const btnIcon = elements.uploadBtn.querySelector('i');
    const btnText = elements.uploadBtn.querySelector('span');
    const btnLoading = elements.uploadBtn.querySelector('.btn-loading');
    
    // Reset button classes
    elements.uploadBtn.className = 'upload-btn primary';
    
    switch (state) {
        case 'loading':
            elements.uploadBtn.disabled = true;
            elements.uploadBtn.classList.add('loading');
            if (btnIcon) btnIcon.className = 'fas fa-spinner fa-spin';
            if (btnText) btnText.textContent = 'Analyzing...';
            if (btnLoading) btnLoading.style.display = 'flex';
            break;
            
        case 'success':
            elements.uploadBtn.disabled = false;
            elements.uploadBtn.classList.add('success');
            if (btnIcon) btnIcon.className = 'fas fa-check';
            if (btnText) btnText.textContent = 'Analysis Complete';
            if (btnLoading) btnLoading.style.display = 'none';
            break;
            
        case 'error':
            elements.uploadBtn.disabled = false;
            elements.uploadBtn.classList.add('error');
            if (btnIcon) btnIcon.className = 'fas fa-exclamation-triangle';
            if (btnText) btnText.textContent = 'Analysis Failed';
            if (btnLoading) btnLoading.style.display = 'none';
            break;
            
        default: // ready
            elements.uploadBtn.disabled = !currentFile;
            if (btnIcon) btnIcon.className = 'fas fa-play';
            if (btnText) btnText.textContent = 'Analyze Data';
            if (btnLoading) btnLoading.style.display = 'none';
            break;
    }
}

function setDemoButtonState(state) {
    if (!elements.demoBtn) return;
    
    const btnIcon = elements.demoBtn.querySelector('i');
    const btnText = elements.demoBtn.textContent.includes('Try Demo') ? 'Try Demo' : elements.demoBtn.textContent;
    
    // Reset button classes
    elements.demoBtn.className = 'demo-btn';
    
    switch (state) {
        case 'loading':
            elements.demoBtn.disabled = true;
            elements.demoBtn.classList.add('loading');
            if (btnIcon) btnIcon.className = 'fas fa-spinner fa-spin';
            elements.demoBtn.innerHTML = '<i class="fas fa-spinner fa-spin"></i> Loading Demo';
            break;
            
        case 'success':
            elements.demoBtn.disabled = false;
            elements.demoBtn.classList.add('success');
            if (btnIcon) btnIcon.className = 'fas fa-check';
            elements.demoBtn.innerHTML = '<i class="fas fa-check"></i> Demo Loaded';
            break;
            
        case 'error':
            elements.demoBtn.disabled = false;
            elements.demoBtn.classList.add('error');
            if (btnIcon) btnIcon.className = 'fas fa-exclamation-triangle';
            elements.demoBtn.innerHTML = '<i class="fas fa-exclamation-triangle"></i> Demo Failed';
            break;
            
        default: // ready
            elements.demoBtn.disabled = false;
            elements.demoBtn.innerHTML = '<i class="fas fa-play"></i> Try Demo';
            break;
    }
}
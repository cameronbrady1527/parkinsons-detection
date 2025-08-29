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
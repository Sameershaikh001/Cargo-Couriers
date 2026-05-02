// Enhanced tracking functionality
class ParcelTracker {
    constructor() {
        this.init();
    }
    
    init() {
        this.setupTrackingForm();
        this.setupRealTimeUpdates();
    }
    
    setupTrackingForm() {
        const form = document.getElementById('trackingForm');
        if (form) {
            form.addEventListener('submit', (e) => this.handleTrackingSubmit(e));
        }
        
        // Auto-focus tracking input if present
        const trackingInput = document.querySelector('input[name="tracking_number"]');
        if (trackingInput && !trackingInput.value) {
            trackingInput.focus();
        }
    }
    
    setupRealTimeUpdates() {
        // Simulate real-time updates for demo purposes
        const statusElements = document.querySelectorAll('.tracking-status');
        
        statusElements.forEach(element => {
            const status = element.dataset.status;
            this.animateStatus(element, status);
        });
    }
    
    animateStatus(element, status) {
        if (status === 'in-transit') {
            element.style.animation = 'pulse 2s infinite';
        }
    }
    
    handleTrackingSubmit(e) {
        const form = e.target;
        const trackingNumber = form.querySelector('input[name="tracking_number"]').value.trim();
        
        if (!this.validateTrackingNumber(trackingNumber)) {
            e.preventDefault();
            this.showError('Please enter a valid tracking number (e.g., AWT12345678)');
            return;
        }
        
        // Show loading state
        const submitButton = form.querySelector('button[type="submit"]');
        const originalText = submitButton.innerHTML;
        submitButton.innerHTML = '<i class="fas fa-spinner fa-spin me-1"></i> Tracking...';
        submitButton.disabled = true;
        
        // Re-enable button after 2 seconds (in case of slow response)
        setTimeout(() => {
            submitButton.innerHTML = originalText;
            submitButton.disabled = false;
        }, 2000);
    }
    
    validateTrackingNumber(trackingNumber) {
        // Basic validation - tracking number should start with AWT and have alphanumeric characters
        const trackingRegex = /^AWT[A-Z0-9]{8,12}$/i;
        return trackingRegex.test(trackingNumber);
    }
    
    showError(message) {
        // Remove existing error alerts
        const existingAlerts = document.querySelectorAll('.alert-danger');
        existingAlerts.forEach(alert => alert.remove());
        
        // Create new error alert
        const alertDiv = document.createElement('div');
        alertDiv.className = 'alert alert-danger alert-dismissible fade show mt-3';
        alertDiv.innerHTML = `
            ${message}
            <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
        `;
        
        // Insert after the form
        const form = document.getElementById('trackingForm');
        form.parentNode.insertBefore(alertDiv, form.nextSibling);
        
        // Auto-remove after 5 seconds
        setTimeout(() => {
            if (alertDiv.parentNode) {
                alertDiv.remove();
            }
        }, 5000);
    }
    
    // Method to simulate parcel status updates
    simulateStatusUpdate(trackingNumber) {
        const statuses = ['Booked', 'Picked Up', 'In Transit', 'Out for Delivery', 'Delivered'];
        let currentStatus = 0;
        
        const interval = setInterval(() => {
            if (currentStatus < statuses.length) {
                this.updateStatusDisplay(trackingNumber, statuses[currentStatus]);
                currentStatus++;
            } else {
                clearInterval(interval);
            }
        }, 3000);
    }
    
    updateStatusDisplay(trackingNumber, status) {
        // This would typically make an API call to update the status
        console.log(`Updating ${trackingNumber} to: ${status}`);
        
        // Update the UI if the tracking number matches
        const statusElement = document.querySelector(`[data-tracking="${trackingNumber}"] .status`);
        if (statusElement) {
            statusElement.textContent = status;
            statusElement.className = `status status-${status.toLowerCase().replace(' ', '-')}`;
        }
    }
}

// Initialize when DOM is loaded
document.addEventListener('DOMContentLoaded', () => {
    new ParcelTracker();
});

// Add CSS animations for tracking
const style = document.createElement('style');
style.textContent = `
    @keyframes pulse {
        0% { opacity: 1; }
        50% { opacity: 0.7; }
        100% { opacity: 1; }
    }
    
    .status-in-transit {
        animation: pulse 2s infinite;
    }
    
    .tracking-progress {
        position: relative;
        height: 4px;
        background: #e9ecef;
        border-radius: 2px;
        overflow: hidden;
    }
    
    .tracking-progress-bar {
        position: absolute;
        height: 100%;
        background: var(--primary-color);
        transition: width 0.3s ease;
    }
`;
document.head.appendChild(style);
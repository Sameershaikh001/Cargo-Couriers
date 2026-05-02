// Admin Panel JavaScript
document.addEventListener('DOMContentLoaded', function() {
    initializeAdminPanel();
});

function initializeAdminPanel() {
    // Update badge counts (you would typically fetch these via AJAX)
    updateDashboardCounts();
    
    // Initialize tooltips
    initializeTooltips();
    
    // Setup search functionality
    setupSearch();
    
    // Setup real-time updates
    setupRealTimeUpdates();
}

function updateDashboardCounts() {
    // This would typically make an API call to get real counts
    // For now, we'll update with static data or leave as is
    console.log('Dashboard counts would be updated here');
}

function initializeTooltips() {
    const tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
    const tooltipList = tooltipTriggerList.map(function (tooltipTriggerEl) {
        return new bootstrap.Tooltip(tooltipTriggerEl);
    });
}

function setupSearch() {
    // Generic search functionality for tables
    const searchInputs = document.querySelectorAll('input[placeholder*="Search"]');
    
    searchInputs.forEach(input => {
        input.addEventListener('input', function() {
            const filter = this.value.toLowerCase();
            const tableId = this.closest('.card').querySelector('table').id;
            const rows = document.querySelectorAll(`#${tableId} tbody tr`);
            
            rows.forEach(row => {
                const text = row.textContent.toLowerCase();
                row.style.display = text.includes(filter) ? '' : 'none';
            });
        });
    });
}

function setupRealTimeUpdates() {
    // Simulate real-time updates for demo
    setInterval(() => {
        updateNotificationBadges();
    }, 30000); // Update every 30 seconds
}

function updateNotificationBadges() {
    // This would typically make an API call to get updated counts
    // For demo purposes, we'll simulate some changes
    const parcelCount = document.getElementById('parcel-count');
    const partnerCount = document.getElementById('partner-count');
    
    if (parcelCount) {
        // Simulate random updates
        const current = parseInt(parcelCount.textContent) || 0;
        const change = Math.random() > 0.7 ? 1 : 0;
        parcelCount.textContent = current + change;
    }
}

// Export functions for global use
window.adminFunctions = {
    exportData: function(table) {
        alert(`Exporting ${table} data...`);
        // Implementation for data export
    },
    
    bulkAction: function(action, items) {
        if (confirm(`Are you sure you want to ${action} ${items.length} items?`)) {
            console.log(`Performing ${action} on:`, items);
            // Implementation for bulk actions
        }
    },
    
    quickStatusUpdate: function(trackingNumber, status) {
        fetch('/admin/update_parcel_status', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/x-www-form-urlencoded',
            },
            body: `tracking_number=${trackingNumber}&status=${status}`
        })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                location.reload();
            } else {
                alert('Error updating status');
            }
        });
    }
};

// Keyboard shortcuts for admin panel
document.addEventListener('keydown', function(e) {
    // Ctrl + D for dashboard
    if (e.ctrlKey && e.key === 'd') {
        e.preventDefault();
        window.location.href = '/admin/dashboard';
    }
    
    // Ctrl + P for parcels
    if (e.ctrlKey && e.key === 'p') {
        e.preventDefault();
        window.location.href = '/admin/parcels';
    }
    
    // Ctrl + L for logout
    if (e.ctrlKey && e.key === 'l') {
        e.preventDefault();
        window.location.href = '/admin/logout';
    }
});

// Auto-save functionality for forms
function setupAutoSave(formId, saveUrl) {
    const form = document.getElementById(formId);
    let timeout;
    
    form.addEventListener('input', function() {
        clearTimeout(timeout);
        timeout = setTimeout(() => {
            saveFormData(form, saveUrl);
        }, 1000);
    });
}

function saveFormData(form, saveUrl) {
    const formData = new FormData(form);
    
    fetch(saveUrl, {
        method: 'POST',
        body: formData
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            showAutoSaveIndicator();
        }
    });
}

function showAutoSaveIndicator() {
    const indicator = document.createElement('div');
    indicator.className = 'alert alert-success alert-dismissible fade show position-fixed';
    indicator.style.top = '20px';
    indicator.style.right = '20px';
    indicator.style.zIndex = '9999';
    indicator.innerHTML = `
        <i class="fas fa-check me-1"></i>Changes saved successfully
        <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
    `;
    
    document.body.appendChild(indicator);
    
    setTimeout(() => {
        indicator.remove();
    }, 3000);
}
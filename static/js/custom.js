// Custom JavaScript for Attendance Management System

document.addEventListener('DOMContentLoaded', function() {
    // Auto-hide alerts after 5 seconds
    const alerts = document.querySelectorAll('.alert');
    alerts.forEach(alert => {
        setTimeout(() => {
            if (alert) {
                alert.style.transition = 'opacity 0.5s ease';
                alert.style.opacity = '0';
                setTimeout(() => {
                    if (alert.parentNode) {
                        alert.parentNode.removeChild(alert);
                    }
                }, 500);
            }
        }, 5000);
    });

    // Remove all form validation that might interfere with submission
    // Let Django handle form validation on the server side

    // Attendance form auto-save (optional feature)
    const attendanceForm = document.querySelector('form[action*="attendance"]');
    if (attendanceForm) {
        const inputs = attendanceForm.querySelectorAll('select');
        inputs.forEach(input => {
            input.addEventListener('change', function() {
                // Add visual feedback
                this.style.borderColor = '#28a745';
                setTimeout(() => {
                    this.style.borderColor = '';
                }, 1000);
            });
        });
    }

    // Chart responsiveness
    window.addEventListener('resize', function() {
        if (window.Chart) {
            Chart.helpers.each(Chart.instances, function(chart) {
                chart.resize();
            });
        }
    });

    // Table row highlighting
    const tableRows = document.querySelectorAll('tbody tr');
    tableRows.forEach(row => {
        row.addEventListener('mouseenter', function() {
            this.style.backgroundColor = '#f8f9fa';
        });
        row.addEventListener('mouseleave', function() {
            this.style.backgroundColor = '';
        });
    });

    // Remove all button loading states that interfere with form submission
    // Forms should submit normally without JavaScript interference
});

// Utility functions
function showAlert(message, type = 'info') {
    const alertDiv = document.createElement('div');
    alertDiv.className = `alert alert-${type} alert-dismissible fade show`;
    alertDiv.innerHTML = `
        ${message}
        <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
    `;
    
    const container = document.querySelector('.container');
    if (container) {
        container.insertBefore(alertDiv, container.firstChild);
        
        // Auto-hide after 5 seconds
        setTimeout(() => {
            if (alertDiv.parentNode) {
                alertDiv.remove();
            }
        }, 5000);
    }
}

// Date picker enhancements
function initializeDatePicker() {
    const dateInputs = document.querySelectorAll('input[type="date"]');
    dateInputs.forEach(input => {
        // Set max date to today
        input.max = new Date().toISOString().split('T')[0];
        
        // Add change event
        input.addEventListener('change', function() {
            if (this.value) {
                this.style.borderColor = '#28a745';
            }
        });
    });
}

// Initialize on page load
document.addEventListener('DOMContentLoaded', initializeDatePicker);

// Export functionality enhancement
function enhanceExport() {
    const exportButtons = document.querySelectorAll('a[href*="export"]');
    exportButtons.forEach(button => {
        button.addEventListener('click', function() {
            this.innerHTML = '<i class="bi bi-download"></i> Preparing Download...';
            this.style.pointerEvents = 'none';
        });
    });
}

document.addEventListener('DOMContentLoaded', enhanceExport);

// MyCRM JavaScript functions

// Initialize tooltips and popovers
document.addEventListener('DOMContentLoaded', function() {
    // Initialize Bootstrap tooltips
    var tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
    var tooltipList = tooltipTriggerList.map(function (tooltipTriggerEl) {
        return new bootstrap.Tooltip(tooltipTriggerEl);
    });

    // Initialize Bootstrap popovers
    var popoverTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="popover"]'));
    var popoverList = popoverTriggerList.map(function (popoverTriggerEl) {
        return new bootstrap.Popover(popoverTriggerEl);
    });
});

// Utility functions
const MyCRM = {
    // Show loading spinner
    showLoading: function(buttonElement) {
        if (buttonElement) {
            buttonElement.disabled = true;
            const originalText = buttonElement.innerHTML;
            buttonElement.setAttribute('data-original-text', originalText);
            buttonElement.innerHTML = '<span class="loading-spinner"></span> Loading...';
        }
    },

    // Hide loading spinner
    hideLoading: function(buttonElement) {
        if (buttonElement) {
            buttonElement.disabled = false;
            const originalText = buttonElement.getAttribute('data-original-text');
            if (originalText) {
                buttonElement.innerHTML = originalText;
            }
        }
    },

    // Show toast notification
    showToast: function(message, type = 'info') {
        const toastContainer = document.getElementById('toast-container') || this.createToastContainer();
        const toastId = 'toast-' + Date.now();
        
        const toastHtml = `
            <div id="${toastId}" class="toast align-items-center text-white bg-${type} border-0" role="alert" aria-live="assertive" aria-atomic="true">
                <div class="d-flex">
                    <div class="toast-body">
                        ${message}
                    </div>
                    <button type="button" class="btn-close btn-close-white me-2 m-auto" data-bs-dismiss="toast" aria-label="Close"></button>
                </div>
            </div>
        `;
        
        toastContainer.insertAdjacentHTML('beforeend', toastHtml);
        const toastElement = document.getElementById(toastId);
        const toast = new bootstrap.Toast(toastElement);
        toast.show();
        
        // Remove toast element after it's hidden
        toastElement.addEventListener('hidden.bs.toast', function() {
            this.remove();
        });
    },

    // Create toast container if it doesn't exist
    createToastContainer: function() {
        const container = document.createElement('div');
        container.id = 'toast-container';
        container.className = 'toast-container position-fixed top-0 end-0 p-3';
        container.style.zIndex = '1055';
        document.body.appendChild(container);
        return container;
    },

    // Confirm dialog
    confirm: function(message, callback) {
        if (confirm(message)) {
            callback();
        }
    },

    // Format date
    formatDate: function(dateString) {
        if (!dateString) return '';
        const date = new Date(dateString);
        return date.toLocaleDateString() + ' ' + date.toLocaleTimeString();
    },

    // Format relative time
    formatRelativeTime: function(dateString) {
        if (!dateString) return '';
        const date = new Date(dateString);
        const now = new Date();
        const diffInSeconds = Math.floor((now - date) / 1000);
        
        if (diffInSeconds < 60) return 'Just now';
        if (diffInSeconds < 3600) return Math.floor(diffInSeconds / 60) + ' minutes ago';
        if (diffInSeconds < 86400) return Math.floor(diffInSeconds / 3600) + ' hours ago';
        return Math.floor(diffInSeconds / 86400) + ' days ago';
    },

    // API helper functions
    api: {
        baseUrl: '/api',
        
        get: async function(endpoint) {
            return this.request('GET', endpoint);
        },
        
        post: async function(endpoint, data) {
            return this.request('POST', endpoint, data);
        },
        
        put: async function(endpoint, data) {
            return this.request('PUT', endpoint, data);
        },
        
        delete: async function(endpoint) {
            return this.request('DELETE', endpoint);
        },
        
        request: async function(method, endpoint, data = null) {
            const url = this.baseUrl + endpoint;
            const options = {
                method: method,
                headers: {
                    'Content-Type': 'application/json'
                }
            };
            
            // Add auth token if available
            const token = localStorage.getItem('authToken');
            if (token) {
                options.headers['Authorization'] = 'Bearer ' + token;
            }
            
            if (data) {
                options.body = JSON.stringify(data);
            }
            
            try {
                const response = await fetch(url, options);
                
                if (response.status === 401) {
                    // Redirect to login if unauthorized
                    localStorage.removeItem('authToken');
                    window.location.href = '/login';
                    return;
                }
                
                if (!response.ok) {
                    throw new Error(`HTTP error! status: ${response.status}`);
                }
                
                return await response.json();
            } catch (error) {
                console.error('API request failed:', error);
                MyCRM.showToast('An error occurred. Please try again.', 'danger');
                throw error;
            }
        }
    }
};

// Global error handler
window.addEventListener('unhandledrejection', function(event) {
    console.error('Unhandled promise rejection:', event.reason);
    MyCRM.showToast('An unexpected error occurred.', 'danger');
});

// Export to global scope
window.MyCRM = MyCRM;

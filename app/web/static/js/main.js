// Main JavaScript file for GovBid Pro

// Check authentication status on protected pages
function checkAuth() {
    const token = localStorage.getItem('token');
    const protectedPaths = ['/dashboard', '/opportunities', '/proposals'];
    
    const currentPath = window.location.pathname;
    
    if (protectedPaths.includes(currentPath) && !token) {
        window.location.href = '/login';
        return false;
    }
    
    return true;
}

// Logout function
function logout() {
    localStorage.removeItem('token');
    window.location.href = '/login';
}

// Format date for display
function formatDate(dateString) {
    if (!dateString) return '-';
    return new Date(dateString).toLocaleDateString();
}

// Initialize tooltips and popovers
document.addEventListener('DOMContentLoaded', function() {
    // Check authentication
    checkAuth();
    
    // Add logout button event listener if it exists
    const logoutBtn = document.getElementById('logout-btn');
    if (logoutBtn) {
        logoutBtn.addEventListener('click', logout);
    }
    
    // Initialize Bootstrap tooltips
    const tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
    tooltipTriggerList.map(function (tooltipTriggerEl) {
        return new bootstrap.Tooltip(tooltipTriggerEl);
    });
    
    // Initialize Bootstrap popovers
    const popoverTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="popover"]'));
    popoverTriggerList.map(function (popoverTriggerEl) {
        return new bootstrap.Popover(popoverTriggerEl);
    });
});

// Custom JupyterLab JavaScript Enhancements

// Wait for JupyterLab to be ready
window.addEventListener('load', function() {
    console.log('Custom JupyterLab script loaded');

    // Change title dynamically
    document.title = 'My Custom JupyterLab';

    // Modify toolbar button styles
    let toolbarButtons = document.querySelectorAll('.jp-ToolbarButton');
    toolbarButtons.forEach(button => {
        button.style.backgroundColor = '#444';
        button.style.borderRadius = '5px';
    });

    // Display an alert when JupyterLab starts
    setTimeout(() => {
        alert('Welcome to your customized JupyterLab environment!');
    }, 1000);
});

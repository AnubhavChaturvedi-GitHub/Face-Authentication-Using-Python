document.addEventListener('DOMContentLoaded', function () {
    const startButton = document.getElementById('start-auth');
    const stopButton = document.getElementById('stop-auth');
    const statusMessage = document.getElementById('status-message');
    const statusProgress = document.getElementById('status-progress');
    const terminalLog = document.getElementById('terminal-log');

    startButton.addEventListener('click', function () {
        fetch('/start_auth', {
            method: 'POST'
        })
        .then(response => response.json())
        .then(data => {
            statusMessage.textContent = data.status;
            // Update other UI elements as needed
        });
    });

    stopButton.addEventListener('click', function () {
        fetch('/stop_auth', {
            method: 'POST'
        })
        .then(response => response.json())
        .then(data => {
            statusMessage.textContent = data.status;
            // Update other UI elements as needed
        });
    });

    function updateStatus() {
        fetch('/status')
        .then(response => response.json())
        .then(data => {
            statusMessage.textContent = data.status;
            statusProgress.textContent = 'Progress: ' + data.progress;
            
            // Assuming the response contains authentication status
            if (data.status === 'Face recognized') {
                terminalLog.innerHTML = '<span class="glow">Welcome Sir</span>';
            } else {
                terminalLog.innerHTML = '<span class="glow">Face not recognized</span>';
            }
        });
    }

    setInterval(updateStatus, 5000); // Update status every 5 seconds
});

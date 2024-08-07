document.addEventListener('DOMContentLoaded', function() {
    const pitchDeckForm = document.getElementById('pitchDeckForm');
    const signinForm = document.getElementById('signinForm');
    const progressBar = document.getElementById('progressBar');
    const analysisSection = document.getElementById('analysisSection');

    if (pitchDeckForm) {
        pitchDeckForm.addEventListener('submit', function(e) {
            e.preventDefault();
            // Handle pitch deck form submission
            // Connect to backend and handle file upload
            alert('Pitch deck uploaded!');
        });
    }

    if (signinForm) {
        signinForm.addEventListener('submit', function(e) {
            e.preventDefault();
            // Handle sign-in form submission
            // Connect to backend for authentication
            alert('Sign-in successful!');
        });
    }

    if (progressBar && analysisSection) {
        // Simulate progress and analysis
        let progress = 0;
        const interval = setInterval(() => {
            if (progress < 100) {
                progress += 10;
                progressBar.style.width = `${progress}%`;
                progressBar.textContent = `${progress}% Complete`;

                // Simulate adding analysis content
                const analysisContent = document.createElement('p');
                analysisContent.textContent = `Analysis for page ${progress / 10}`;
                analysisSection.appendChild(analysisContent);
            } else {
                clearInterval(interval);
            }
        }, 500);
    }
});

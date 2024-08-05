document.addEventListener('DOMContentLoaded', () => {
    const form = document.getElementById('pitchDeckForm');
    const submitBtn = document.getElementById('submitBtn');
    const outputSection = document.querySelector('.output');

    // Add event listener to the submit button
    submitBtn.addEventListener('click', async (event) => {
        event.preventDefault(); // Prevent the default form submission

        const email = document.getElementById('email').value;
        const pitchDeck = document.getElementById('pitchDeck').files[0];

        if (!email || !pitchDeck) {
            alert('Please provide both email and pitch deck.');
            return;
        }

        // Change button text to "Processing..." and show a loader
        submitBtn.textContent = 'Processing...';
        outputSection.innerHTML = "<div class='loader'></div>"; // Show loader

        const formData = new FormData();
        formData.append('email', email);
        formData.append('pitchDeck', pitchDeck);

        try {
            const response = await fetch('/upload', {
                method: 'POST',
                body: formData
            });

            if (!response.ok) {
                throw new Error('File processing failed');
            }

            const data = await response.text();
            outputSection.innerHTML = data; // Insert response into the output section
        } catch (error) {
            console.error('Error:', error);
            outputSection.innerHTML = 'An error occurred while processing your request.';
        } finally {
            // Reset button text back to "Submit"
            submitBtn.textContent = 'Submit';
        }
    });
});

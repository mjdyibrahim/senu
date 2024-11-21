<template>
    <div>
        <Header />
        <main class="main-content">
            <section class="hero">
                <!-- Hero section content goes here -->
                <PitchDeckUploadForm />
                <ChatForm />
            </section>
            <section class="output">
                <!-- Output section content goes here -->
            </section>
            <section class="feedback">
                <h2>Your Startup Score & Feedback</h2>
                <div class="score-details">
                    <!-- Dynamic content for score and feedback will be inserted here -->
                </div>
            </section>
        </main>
        <Footer />
    </div>
</template>

<script>
import Header from "~/components/Header/Header.vue";
import Footer from "~/components/Footer/Footer.vue";
import PitchDeckUploadForm from "~/components/PitchDeckUploadForm.vue";
import ChatForm from "~/components/ChatForm.vue";

export default {
    components: {
        Header,
        Footer,
        PitchDeckUploadForm,
        ChatForm,
    },
};

document.addEventListener("DOMContentLoaded", () => {
  const form = document.getElementById("pitchDeckForm");
  const submitBtn = document.getElementById("submitBtn");
  const outputSection = document.querySelector(".output");

  // Add event listener to the form submission
  form.addEventListener("submit", async (event) => {
    event.preventDefault(); // Prevent the default form submission to handle it via JavaScript

    const email = document.getElementById("email").value;
    const pitchDeck = document.getElementById("pitchDeck").files[0];

    if (!email || !pitchDeck) {
      alert("Please provide both email and pitch deck.");
      return;
    }

    // Change button text to "Processing..." and show a loader
    submitBtn.textContent = "Processing...";
    outputSection.innerHTML = "<div class='loader'></div>"; // Show loader

    const formData = new FormData();
    formData.append("email", email);
    formData.append("file", pitchDeck);

    try {
      const response = await fetch(form.action, {
        method: "POST",
        body: formData,
      });

      if (!response.ok) {
        throw new Error("File processing failed");
      }

      const data = await response.text();
      outputSection.innerHTML = data; // Insert response into the output section
    } catch (error) {
      console.error("Error:", error);
      outputSection.innerHTML =
        "An error occurred while processing your request.";
    } finally {
      // Reset button text back to "Submit"
      submitBtn.textContent = "Analyze my Pitch Deck";
    }
  });
});

</script>

<style scoped>
/* Import main style */
@import "@/assets/css/main.css";
</style>

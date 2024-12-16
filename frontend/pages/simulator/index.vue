<template>
    <div>
        <main class="main-content">
            <section class="hero">
                <h1>Virtual Pitch Simulator</h1>
                <p>Experience the thrill of pitching your startup and receive valuable feedback.</p>
                <PitchDeckUploadForm @submit="handleFormSubmit" />
            </section>
            <section class="output" ref="outputSection" v-if="uploadResult">
                <h2>Results</h2>
                <pre>{{ uploadResult }}</pre>
            </section>
            <section class="feedback" v-if="uploadResult">
                <h2>Your Startup Score & Feedback</h2>
                <div class="score-details">
                    <!-- Display feedback based on uploadResult -->
                </div>
            </section>
        </main>
    </div>
</template>

<script setup>
import { ref } from "vue";
import TheHeader from "~/components/TheHeader.vue";
import TheFooter from "~/components/TheFooter.vue";
import PitchDeckUploadForm from "~/components/PitchDeckUploadForm.vue";

const uploadResult = ref(null);
const outputSection = ref(null);

const handleFormSubmit = (result) => {
    uploadResult.value = result;
    // Additional handling of the upload result
};
</script>

<style scoped>
@import "@/assets/css/main.css";

.main-content {
    padding: 2rem;
    max-width: 1200px;
    margin: 0 auto;
}

.hero {
    margin-bottom: 2rem;
}

/* New styles for side-by-side layout */
.hero-container {
    display: grid;
    grid-template-columns: 1fr 1fr; /* Two equal columns */
    gap: 2rem; /* Space between the forms */
    align-items: start; /* Align items to the top */
}

/* Optional: Make it responsive */
@media (max-width: 768px) {
    .hero-container {
        grid-template-columns: 1fr; /* Stack on mobile */
        gap: 1rem;
    }
}

.pitch-deck-section,
.chat-section {
    width: 100%;
    height: 100%;
}

.output {
    margin-bottom: 2rem;
    padding: 1rem;
    border: 1px solid #ddd;
    border-radius: 4px;
}

.feedback {
    padding: 1rem;
    background-color: #f8f9fa;
    border-radius: 4px;
}
</style>

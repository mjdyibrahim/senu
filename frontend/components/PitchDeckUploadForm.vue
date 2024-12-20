<template>
    <div id="form-container" class="pitch-deck-form-container">
        <h3>Upload Pitch Deck -> Get instant score</h3>
        <form
            id="pitchDeckForm"
            class="pitch-deck-form"
            @submit.prevent="handleSubmit"
            enctype="multipart/form-data"
        >
            <input
                type="email"
                id="email"
                v-model="email"
                name="email"
                autocomplete="email"
                placeholder="Your Email"
                required
            />
            <input
                type="file"
                id="pitchDeck"
                ref="fileInput"
                @change="handleFileChange"
                name="file"
                accept="application/pdf"
                required
            />
            <button id="submitBtn" type="submit" :disabled="isSubmitting">
                {{ isSubmitting ? "Processing ... " : "Analyze my Pitch Deck" }}
            </button>
        </form>
    </div>
</template>

<script setup>
import { ref } from "vue";

const emit = defineEmits(["submit"]);
const email = ref("");
const fileInput = ref(null);
const isSubmitting = ref(false);

const handleFileChange = (event) => {
    // Optional: Add file validation here
    const file = event.target.files[0];
    if (file && file.type !== "application/pdf") {
        alert("Please upload a PDF file");
        event.target.value = ""; // Clear the input
    }
};

const handleSubmit = async () => {
    if (!email.value || !fileInput.value?.files?.[0]) {
        alert("Please provide both email and pitch deck.");
        return;
    }

    isSubmitting.value = true;

    try {
        const formData = new FormData();
        formData.append("email", email.value);
        formData.append("file", fileInput.value.files[0]);

        // You might want to add your API endpoint here
        const response = await fetch("/api/upload", {
            method: "POST",
            body: formData,
        });

        if (!response.ok) {
            throw new Error("Upload failed");
        }

        const result = await response.json();
        emit("submit", result);

        // Clear form after successful submission
        email.value = "";
        if (fileInput.value) {
            fileInput.value.value = "";
        }
    } catch (error) {
        console.error("Error uploading file:", error);
        alert("Failed to upload file. Please try again.");
    } finally {
        isSubmitting.value = false;
    }
};
</script>

<style scoped>
/* Import your main styles */

.pitch-deck-form-container {
    width: 100%; /* Take full width of parent */
    padding: 20px;
    box-sizing: border-box;
}

.pitch-deck-form {
    width: 100%;
    display: flex;
    flex-direction: column;
    gap: 1rem;
}

.pitch-deck-form input[type="email"],
.pitch-deck-form input[type="file"] {
    width: 100%;
    padding: 8px;
    border: 1px solid #ddd;
    border-radius: 4px;
    box-sizing: border-box;
}

.pitch-deck-form button {
    width: 100%;
    padding: 10px 20px;
    background-color: #007bff;
    color: white;
    border: none;
    border-radius: 4px;
    cursor: pointer;
}

.pitch-deck-form button:disabled {
    background-color: #cccccc;
    cursor: not-allowed;
}
</style>

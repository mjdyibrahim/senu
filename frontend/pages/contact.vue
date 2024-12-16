<template>
    <main class="contact min-h-screen">
        <h1>Contact Us</h1>
        <p>If you have any questions, feel free to reach out to us using the form below.</p>
        <form @submit.prevent="submitForm" class="contact-form">
            <div class="form-group">
                <label for="name">Name:</label>
                <input type="text" id="name" v-model="form.name" required />
            </div>
            <div class="form-group">
                <label for="email">Email:</label>
                <input type="email" id="email" v-model="form.email" required />
            </div>
            <div class="form-group">
                <label for="message">Message:</label>
                <textarea id="message" v-model="form.message" required></textarea>
            </div>
            <button type="submit">Send Message</button>
        </form>
    </main>
</template>

<script setup lang="ts">
import { ref } from 'vue';

const form = ref({
    name: '',
    email: '',
    message: ''
});

const submitForm = () => {
    // Handle form submission logic here
    console.log('Form submitted:', form.value);
    // Reset form after submission
    form.value = { name: '', email: '', message: '' };
};
</script>

<style scoped>
.contact {
    padding: 20px;
    max-width: 600px; /* Limit the width of the contact form */
    margin: auto; /* Center the form on the page */
}

.contact-form {
    display: flex;
    flex-direction: column;
}

.form-group {
    margin-bottom: 15px; /* Space between form fields */
}

label {
    margin-bottom: 5px; /* Space between label and input */
    font-weight: bold; /* Make labels bold */
}

input, textarea {
    width: 100%; /* Full width for inputs */
    padding: 10px; /* Increased padding for better touch targets */
    border: 1px solid #ccc;
    border-radius: 4px;
    font-size: 16px; /* Increase font size for better readability */
}

textarea {
    resize: vertical; /* Allow vertical resizing of the textarea */
    min-height: 100px; /* Set a minimum height for the textarea */
}

button {
    padding: 10px;
    background-color: #007BFF;
    color: white;
    border: none;
    border-radius: 4px;
    cursor: pointer;
    font-size: 16px; /* Increase font size for better readability */
}

button:hover {
    background-color: #0056b3;
}
</style>
<template>
  <div>
    <div class="gradient-background"></div>
    <div class="container">
      <!-- Hero Section -->
      <section class="hero">
        <h1 class="hero-title">
          Refine the Next Generation of AI with Your Expertise
        </h1>
        <p class="hero-subtitle">
          Join our network of experts and help shape the future of AI technology
        </p>
        <button class="button primary-button">Get Started</button>
      </section>

      <!-- Features Section -->
      <section class="features">
        <div class="feature-card">
          <div class="feature-icon">
            <!-- Add icon here -->
          </div>
          <h3>Expert Network</h3>
          <p>Connect with leading AI researchers and practitioners</p>
        </div>
        <div class="feature-card">
          <div class="feature-icon">
            <!-- Add icon here -->
          </div>
          <h3>AI Development</h3>
          <p>Contribute to cutting-edge AI models and applications</p>
        </div>
        <div class="feature-card">
          <div class="feature-icon">
            <!-- Add icon here -->
          </div>
          <h3>Flexible Collaboration</h3>
          <p>Work on projects that match your expertise and schedule</p>
        </div>
      </section>
    </div>
  </div>
</template>

<script setup lang="ts">
// Add any necessary imports and component logic here
</script>

<style scoped>

@import url('https://fonts.googleapis.com/css2?family=Inter+Tight:wght@400;500;600;700&display=swap');

/* Reset and base styles */

body {
  font-family: 'Inter Tight', sans-serif;
  background: rgb(254, 253, 250);
  color: rgb(27, 0, 48);
}

* {
  box-sizing: border-box;
  margin: 0;
  padding: 0;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
}

:root {
  --primary-dark: rgb(27, 0, 48);
  --primary-light: rgb(255, 255, 255);
  --accent-purple: rgb(89, 79, 238);
  --text-gray: rgb(69, 62, 74);
  --background-light: rgb(254, 253, 250);
}

/* Background styles */
.gradient-background {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background: rgb(254, 253, 250);
  z-index: -1;
}

/* Container styles */
.container {
  max-width: 1200px;
  margin: 0 auto;
  padding: 0 2rem;
}

/* Navigation styles */
.nav {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 1rem 0;
}

/* Button styles */
.button {
  background: var(--accent-purple);
  color: var(--primary-light);
  padding: 0.75rem 1.5rem;
  border-radius: 8px;
  border: none;
  cursor: pointer;
  transition: background-color 0.3s ease;
}

.button:hover {
  background: rgb(81, 72, 217);
}

/* Add more specific styles as needed */
</style>

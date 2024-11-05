<template>
  <div id="form-container">
    <h3>Upload Pitch Deck -> Get instant score</h3>
    <form id="pitchDeckForm" action="/upload" method="post" enctype="multipart/form-data" @submit.prevent="submitForm">
      <input type="email" id="email" name="email" autocomplete="email" placeholder="Your Email" required>
      <input type="file" id="pitchDeck" name="file" accept="application/pdf" required>
      <button id="submitBtn" type="submit">Analyze my Pitch Deck</button>
    </form>
  </div>
</template>

<script>
export default {
  methods: {
    submitForm() {
      // Handle form submission logic here
    }
  }
}
</script>

<style scoped>
/* Your styles go here */
</style>

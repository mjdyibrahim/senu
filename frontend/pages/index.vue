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
import Header from '~/components/Header/Header.vue'
import Footer from '~/components/Footer/Footer.vue'
import PitchDeckUploadForm from '~/components/PitchDeckUploadForm.vue'
import ChatForm from '~/components/ChatForm.vue'

export default {
  components: {
    Header,
    Footer,
    PitchDeckUploadForm,
    ChatForm
  }
}
</script>

<style scoped>
/* Your styles go here */
</style>

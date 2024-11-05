<template>
  <div>
    <Header />
    <section class="chat">
      <div class="chatbox-container" id="chatbox">
        <!-- Chatbox content goes here -->
      </div>
    </section>
    <Footer />
  </div>
</template>

<script>
import Header from '~/components/Header/Header.vue'
import Footer from '~/components/Footer/Footer.vue'

export default {
  components: {
    Header,
    Footer
  }
}
</script>

<style scoped>
/* Your styles go here */
</style>

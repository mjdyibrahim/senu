<template>
  <div>
    <Header />
    <main>
      <!-- Main content goes here -->
    </main>
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

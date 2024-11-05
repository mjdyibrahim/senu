<template>
  <div>
    <Header />
    <main class="main-content">
      <section class="auth-section">
        <h2>Register</h2>
        <form action="/register" method="post" class="auth-form">
          <!-- Registration form content goes here -->
        </form>
        <p class="auth-switch">Already have an account? <nuxt-link to="/signin">Sign In</nuxt-link></p>
      </section>
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

<template>
  <div>
    <Header />
    <main class="main-content">
      <section class="auth-section">
        <h2>Sign In</h2>
        <form action="/login" method="post" class="auth-form">
          <div class="form-group">
            <label for="email">Email</label>
            <input type="email" id="email" name="email" placeholder="Enter your email" required>
          </div>
          <div class="form-group">
            <label for="password">Password</label>
            <input type="password" id="password" name="password" placeholder="Enter your password" required>
          </div>
          <button type="submit" class="btn btn-primary">Sign In</button>
        </form>
        <p class="auth-switch">Don't have an account? <nuxt-link to="/register">Register</nuxt-link></p>
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

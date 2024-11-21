<template>
  <header>
    <nav>
      <div class="logo">Senu</div>
      <ul class="nav-links">
        <li><nuxt-link to="/"><i class="fas fa-home"></i> Home</nuxt-link></li>
        <li><nuxt-link to="/dashboard"><i class="fas fa-tachometer-alt"></i> Dashboard</nuxt-link></li>
        <li><nuxt-link to="/feedback"><i class="fas fa-chart-line"></i> Feedback</nuxt-link></li>
        <li><nuxt-link to="/resources"><i class="fas fa-book"></i> Resources</nuxt-link></li>
        <li><nuxt-link to="/login"><i class="fas fa-sign-in-alt"></i> Log In</nuxt-link></li>
      </ul>
    </nav>
  </header>
</template>

<script>
export default {
  // Your script goes here
}
</script>

<style scoped>
/* Your styles go here */
</style>

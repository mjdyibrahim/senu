<template>
  <div>
      <Header />

      <Footer />
  </div>
</template>

<script>
export default {
  middleware: 'auth',
  // ... rest of the script ...
}
</script>

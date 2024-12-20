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

<style scoped>
.dashboard {
  @apply py-12 px-5 text-center;
}

.wizard {
  @apply bg-white p-5 rounded-lg shadow-md max-w-4xl mx-auto text-left;
}

.progress-bar {
  @apply h-5 bg-accent-purple w-0 text-center text-white transition-[width];
}

/* ... other dashboard-specific styles ... */
</style>

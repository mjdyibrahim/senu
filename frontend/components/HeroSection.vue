<template>
  <div class="relative bg-gradient-to-br from-primary to-[#003087] min-h-screen flex items-center">
    <div class="absolute inset-0">
      <div class="absolute inset-0 bg-[url('https://images.unsplash.com/photo-1551434678-e076c223a692?ixlib=rb-1.2.1&auto=format&fit=crop&w=2850&q=80')] mix-blend-overlay opacity-10"></div>
    </div>
    
    <div class="relative max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-32">
      <div class="text-center">
        <h1 class="text-4xl sm:text-5xl md:text-6xl font-bold text-black mb-6">
          AI-Powered Solutions for Entrepreneurs and Employers
        </h1>
        <p class="text-xl md:text-2xl text-gray-200 mb-12 max-w-3xl mx-auto">
          Delivering high-quality, templated services with human-AI collaboration
        </p>
        <div class="flex flex-col sm:flex-row gap-4 justify-center">
          <BaseButton variant="secondary" class="group">
            Explore Services for Entrepreneurs
            <Icon name="mdi:arrow-right" class="ml-2 h-5 w-5 group-hover:translate-x-1 transition-transform" />
          </BaseButton>
          <BaseButton variant="outline" class="group">
            Order Deliverables for Employers
            <Icon name="mdi:arrow-right" class="ml-2 h-5 w-5 group-hover:translate-x-1 transition-transform" />
          </BaseButton>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
</script>

<style scoped>
.hero {
  @apply bg-accent-purple text-white py-12 px-5 text-center min-h-[650px] relative overflow-hidden;
}

.hero h2 {
  @apply text-4xl mb-5;
}

.hero p {
  @apply text-lg mb-5;
}

.hero form {
  @apply flex flex-col md:flex-row items-center justify-center gap-12 my-12 border-2 border-white;
}

/* ... other hero-specific styles ... */
</style>
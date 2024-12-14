<template>
  <footer class="bg-gray-800 text-white py-6">
    <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
      <div class="flex justify-between items-center">
        <div>
          <h2 class="text-lg font-bold">Empowering Economic Builders</h2>
          <p class="mt-1 text-sm">AI that empowers economic builders in emerging markets.</p>
        </div>
        <nav class="space-x-4">
          <NuxtLink to="/about" class="hover:underline">About Us</NuxtLink>
          <NuxtLink to="/services" class="hover:underline">Services</NuxtLink>
          <NuxtLink to="/contact" class="hover:underline">Contact</NuxtLink>
        </nav>
      </div>
      <div class="mt-4 flex justify-center space-x-4">
        <NuxtIcon name="twitter" class="h-6 w-6" />
        <NuxtIcon name="linkedin" class="h-6 w-6" />
        <NuxtIcon name="facebook" class="h-6 w-6" />
      </div>
      <div class="mt-4 text-center text-sm">
        &copy; {{ new Date().getFullYear() }} Senu AI. All rights reserved..
      </div>
    </div>
  </footer>
</template>

<script setup lang="ts">
// You can add any necessary script logic here
</script>

<style scoped>
/* Add any specific styles for the footer here */
</style>

<template>
  <header class="header fixed w-full backdrop-blur-sm z-50 shadow-sm">
    <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
      <div class="flex justify-between items-center py-4">
        <div class="flex items-center">
          <span class="text-2xl font-bold">{{ siteConfig.name }}</span>
        </div>
        
        <nav class="hidden md:flex space-x-8">
          <NuxtLink
            v-for="item in siteConfig.nav"
            :key="item.href"
            :to="item.href"
            class="text-gray-700 hover:text-primary"
          >
            {{ item.label }}
          </NuxtLink>
        </nav>

        <div class="hidden md:flex">
          <BaseButton>Get Started</BaseButton>
        </div>

        <button 
          class="md:hidden"
          @click="isMenuOpen = !isMenuOpen"
        >
          <span v-if="!isMenuOpen" class="h-6 w-6" >☰</span> 
          <span v-else class="h-6 w-6" >✖</span>
        </button>
      </div>
    </div>

    <div v-if="isMenuOpen" class="md:hidden">
      <div class="px-2 pt-2 pb-3 space-y-1 sm:px-3">
        <NuxtLink
          v-for="item in siteConfig.nav"
          :key="item.href"
          :to="item.href"
          class="block px-3 py-2 text-gray-700"
        >
          {{ item.label }}
        </NuxtLink>
      </div>
    </div>
  </header>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import { siteConfig } from '~/config/site'
</script>

<style scoped>
.header {
  background-color: #1a1a1a; /* Dark background */
  color: var(--primary-color); /* White text */
}

.header .text-primary {
  color: #ffcc00; /* Distinct color for primary text */
}

.header .nav-links a {
  color: #ffffff; /* White links */
  transition: color 0.3s;
}

.header .nav-links a:hover {
  color: #ffcc00; /* Change color on hover */
}

.header .button {
  background-color: #ffcc00; /* Button color */
  color: #1a1a1a; /* Button text color */
  border: none;
  padding: 10px 20px;
  border-radius: 5px;
  cursor: pointer;
}

.header .button:hover {
  background-color: #e6b800; /* Darker button on hover */
}
</style>
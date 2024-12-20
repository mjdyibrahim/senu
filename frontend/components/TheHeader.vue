<template>
  <header class="top-0 left-0 right-0 bg-background-light z-50 h-[80px]">
    <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
      <div class="flex justify-between items-center py-4">
        <div class="flex items-center">
          <span class="text-2xl font-bold text-black">{{ siteConfig.name }}</span>
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

const isMenuOpen = ref(false)
</script>

<style scoped>

</style>
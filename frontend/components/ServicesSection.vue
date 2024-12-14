<template>
  <section id="services" class="py-24 bg-accent">
    <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
      <div class="text-center mb-16">
        <h2 class="text-3xl md:text-4xl font-bold text-primary mb-4">
          Our Featured Services
        </h2>
        <p class="text-gray-600 max-w-2xl mx-auto">
          Leverage the power of AI and human expertise to grow your business with our comprehensive service offerings.
        </p>
      </div>

      <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-8">
        <div
          v-for="service in services"
          :key="service.slug"
          class="bg-white rounded-lg p-6 shadow-lg hover:shadow-xl transition-shadow"
        >
          <div class="w-12 h-12 bg-primary/10 rounded-lg flex items-center justify-center mb-4">
            <component :is="service.icon" class="h-6 w-6 text-primary" />
          </div>
          <h3 class="text-xl font-semibold text-primary mb-2">
            {{ service.title }}
          </h3>
          <p class="text-gray-600 mb-4">{{ service.description }}</p>
          <button class="text-primary font-medium hover:text-secondary transition-colors">
            Learn More →
          </button>
        </div>
      </div>
    </div>
  </section>
</template>

<script setup lang="ts">
import { services } from '~/config/services'
</script>
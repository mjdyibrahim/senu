<template>
  <div class="min-h-screen flex flex-col">
    <main class="flex-1 pt-[80px]">
      <HeroSection />
      <CustomImageSection />

      <ServicesSection />

      <section class="bg-primary py-24">
    <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
      <div class="text-center">
        <h2 class="text-3xl md:text-4xl font-bold mb-6">
          Ready to Transform Your Business?
        </h2>
        <p class="text-xl text-gray-200 mb-12 max-w-2xl mx-auto">
          Join thousands of entrepreneurs and businesses leveraging AI-powered solutions for growth.
        </p>
        <div class="flex flex-col sm:flex-row gap-4 justify-center">
          <BaseButton variant="secondary" class="group">
            Get Started Now
            <Icon name="mdi:arrow-right" class="ml-2 h-5 w-5 group-hover:translate-x-1 transition-transform" />
          </BaseButton>
          <a
            href="https://t.me/senuai_bot"
            target="_blank"
            rel="noopener noreferrer"
          >
            <BaseButton variant="outline" class="group w-full sm:w-auto">
              Chat on Telegram
              <Icon name="mdi:message-circle" class="ml-2 h-5 w-5 group-hover:translate-x-1 transition-transform" />
            </BaseButton>
          </a>
        </div>
      </div>
        </div>
      </section>

      <section class="py-16 px-8 text-center">
        <div class="container mx-auto max-w-6xl">
          <h2 class="text-3xl md:text-4xl font-bold mb-8 text-primary-dark">
            Explore Our Offerings
          </h2>
          <div class="flex flex-col md:flex-row justify-center gap-4 md:gap-6">
            <BaseButton 
              variant="secondary" 
              @click="navigateToPitchSimulator"
              class="w-full md:w-auto"
            >
              Virtual Pitch Simulator
            </BaseButton>
            <BaseButton 
              variant="outline" 
              @click="navigateToProductizedServices"
              class="w-full md:w-auto"
            >
              Productized Services
            </BaseButton>
          </div>
        </div>
      </section>
    </main>
  </div>
</template>

<script setup lang="ts">
import { useRouter } from 'vue-router'

const router = useRouter()

const navigateToPitchSimulator = () => {
  router.push('/pitch-simulator')
}

const navigateToProductizedServices = () => {
  router.push('/productized-services')
}
</script>
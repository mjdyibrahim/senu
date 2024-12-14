<template>
    <main>
      <HeroSection />
      <ServicesSection />
      <CTASection />
      <section class="cta-dual-purpose">
        <div class="cta-container">
          <h2>Explore Our Offerings</h2>
          <div class="cta-buttons">
            <BaseButton variant="secondary" @click="navigateToPitchSimulator">
              Virtual Pitch Simulator
            </BaseButton>
            <BaseButton variant="outline" @click="navigateToProductizedServices">
              Productized Services
            </BaseButton>
          </div>
        </div>
      </section>
    </main>
  </template>

<script setup lang="ts">
import TheHeader from '~/components/TheHeader.vue'
import { useRouter } from 'vue-router'

const router = useRouter()

const navigateToPitchSimulator = () => {
  router.push('/pitch-simulator')
}

const navigateToProductizedServices = () => {
  router.push('/productized-services')
}
</script>

<style scoped>
.cta-dual-purpose {
  padding: 2rem;
  text-align: center;
}

.cta-buttons {
  display: flex;
  justify-content: center;
  gap: 1rem;
}
</style>
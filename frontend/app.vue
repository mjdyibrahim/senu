<template>
    <TheHeader />
    <NuxtPage />
    <TheFooter />
</template>

<script setup lang="ts">
import { onMounted } from 'vue'
import { useAuthStore } from "@/stores/auth"
import { useHead } from '@vueuse/head'
import TheHeader from '~/components/TheHeader.vue'
import TheFooter from '~/components/TheFooter.vue'

const auth = useAuthStore()

// Check auth status when app loads
onMounted(() => {
  auth.checkAuth()
})

useHead({
  title: 'AI Empowering Economic Builders, Entrepreneurs and SMEs',
  meta: [
    { charset: 'utf-8' },
    { name: 'viewport', content: 'width=device-width, initial-scale=1' },
    { hid: 'description', name: 'description', content: 'AI Empowering Economic Builders, Entrepreneurs and SMEs' },
    // Add other meta tags as needed
  ],
})
</script>

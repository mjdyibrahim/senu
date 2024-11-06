import { defineNuxtConfig } from "nuxt/config";
import { config } from 'dotenv';

config({ path: '../.env' }); // Load environment variables from the parent directory

export default defineNuxtConfig({
  compatibilityDate: '2024-04-03',
  devtools: { enabled: true },
  modules: [
    '@nuxtjs/tailwindcss',
    // ... rest of the modules
  ],
  css: ['@/assets/css/tailwind.css'],
  tailwindcss: {
    config: {
      content: [
        './components/**/*.{vue,js}',
        './layouts/**/*.vue',
        './pages/**/*.vue',
        './plugins/**/*.{js,ts}',
        './nuxt.config.{js,ts}',
      ],
      theme: {
        extend: {},
      },
      plugins: [],
    },
  },
  env: {
    SUPABASE_URL: process.env.SUPABASE_URL,
    // Add other environment variables you need here
  },
  // ... rest of the configuration
})

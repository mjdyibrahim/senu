import { defineNuxtConfig } from "nuxt/config";
import { config } from "dotenv";

config({ path: "../.env" }); // Load environment variables from the parent directory

export default defineNuxtConfig({
  compatibilityDate: "2024-04-03",
  devtools: { enabled: true },
  modules: [
    "@nuxtjs/tailwindcss",
    "@nuxtjs/supabase",

    // ... rest of the modules
  ],
  css: ["@/assets/css/tailwind.css"],
  tailwindcss: {
    config: {
      content: [
        "./components/**/*.{vue,js}",
        "./layouts/**/*.vue",
        "./pages/**/*.vue",
        "./plugins/**/*.{js,ts}",
        "./nuxt.config.{js,ts}",
      ],
      theme: {
        extend: {},
      },
      plugins: [],
    },
  },
  supabase: {
    url: useRuntimeConfig().public.SUPABASE_URL,
    key: useRuntimeConfig().public.SUPABASE_ANON_KEY,
    redirect: true,
    // Optional: Add other Supabase configurations here
    // redirectOptions: {
    //   login: '/login',
    //   callback: '/confirm'
    // }
  },
  // ... rest of the configuration
});

import { defineNuxtConfig } from "nuxt/config";
import { config } from "dotenv";

config({ path: "../.env" }); // Load environment variables from the current directory

export default defineNuxtConfig({
  compatibilityDate: "2024-04-03",
  devtools: {
    enabled: true,

    timeline: {
      enabled: true,
    },
  },
  modules: [
    "@nuxtjs/tailwindcss",
    "@nuxtjs/supabase",
    "@pinia/nuxt",
    "@nuxt/icon",

    // ... rest of the modules
  ],
  css: ["@/assets/css/tailwind.css", "@/assets/css/main.css"],
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
      cssPath: "./assets/css/tailwind.css",
      configPath: "./tailwind.config.ts",
      exposeConfig: true,
    },
  },
  supabase: {
    url: process.env.SUPABASE_URL,
    key: process.env.SUPABASE_ANON_KEY,
    redirect: true,
    redirectOptions: {
      login: "/login",
      callback: "/confirm",
      exclude: ["/*"],
    },
  },
  pinia: {},
  // ... rest of the configuration
  build: {
    transpile: ['@supabase/supabase-js'],
  },
});

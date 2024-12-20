<template>
  <button 
    :class="[
      'px-6 py-3 rounded-lg transition-colors duration-200',
      variant === 'secondary' ? 'bg-accent-purple text-white hover:bg-purple-700' :
      variant === 'outline' ? 'border-2 border-accent-purple text-accent-purple hover:bg-accent-purple hover:text-white' :
      'bg-primary-dark text-white hover:bg-primary-dark/90'
    ]"
  >
    <slot />
  </button>
</template>

<script setup lang="ts">
defineProps<{
  variant?: 'primary' | 'secondary' | 'outline'
}>()
</script>
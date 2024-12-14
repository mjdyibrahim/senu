<template>
  <button
    :class="[
      'inline-flex items-center justify-center rounded-md text-sm font-medium transition-colors focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-offset-2 disabled:pointer-events-none disabled:opacity-50 px-6 py-2',
      variantClasses[variant],
      className
    ]"
    v-bind="$attrs"
  >
    <slot />
  </button>
</template>

<script setup lang="ts">
interface Props {
  variant?: 'primary' | 'secondary' | 'outline'
  className?: string
}

const props = withDefaults(defineProps<Props>(), {
  variant: 'primary',
  className: ''
})

const variantClasses = {
  primary: 'bg-primary text-white hover:bg-primary/90',
  secondary: 'bg-secondary text-primary hover:bg-secondary/90',
  outline: 'border-2 border-white text-white hover:bg-white/10'
}
</script>
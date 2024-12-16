<template>
  <section class="bg-primary py-24">
    <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
      <div class="text-center">
        <h2 class="text-3xl md:text-4xl font-bold text-white mb-6">
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
</template>

<script setup lang="ts">
</script>
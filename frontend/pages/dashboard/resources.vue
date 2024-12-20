<template>
    <div>
        <TheHeader />
        <main class="main-content">
            <section class="resources">
                <!-- Roadmap section content goes here -->
            </section>
        </main>
        <TheFooter />
    </div>
</template>

<script>
import TheHeader from "~/components/TheHeader.vue";
import TheFooter from "~/components/TheFooter.vue";

export default {
    components: {
        TheHeader,
        TheFooter,
    },
};
</script>

<style scoped>
.resources {
  @apply py-12 px-5 text-center;
}

.resource-list {
  @apply bg-white p-5 rounded-lg shadow-md max-w-4xl mx-auto text-left;
}

/* ... other resources-specific styles ... */
</style>

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
/* Import main style */
@import "@/assets/css/main.css";
</style>

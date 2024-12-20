<template>
    <div>
        <Header />
        <main class="main-content">
            <section class="roadmap">
                <!-- Roadmap section content goes here -->
            </section>
        </main>
        <Footer />
    </div>
</template>

<script>
import Header from "~/components/Header/Header.vue";
import Footer from "~/components/Footer/Footer.vue";

export default {
    components: {
        Header,
        Footer,
    },
};
</script>

<style scoped>
/* Import main style */
</style>

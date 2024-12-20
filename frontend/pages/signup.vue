<template>
    <div>
        <Header />
        <main class="main-content">
            <section class="auth-section">
                <h2>Register</h2>

                <p class="auth-switch">
                    Already have an account?
                    <nuxt-link to="/signin">Sign In</nuxt-link>
                </p>
            </section>
        </main>
        <Footer />
    </div>
</template>

<script>
definePageMeta({
    middleware: ["guest"],
});

import Header from "~/components/Header/Header.vue";
import Footer from "~/components/Footer/Footer.vue";

export default {
    components: {
        Header,
        Footer,
    },
    methods: {
        submitForm() {
            // Handle form submission logic here
        },
    },
};
</script>

<style scoped>
/* Import main style */
</style>

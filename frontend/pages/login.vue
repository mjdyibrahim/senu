<template>
    <div>
        <Header />
        <main class="main-content">
            <section class="auth-section">
                <h2>Log In</h2>
                <LoginForm />
                <p class="auth-switch">
                    Don't have an account?
                    <nuxt-link to="/signup">Signup</nuxt-link>
                </p>
            </section>
        </main>
        <Footer />
    </div>
</template>

<script>
import Header from "~/components/Header/Header.vue";
import Footer from "~/components/Footer/Footer.vue";
import LoginForm from "~/components/LoginForm.vue";
import "~/assets/js/utils";

export default {
    components: {
        Header,
        Footer,
        LoginForm,
    },
};
</script>

<style scoped>
/* Your styles go here */

</style>

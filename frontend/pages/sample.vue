<template>
    <div>
        <Header />
        <Sidebar />
        <main>
            <!-- Main content goes here -->
        </main>
        <Footer />
    </div>
</template>

<script>
import Header from "~/components/Header/Header.vue";
import Footer from "~/components/Footer/Footer.vue";
import Sidebar from "~/components/Sidebar/Sidebar.vue";

export default {
    components: {
        Header,
        Footer,
        Sidebar,
    },
};
</script>

<style scoped>
/* Import main style */
@import "@/assets/css/main.css";
</style>

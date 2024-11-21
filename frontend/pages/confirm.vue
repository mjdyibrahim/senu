<template>
    <div>
        <Header />
        <main class="main-content">
            <section class="confirmation-section">
                <div v-if="loading">Confirming your email...</div>
                <div v-else-if="error">{{ error }}</div>
                <div v-else>
                    <h2>Email Confirmed!</h2>
                    <p>You can now login to your account.</p>
                    <NuxtLink to="/login" class="btn btn-primary">
                        Go to Login
                    </NuxtLink>
                </div>
            </section>
        </main>
        <Footer />
    </div>
</template>

<script setup>
import { ref, onMounted } from "vue";
const loading = ref(true);
const error = ref("");

onMounted(async () => {
    try {
        const { $supabase } = useNuxtApp();
        const hash = window.location.hash;
        const hashParams = new URLSearchParams(hash.substring(1));
        const type = hashParams.get("type");

        if (type === "signup") {
            await $supabase.auth.confirmSignUp();
            loading.value = false;
        }
    } catch (e) {
        error.value = e.message;
    } finally {
        loading.value = false;
    }
});
</script>

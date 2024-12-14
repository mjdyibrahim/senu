<template>
    <form @submit.prevent="handleLogin" class="auth-form space-y-4">
        <div class="form-group">
            <label for="email">Email</label>
            <input
                v-model="email"
                type="email"
                id="email"
                placeholder="Email"
                required
            />
        </div>
        <div class="form-group">
            <label for="password">Password</label>
            <input
                v-model="password"
                type="password"
                id="password"
                placeholder="Password"
                required
            />
        </div>
        <button type="submit" class="btn btn-primary">Login</button>
        <p v-if="error" class="text-red-500">{{ error }}</p>
    </form>
</template>

<script setup>
import { ref } from "vue";
import { useAuthStore } from "@/stores/auth";

const auth = useAuthStore();
const email = ref("");
const password = ref("");
const error = ref("");

onMounted(async () => {
    await auth.checkAuth();
});

const handleLogin = async () => {
    try {
        error.value = "";
        await auth.login({
            email: email.value,
            password: password.value,
        });
    } catch (e) {
        error.value = e.message || "Login failed";
    }
};
</script>

<style>
@import "@/assets/css/main.css";
</style>

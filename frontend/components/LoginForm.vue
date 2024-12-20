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


/* Authentication Styles */
.auth-section {
    max-width: 400px;
    margin: 2rem auto;
    padding: 2rem;
    background-color: #fff;
    border-radius: 8px;
    box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

.auth-form .form-group {
    margin-bottom: 1rem;
}

.auth-form label {
    display: block;
    margin-bottom: 0.5rem;
    color: #333;
}

.auth-form input {
    width: 100%;
    padding: 0.5rem;
    border: 1px solid #ced4da;
    border-radius: 4px;
    font-size: 16px;
}

.auth-form .btn-primary {
    width: 100%;
    padding: 0.75rem;
    background-color: #4caf50;
    color: white;
    border: none;
    border-radius: 4px;
    cursor: pointer;
    font-size: 16px;
    transition: background-color 0.3s;
}

.auth-form .btn-primary:hover {
    background-color: #45a049;
}

.auth-switch {
    text-align: center;
    margin-top: 1rem;
    color: #666;
}

.auth-switch a {
    color: #4caf50;
    text-decoration: none;
}

.auth-switch a:hover {
    text-decoration: underline;
}

</style>

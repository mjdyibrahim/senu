<template>
    <form @submit.prevent="handleLogin" class="space-y-4">
        <div>
            <input v-model="email" type="email" placeholder="Email" required />
        </div>
        <div>
            <input
                v-model="password"
                type="password"
                placeholder="Password"
                required
            />
        </div>
        <div>
            <button type="submit">Login</button>
        </div>
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
``` 7. Update your `app.vue`: ```vue
<template>
    <div>
        <NuxtLayout>
            <NuxtPage />
        </NuxtLayout>
    </div>
</template>

<script setup>
import { useAuthStore } from "@/stores/auth";

const auth = useAuthStore();

onMounted(async () => {
    await auth.checkAuth();
});
</script>

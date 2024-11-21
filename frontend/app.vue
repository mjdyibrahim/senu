<template>
    <NuxtPage />
</template>
<script setup>
import { useAuthStore } from "@/stores/auth";

const auth = useAuthStore();

// Check auth status when app loads
onMounted(() => {
    auth.checkAuth();
});
</script>

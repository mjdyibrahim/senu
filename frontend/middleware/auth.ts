export default defineNuxtRouteMiddleware(async (to, from) => {
  const auth = useAuthStore();

  if (!auth.user && to.path !== "/login") {
    return navigateTo("/login");
  }

  if (auth.user && to.path === "/login") {
    return navigateTo("/dashboard");
  }
});

export default defineNuxtRouteMiddleware(async (to, from) => {
  const { $supabase } = useNuxtApp();
  const user = await $supabase.auth.getUser();

  if (!user.data.user && to.path !== "/login") {
    return navigateTo("/login");
  }

  if (user.data.user && to.path === "/login") {
    return navigateTo("/dashboard");
  }
});

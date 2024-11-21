export default defineNuxtPlugin((nuxtApp) => {
  const supabase = useSupabaseClient();

  console.log("Supabase URL:", supabase.supabaseUrl);
  console.log("Supabase Key:", supabase.supabaseKey);
});

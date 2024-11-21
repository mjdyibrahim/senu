import { createClient } from "@supabase/supabase-js";

export default defineNuxtPlugin((nuxtApp) => {
  const supabaseUrl = useRuntimeConfig().public.SUPABASE_URL;
  const supabaseKey = useRuntimeConfig().public.SUPABASE_ANON_KEY;
  const supabase = createClient(supabaseUrl, supabaseKey);

  console.log("Supabase URL:", supabaseUrl);
  console.log("Supabase Key:", supabaseKey);

  nuxtApp.provide("supabase", supabase);
});

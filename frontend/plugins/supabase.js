import { createClient } from "@supabase/supabase-js";

export default defineNuxtPlugin((nuxtApp) => {
  const config = useRuntimeConfig();
  const supabaseUrl = config.public.SUPABASE_URL;
  const supabaseKey = config.public.SUPABASE_ANON_KEY;

  console.log("Supabase URL from runtime config:", supabaseUrl);
  console.log("Supabase Key from runtime config:", supabaseKey);

  if (!supabaseUrl || !supabaseKey) {
    throw new Error('Supabase URL and Anon Key are required.');
  }

  const supabase = createClient(supabaseUrl, supabaseKey);

  console.log("Supabase URL:", supabaseUrl);
  console.log("Supabase Key:", supabaseKey);

  nuxtApp.provide("supabase", supabase);
});

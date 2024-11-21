<script setup>
const { $supabase } = useNuxtApp()

const { data, error } = await $supabase
  .from('your_table')
  .select('*')
</script>
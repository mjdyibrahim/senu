import { createClient } = require('@supabase/supabase-js')

// Use environment variables to store sensitive information
const supabaseUrl = process.env.SUPABASE_URL || 'http://localhost:54322'
const supabaseAnonKey = process.env.SUPABASE_ANON_KEY || 'your-local-anon-key'

// Create a Supabase client
export const supabase = createClient(supabaseUrl, supabaseAnonKey)
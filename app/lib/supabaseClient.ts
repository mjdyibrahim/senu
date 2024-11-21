import { createClient } from "@supabase/supabase-js";

// This TypeScript code is part of a hybrid Python/Node.js project
// The TypeScript/JavaScript portions run in Node.js alongside Python
// They communicate via APIs, shared files, or IPC mechanisms
// The package.json indicates Node.js dependencies like supabase-js client
const supabaseUrl = process.env.SUPABASE_URL;
const supabaseAnonKey = process.env.SUPABASE_ANON_KEY;

// Create Supabase client for Node.js portions of hybrid app
export const supabase = createClient(supabaseUrl, supabaseAnonKey);

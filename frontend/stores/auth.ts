import { defineStore } from "pinia";
import type { User } from "#supabase/server";

interface AuthState {
  user: User | null;
  loading: boolean;
  isAuthenticated: false;
}

export const useAuthStore = defineStore("auth", {
  state: (): AuthState => ({
    user: null,
    loading: false,
    isAuthenticated: false,
  }),

  actions: {
    async getUser() {
      const { $supabase } = useNuxtApp();
      const {
        data: { user },
        error,
      } = await $supabase.client.auth.getUser();
      if (error) throw error;
      this.user = user;
      return user;
    },
    async login(credentials: { email: string; password: string }) {
      try {
        const { $supabase } = useNuxtApp();
        const { data, error } = await $supabase.auth.signInWithPassword({
          email: credentials.email,
          password: credentials.password,
        });

        if (error) throw error;

        this.user = data.user;
        this.isAuthenticated = true;

        return navigateTo("/dashboard");
      } catch (error) {
        console.error("Login error:", error);
        throw error;
      }
    },

    async register(credentials: { email: string; password: string }) {
      try {
        const { $supabase } = useNuxtApp();
        const { data, error } = await $supabase.auth.signUp({
          email: credentials.email,
          password: credentials.password,
          // Optional: Add additional user data
          options: {
            data: {
              // Add any additional user metadata here
              registered_at: new Date().toISOString(),
            },
          },
        });

        if (error) throw error;

        // Optional: Auto-login after registration
        // this.user = data.user
        // this.isAuthenticated = true

        return data;
      } catch (error) {
        console.error("Registration error:", error);
        throw error;
      }
    },

    async logout() {
      try {
        const { $supabase } = useNuxtApp();
        await $supabase.auth.signOut();
        this.user = null;
        this.isAuthenticated = false;
        return navigateTo("/login");
      } catch (error) {
        console.error("Logout error:", error);
        throw error;
      }
    },

    async checkAuth() {
      try {
        const { $supabase } = useNuxtApp();
        const {
          data: { user },
        } = await $supabase.auth.getUser();
        this.user = user;
        this.isAuthenticated = !!user;
      } catch (error) {
        console.error("Check auth error:", error);
        this.user = null;
        this.isAuthenticated = false;
      }
    },
  },

  getters: {
    getUserProfile: (state) => state.user,
    isLoggedIn: (state) => state.isAuthenticated,
  },
});

// Zustand auth store with localStorage persistence
import { create } from 'zustand'
import { persist } from 'zustand/middleware'

const useAuthStore = create(
  persist(
    (set, get) => ({
      // State
      user: null,
      token: null,
      isAuthenticated: false,
      isHydrated: false,

      // Actions
      setAuth: (user, token) => {
        // Also store token separately for API interceptor
        localStorage.setItem('access_token', token)
        set({ user, token, isAuthenticated: true })
      },

      logout: () => {
        localStorage.removeItem('access_token')
        set({ user: null, token: null, isAuthenticated: false })
      },

      updateUser: (userData) => {
        set((state) => ({
          user: state.user ? { ...state.user, ...userData } : userData,
        }))
      },

      // Called after hydration from localStorage
      setHydrated: () => set({ isHydrated: true }),
    }),
    {
      name: 'auth-storage',
      // Only persist these fields
      partialize: (state) => ({
        user: state.user,
        token: state.token,
        isAuthenticated: state.isAuthenticated,
      }),
      onRehydrateStorage: () => (state) => {
        // Sync token to access_token key for API interceptor
        if (state?.token) {
          localStorage.setItem('access_token', state.token)
        }
        state?.setHydrated()
      },
    }
  )
)

export default useAuthStore

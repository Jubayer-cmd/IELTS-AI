// React Query hooks for authentication
import { useMutation, useQuery, useQueryClient } from '@tanstack/react-query'
import { authAPI } from '../services/api'
import useAuthStore from '../store/authStore'

// Query keys for cache management
export const authKeys = {
  profile: ['auth', 'profile'],
}

/**
 * Hook for user login
 * Returns mutation for logging in with email/password
 */
export function useLogin() {
  const setAuth = useAuthStore((state) => state.setAuth)
  const queryClient = useQueryClient()

  return useMutation({
    mutationFn: async ({ email, password }) => {
      const response = await authAPI.login(email, password)
      return response
    },
    onSuccess: async (data) => {
      // Fetch user profile after successful login
      const profile = await authAPI.getProfile()
      setAuth(profile, data.access_token)
      // Invalidate any cached queries
      queryClient.invalidateQueries({ queryKey: authKeys.profile })
    },
  })
}

/**
 * Hook for user registration
 * Returns mutation for creating a new account
 */
export function useRegister() {
  const setAuth = useAuthStore((state) => state.setAuth)
  const queryClient = useQueryClient()

  return useMutation({
    mutationFn: async ({ name, email, password }) => {
      // Register the user
      await authAPI.register({ name, email, password })
      // Then log them in
      const loginResponse = await authAPI.login(email, password)
      return loginResponse
    },
    onSuccess: async (data) => {
      // Fetch user profile after successful registration + login
      const profile = await authAPI.getProfile()
      setAuth(profile, data.access_token)
      queryClient.invalidateQueries({ queryKey: authKeys.profile })
    },
  })
}

/**
 * Hook for fetching current user profile
 * Only runs when user is authenticated
 */
export function useProfile() {
  const { isAuthenticated, token } = useAuthStore()

  return useQuery({
    queryKey: authKeys.profile,
    queryFn: authAPI.getProfile,
    enabled: isAuthenticated && !!token,
    staleTime: 5 * 60 * 1000, // Consider fresh for 5 minutes
    retry: false, // Don't retry on 401
  })
}

/**
 * Hook for logout
 * Clears auth state and cache
 */
export function useLogout() {
  const logout = useAuthStore((state) => state.logout)
  const queryClient = useQueryClient()

  return () => {
    authAPI.logout()
    logout()
    queryClient.clear() // Clear all cached queries
  }
}

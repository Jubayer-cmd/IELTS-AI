// Authentication context and hooks (minimal client-only for UI flow)

import { createContext, useContext, useReducer, useEffect } from 'react'

const AuthContext = createContext()

const initialState = {
  user: null,
  token: null,
  isAuthenticated: false,
  loading: true,
}

const authReducer = (state, action) => {
  switch (action.type) {
    case 'INIT':
      return { ...state, ...action.payload, loading: false }
    case 'LOGIN_SUCCESS':
      return { ...state, user: action.payload.user, token: action.payload.token, isAuthenticated: true }
    case 'LOGOUT':
      return { ...state, user: null, token: null, isAuthenticated: false }
    case 'UPDATE_USER':
      return { ...state, user: { ...state.user, ...action.payload } }
    default:
      return state
  }
}

export function AuthProvider({ children }) {
  const [state, dispatch] = useReducer(authReducer, initialState)

  useEffect(() => {
    const saved = localStorage.getItem('auth')
    if (saved) {
      try {
        const parsed = JSON.parse(saved)
        dispatch({ type: 'INIT', payload: { ...parsed, loading: false } })
      } catch {
        dispatch({ type: 'INIT', payload: { ...initialState, loading: false } })
      }
    } else {
      dispatch({ type: 'INIT', payload: { ...initialState, loading: false } })
    }
  }, [])

  useEffect(() => {
    if (!state.loading) {
      localStorage.setItem('auth', JSON.stringify({ user: state.user, token: state.token, isAuthenticated: state.isAuthenticated }))
    }
  }, [state.user, state.token, state.isAuthenticated, state.loading])

  const value = {
    ...state,
    login: async ({ email }) => {
      // For MVP, simulate success
      const user = { id: 'local', email, name: email?.split('@')[0] || 'User' }
      dispatch({ type: 'LOGIN_SUCCESS', payload: { user, token: 'demo-token' } })
      return user
    },
    logout: () => {
      dispatch({ type: 'LOGOUT' })
    },
    register: async ({ email }) => {
      // Simulate registration then login
      const user = { id: 'local', email, name: email?.split('@')[0] || 'User' }
      dispatch({ type: 'LOGIN_SUCCESS', payload: { user, token: 'demo-token' } })
      return user
    },
  }

  return <AuthContext.Provider value={value}>{children}</AuthContext.Provider>
}

export function useAuth() {
  const context = useContext(AuthContext)
  if (!context) {
    throw new Error('useAuth must be used within an AuthProvider')
  }
  return context
}

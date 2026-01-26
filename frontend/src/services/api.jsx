// API client for backend communication
// Following FastAPI full-stack template pattern

import axios from 'axios'

const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000'

// Create axios instance with base config
const apiClient = axios.create({
  baseURL: `${API_BASE_URL}/api/v1`,
  headers: {
    'Content-Type': 'application/json',
  },
})

// Request interceptor - adds auth token to requests
apiClient.interceptors.request.use(
  (config) => {
    const token = localStorage.getItem('access_token')
    if (token) {
      config.headers.Authorization = `Bearer ${token}`
    }
    return config
  },
  (error) => Promise.reject(error)
)

// Response interceptor - handles auth errors
apiClient.interceptors.response.use(
  (response) => response,
  (error) => {
    if (error.response?.status === 401) {
      // Token expired or invalid - clear auth storage
      // Zustand's persist middleware uses 'auth-storage' key
      localStorage.removeItem('access_token')
      localStorage.removeItem('auth-storage')
      // The app will naturally show unauthenticated UI on next render
    }
    return Promise.reject(error)
  }
)

// Helper to get/set auth token
export const setAuthToken = (token) => {
  localStorage.setItem('access_token', token)
}

export const clearAuthToken = () => {
  localStorage.removeItem('access_token')
}

export const getAuthToken = () => {
  return localStorage.getItem('access_token')
}

// Auth API
export const authAPI = {
  register: async (userData) => {
    const response = await apiClient.post('/auth/register', userData)
    return response.data
  },

  login: async (email, password) => {
    // OAuth2 form data format
    const formData = new URLSearchParams()
    formData.append('username', email)
    formData.append('password', password)

    const response = await apiClient.post('/auth/login', formData, {
      headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
    })

    // Store token
    if (response.data.access_token) {
      setAuthToken(response.data.access_token)
    }

    return response.data
  },

  logout: () => {
    clearAuthToken()
  },

  getProfile: async () => {
    const response = await apiClient.get('/auth/me')
    return response.data
  },
}

// Chat API - Thread and message management
export const chatAPI = {
  /**
   * Create a new chat thread
   * @param {string} title - Optional thread title
   * @returns {Promise<{id: number, title: string|null, created_at: string, updated_at: string}>}
   */
  createThread: async (title = null) => {
    const response = await apiClient.post('/chat/threads', { title })
    return response.data
  },

  /**
   * Get all threads for the current user
   * @returns {Promise<Array<{id: number, title: string|null, created_at: string, updated_at: string}>>}
   */
  getThreads: async () => {
    const response = await apiClient.get('/chat/threads')
    return response.data
  },

  /**
   * Get all messages in a thread
   * @param {number} threadId
   * @returns {Promise<Array<{id: number, thread_id: number, role: string, message_type: string, content: string, evaluation: string|null, created_at: string}>>}
   */
  getThreadMessages: async (threadId) => {
    const response = await apiClient.get(`/chat/threads/${threadId}/messages`)
    return response.data
  },

  /**
   * Delete a thread and all its messages
   * @param {number} threadId
   * @returns {Promise<{message: string}>}
   */
  deleteThread: async (threadId) => {
    const response = await apiClient.delete(`/chat/threads/${threadId}`)
    return response.data
  },

  /**
   * Send a message to a thread
   * @param {number} threadId
   * @param {string} content - The message content
   * @returns {Promise<{id: number, thread_id: number, role: string, message_type: string, content: string, evaluation: string|null, created_at: string}>}
   */
  sendMessage: async (threadId, content) => {
    const response = await apiClient.post(`/chat/threads/${threadId}/messages`, {
      content: content,
    })
    return response.data
  },
}

export const paymentAPI = {
  initiatePayment: (paymentData) => {
    // TODO: Implement payment initiation API call
  },
  getPaymentHistory: () => {
    // TODO: Implement get payment history API call
  },
}

export const adminAPI = {
  getUsers: () => {
    // TODO: Implement get all users API call
  },
  getPayments: () => {
    // TODO: Implement get all payments API call
  },
  getStats: () => {
    // TODO: Implement get system stats API call
  },
}

export default apiClient

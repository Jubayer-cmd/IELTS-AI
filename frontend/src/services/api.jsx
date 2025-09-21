// API client for backend communication
// TODO: Implement axios client with interceptors

import axios from 'axios'

const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000'

const apiClient = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
})

// TODO: Add request interceptor for auth tokens
// TODO: Add response interceptor for error handling

export const authAPI = {
  register: (userData) => {
    // TODO: Implement user registration API call
  },
  login: (credentials) => {
    // TODO: Implement user login API call
  },
  getProfile: () => {
    // TODO: Implement get user profile API call
  },
}

export const evaluationAPI = {
  generateQuestion: (taskType) => {
    // TODO: Implement question generation API call
  },
  evaluateEssay: (essayData) => {
    // TODO: Implement essay evaluation API call
  },
  getEvaluations: () => {
    // TODO: Implement get evaluations API call
  },
  getEvaluationDetails: (id) => {
    // TODO: Implement get evaluation details API call
  },
}

export const chatAPI = {
  sendMessage: async (message, sessionId = null, onMessage = null) => {
    try {
      const url = `${API_BASE_URL}/chat/message`
      const response = await fetch(url, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          message: message,
        }),
      })
      
      if (!response.ok) {
        throw new Error(`Failed to send message: ${response.status}`)
      }

      const data = await response.json()
      
      // Simulate the old streaming format for compatibility
      if (onMessage) {
        onMessage({ type: 'message', content: data.message })
      }
      
    } catch (error) {
      throw error
    }
  },

  generateQuestion: async (taskType = 'Task 2', onMessage = null) => {
    try {
      const message = `Generate an IELTS Writing ${taskType} question for me to practice.`
      
      const response = await fetch(`${API_BASE_URL}/chat/message`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ message }),
      })

      if (!response.ok) {
        throw new Error('Failed to generate question')
      }

      const data = await response.json()
      
      // Simulate the old streaming format for compatibility
      if (onMessage) {
        onMessage({ type: 'message', content: data.message })
      }
      
    } catch (error) {
      throw error
    }
  },

  evaluateEssay: async (essayText, taskType = 'Task 2', onMessage = null) => {
    try {
      const message = `Please evaluate this IELTS Writing ${taskType} essay and provide detailed feedback:\n\n${essayText}`
      
      const response = await fetch(`${API_BASE_URL}/chat/message`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ message }),
      })

      if (!response.ok) {
        throw new Error('Failed to evaluate essay')
      }

      const data = await response.json()
      
      // Simulate the old streaming format for compatibility
      if (onMessage) {
        onMessage({ type: 'message', content: data.message })
      }
      
    } catch (error) {
      throw error
    }
  },

  getSessionHistory: async (sessionId) => {
    try {
      const response = await apiClient.get(`/chat/sessions/${sessionId}/history`)
      return response.data
    } catch (error) {
      throw error
    }
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

// API client for backend communication
// TODO: Implement axios client with interceptors

import axios from 'axios'

// Simple user ID generation for memory persistence
const getUserId = () => {
  let userId = localStorage.getItem('ielts_user_id')
  if (!userId) {
    userId = 'user_' + Date.now() + '_' + Math.random().toString(36).substr(2, 9)
    localStorage.setItem('ielts_user_id', userId)
  }
  return userId
}

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

// Note: Evaluation functionality has been moved to chatAPI
// All IELTS evaluations and question generation are now handled through the chat interface

export const chatAPI = {
  // Thread management
  createThread: async (title = 'New Chat') => {
    try {
      const response = await apiClient.post('/chat/threads', { title })
      return response.data
    } catch (error) {
      throw error
    }
  },

  getThreads: async () => {
    try {
      const response = await apiClient.get('/chat/threads')
      return response.data
    } catch (error) {
      throw error
    }
  },

  getThreadMessages: async (threadId) => {
    try {
      const response = await apiClient.get(`/chat/threads/${threadId}/messages`)
      return response.data
    } catch (error) {
      throw error
    }
  },

  deleteThread: async (threadId) => {
    try {
      const response = await apiClient.delete(`/chat/threads/${threadId}`)
      return response.data
    } catch (error) {
      throw error
    }
  },

  sendMessageToThread: async (threadId, message, imageData = null, conversationState = 'greeting') => {
    try {
      const response = await apiClient.post(`/chat/threads/${threadId}/messages`, {
        message: message,
        image_data: imageData,
        conversation_state: conversationState,
        user_id: getUserId(),
      })

      return {
        message: response.data.message,
        shouldDeductCredit: response.data.should_deduct_credit,
        conversationState: response.data.conversation_state,
        userIntent: response.data.user_intent,
        evaluationData: response.data.evaluation_data,
      }
    } catch (error) {
      throw error
    }
  },

  // Legacy endpoint (kept for backward compatibility)
  sendMessage: async (message, imageData = null, conversationState = 'greeting', onMessage = null) => {
    try {
      const url = `${API_BASE_URL}/chat/message`
      const response = await fetch(url, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          message: message,
          image_data: imageData,
          conversation_state: conversationState,
          user_id: getUserId(),
        }),
      })

      if (!response.ok) {
        throw new Error(`Failed to send message: ${response.status}`)
      }

      const data = await response.json()

      // Return the full response with all new fields
      const result = {
        message: data.message,
        shouldDeductCredit: data.should_deduct_credit,
        conversationState: data.conversation_state,
        userIntent: data.user_intent,
        evaluationData: data.evaluation_data,
      }

      // Also call onMessage callback for compatibility
      if (onMessage) {
        onMessage({ type: 'message', content: data.message, data: result })
      }

      return result

    } catch (error) {
      throw error
    }
  },

  generateQuestion: async (taskType = 'Task 2', onMessage = null) => {
    try {
      const message = `Generate an IELTS Writing ${taskType} question for me to practice.`
      return await chatAPI.sendMessage(message, null, 'waiting_for_preference', onMessage)
    } catch (error) {
      throw error
    }
  },

  evaluateEssay: async (essayText, taskType = 'Task 2', imageData = null, onMessage = null) => {
    try {
      const message = `Please evaluate this IELTS Writing ${taskType} essay and provide detailed feedback:\n\n${essayText}`
      return await chatAPI.sendMessage(message, imageData, 'waiting_for_essay', onMessage)
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

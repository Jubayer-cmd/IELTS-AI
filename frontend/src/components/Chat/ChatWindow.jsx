import React, { useState, useCallback, useRef, useEffect } from 'react'
import MessageList from '@/components/Chat/MessageList'
import ChatInput from '@/components/Chat/ChatInput'
import { chatAPI } from '@/services/api'

export default function ChatWindow({ currentThreadId }) {
  const [messages, setMessages] = useState([])
  const [isLoading, setIsLoading] = useState(false)
  const messagesEndRef = useRef(null)

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' })
  }

  useEffect(() => {
    scrollToBottom()
  }, [messages])

  // Load messages when thread changes
  useEffect(() => {
    if (currentThreadId) {
      loadThreadMessages(currentThreadId)
    } else {
      setMessages([])
      setIsLoading(false)
    }
  }, [currentThreadId])

  const loadThreadMessages = async (threadId) => {
    try {
      setIsLoading(true)
      const threadMessages = await chatAPI.getThreadMessages(threadId)

      // Convert backend messages to frontend format
      const formattedMessages = threadMessages.map(msg => ({
        id: msg.id,
        role: msg.role === 'user' ? 'user' : 'ai',
        content: msg.content,
        type: msg.message_type || 'text',
        evaluation: msg.evaluation ? JSON.parse(msg.evaluation) : null,
        timestamp: new Date(msg.created_at)
      }))

      setMessages(formattedMessages)
    } catch (error) {
      console.error('Failed to load thread messages:', error)
    } finally {
      setIsLoading(false)
    }
  }

  const handleSendMessage = useCallback(async (message) => {
    if (!message.trim() || isLoading || !currentThreadId) {
      return
    }

    setIsLoading(true)

    // Optimistically add user message to UI
    const tempUserMsg = {
      id: `temp-${Date.now()}`,
      role: 'user',
      content: message,
      type: 'text',
      timestamp: new Date()
    }
    setMessages(prev => [...prev, tempUserMsg])

    try {
      // Send message to backend
      const response = await chatAPI.sendMessage(currentThreadId, message)

      // Replace temp message with actual response
      setMessages(prev => {
        const updated = prev.filter(m => m.id !== tempUserMsg.id)
        return [...updated, {
          id: response.id,
          role: 'user',
          content: response.content,
          type: response.message_type || 'text',
          timestamp: new Date(response.created_at)
        }]
      })

      // TODO: When LangGraph is integrated, the backend will return
      // an AI response which should be added here

    } catch (error) {
      console.error('Failed to send message:', error)
      // Remove the optimistic message and show error
      setMessages(prev => {
        const updated = prev.filter(m => m.id !== tempUserMsg.id)
        return [...updated, {
          id: `error-${Date.now()}`,
          role: 'ai',
          content: 'Sorry, I encountered an error. Please try again.',
          type: 'error',
          timestamp: new Date()
        }]
      })
    } finally {
      setIsLoading(false)
    }
  }, [currentThreadId, isLoading])

  return (
    <div className='h-full flex flex-col bg-transparent'>
      {/* Messages Area - scrollable */}
      <div className='flex-1 overflow-y-auto'>
        <MessageList messages={messages} isLoading={isLoading} />
        <div ref={messagesEndRef} />
      </div>

      {/* Input Area - fixed at bottom */}
      <div className='flex-shrink-0'>
        <ChatInput onSend={handleSendMessage} disabled={isLoading || !currentThreadId} />
      </div>
    </div>
  )
}

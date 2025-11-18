import React, { useState, useCallback, useRef, useEffect } from 'react'
import { Card, CardContent } from '@/components/ui/card'
import { Separator } from '@/components/ui/separator'
import { Button } from '@/components/ui/button'
import MessageList from '@/components/Chat/MessageList'
import ChatInput from '@/components/Chat/ChatInput'
import { chatAPI } from '@/services/api'

export default function ChatWindow({ currentThreadId }) {
  const [messages, setMessages] = useState([])
  const [conversationState, setConversationState] = useState('greeting')
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
        type: 'message',
        timestamp: new Date(msg.created_at)
      }))

      setMessages(formattedMessages)
    } catch (error) {
      console.error('Failed to load thread messages:', error)
    } finally {
      setIsLoading(false)
    }
  }

  const addMessage = useCallback((role, content, type = 'message') => {
    setMessages(prev => [...prev, {
      id: Date.now() + Math.random(),
      role,
      content,
      type,
      timestamp: new Date()
    }])
  }, [])

  const updateLastMessage = useCallback((content) => {
    setMessages(prev => {
      const updated = [...prev]
      if (updated.length > 0 && updated[updated.length - 1].role === 'ai') {
        updated[updated.length - 1].content += content
      }
      return updated
    })
  }, [])

  const handleSendMessage = useCallback(async (message) => {
    if (!message.trim() || isLoading || !currentThreadId) {
      return
    }

    setIsLoading(true)

    // Add user message
    addMessage('user', message)

    // Add placeholder AI message
    addMessage('ai', '')

    try {
      const response = await chatAPI.sendMessageToThread(
        currentThreadId,
        message,
        null,
        conversationState
      )

      // Handle the full response
      if (response) {
        // Update conversation state
        setConversationState(response.conversationState)

        // Update the AI message with the response
        setMessages(prev => {
          const updated = [...prev]
          if (updated.length > 0 && updated[updated.length - 1].role === 'ai') {
            updated[updated.length - 1].content = response.message
            // Add evaluation data if present
            if (response.evaluationData) {
              updated[updated.length - 1].evaluationData = response.evaluationData
            }
          }
          return updated
        })
      }
    } catch (error) {
      setMessages(prev => {
        const updated = [...prev]
        if (updated.length > 0 && updated[updated.length - 1].role === 'ai') {
          updated[updated.length - 1].content = 'Sorry, I encountered an error. Please try again.'
          updated[updated.length - 1].type = 'error'
        }
        return updated
      })
    } finally {
      setIsLoading(false)
    }
  }, [currentThreadId, conversationState, isLoading, addMessage])

  const handleGenerateQuestion = useCallback(async (taskType = 'Task 2') => {
    if (isLoading || !currentThreadId) return

    setIsLoading(true)

    const questionMessage = `Generate an IELTS Writing ${taskType} question for me to practice.`

    // Add user request
    addMessage('user', `Generate a ${taskType} question`)

    // Add placeholder AI message
    addMessage('ai', '')

    try {
      const response = await chatAPI.sendMessageToThread(
        currentThreadId,
        questionMessage,
        null,
        'waiting_for_preference'
      )

      // Handle the full response
      if (response) {
        // Update conversation state
        setConversationState(response.conversationState)

        // Update the AI message with the response
        setMessages(prev => {
          const updated = [...prev]
          if (updated.length > 0 && updated[updated.length - 1].role === 'ai') {
            updated[updated.length - 1].content = response.message
          }
          return updated
        })
      }
    } catch (error) {
      setMessages(prev => {
        const updated = [...prev]
        if (updated.length > 0 && updated[updated.length - 1].role === 'ai') {
          updated[updated.length - 1].content = 'Sorry, I couldn\'t generate a question. Please try again.'
          updated[updated.length - 1].type = 'error'
        }
        return updated
      })
    } finally {
      setIsLoading(false)
    }
  }, [currentThreadId, isLoading, addMessage])

  return (
    <div className='h-full flex flex-col bg-transparent'>
      {/* Header */}
      <div className='p-3 md:p-4 border-b border-border bg-card flex-shrink-0'>
        <h2 className='font-semibold text-foreground text-base md:text-lg'>IELTS Writing Assistant</h2>
      </div>


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

import React, { useState, useCallback, useRef, useEffect } from 'react'
import { Card, CardContent } from '@/components/ui/card'
import { Separator } from '@/components/ui/separator'
import { Button } from '@/components/ui/button'
import MessageList from '@/components/Chat/MessageList'
import ChatInput from '@/components/Chat/ChatInput'
import { chatAPI } from '@/services/api'

export default function ChatWindow() {
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
    if (!message.trim() || isLoading) {
      return
    }

    setIsLoading(true)
    
    // Add user message
    addMessage('user', message)
    
    // Add placeholder AI message
    addMessage('ai', '')

    try {
      const response = await chatAPI.sendMessage(message, null, conversationState)

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
  }, [conversationState, isLoading, addMessage])

  const handleGenerateQuestion = useCallback(async (taskType = 'Task 2') => {
    if (isLoading) return

    setIsLoading(true)
    
    // Add user request
    addMessage('user', `Generate a ${taskType} question`)
    
    // Add placeholder AI message
    addMessage('ai', '')

    try {
      const response = await chatAPI.generateQuestion(taskType)

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
  }, [isLoading, addMessage])

  return (
    <div className='h-full flex flex-col bg-transparent'>
      {/* Header with Task Buttons - only show if we have messages */}
      {messages.length > 0 && (
        <div className='p-3 md:p-4 border-b border-border flex flex-col md:flex-row gap-3 md:gap-0 md:justify-between items-start md:items-center bg-card flex-shrink-0'>
          <h2 className='font-semibold text-foreground text-base md:text-lg'>IELTS Writing Assistant</h2>
          <div className='flex gap-2 w-full md:w-auto'>
            <Button
              variant='outline'
              size='sm'
              onClick={() => handleGenerateQuestion('Task 1')}
              disabled={isLoading}
              className='flex-1 md:flex-initial text-xs md:text-sm'
            >
              Task 1 Question
            </Button>
            <Button
              variant='outline'
              size='sm'
              onClick={() => handleGenerateQuestion('Task 2')}
              disabled={isLoading}
              className='flex-1 md:flex-initial text-xs md:text-sm'
            >
              Task 2 Question
            </Button>
          </div>
        </div>
      )}

      {/* Messages Area - scrollable */}
      <div className='flex-1 overflow-y-auto'>
        <MessageList messages={messages} isLoading={isLoading} />
        <div ref={messagesEndRef} />
      </div>

      {/* Input Area - fixed at bottom */}
      <div className='flex-shrink-0'>
        <ChatInput onSend={handleSendMessage} disabled={isLoading} />
      </div>
    </div>
  )
}



import React, { useState, useCallback, useRef, useEffect } from 'react'
import { Card, CardContent } from '@/components/ui/card'
import { Separator } from '@/components/ui/separator'
import { Button } from '@/components/ui/button'
import MessageList from '@/components/Chat/MessageList'
import ChatInput from '@/components/Chat/ChatInput'
import { chatAPI } from '@/services/api'

export default function ChatWindow() {
  const [messages, setMessages] = useState([])
  const [sessionId, setSessionId] = useState(null)
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
      await chatAPI.sendMessage(message, sessionId, (data) => {
        if (data.type === 'message' && data.content) {
          // Replace the empty AI message with the full response
          setMessages(prev => {
            const updated = [...prev]
            if (updated.length > 0 && updated[updated.length - 1].role === 'ai') {
              updated[updated.length - 1].content = data.content
            }
            return updated
          })
        } else if (data.type === 'error') {
          setMessages(prev => {
            const updated = [...prev]
            if (updated.length > 0 && updated[updated.length - 1].role === 'ai') {
              updated[updated.length - 1].content = `Error: ${data.content}`
              updated[updated.length - 1].type = 'error'
            }
            return updated
          })
        }
      })
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
  }, [sessionId, isLoading, addMessage, updateLastMessage])

  const handleGenerateQuestion = useCallback(async (taskType = 'Task 2') => {
    if (isLoading) return

    setIsLoading(true)
    
    // Add user request
    addMessage('user', `Generate a ${taskType} question`)
    
    // Add placeholder AI message
    addMessage('ai', '')

    try {
      await chatAPI.generateQuestion(taskType, (data) => {
        if (data.type === 'message' && data.content) {
          // Replace the empty AI message with the full response
          setMessages(prev => {
            const updated = [...prev]
            if (updated.length > 0 && updated[updated.length - 1].role === 'ai') {
              updated[updated.length - 1].content = data.content
            }
            return updated
          })
        } else if (data.type === 'error') {
          setMessages(prev => {
            const updated = [...prev]
            if (updated.length > 0 && updated[updated.length - 1].role === 'ai') {
              updated[updated.length - 1].content = `Error: ${data.content}`
              updated[updated.length - 1].type = 'error'
            }
            return updated
          })
        }
      })
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
  }, [isLoading, addMessage, updateLastMessage])

  return (
    <div className='h-screen flex flex-col bg-transparent'>
      {/* Header with Task Buttons - only show if we have messages */}
      {messages.length > 0 && (
        <div className='p-4 border-b border-gray-700 flex justify-between items-center bg-[#1a1a1a] flex-shrink-0'>
          <h2 className='font-semibold text-white'>IELTS Writing Assistant</h2>
          <div className='flex gap-2'>
            <Button
              variant='outline'
              size='sm'
              onClick={() => handleGenerateQuestion('Task 1')}
              disabled={isLoading}
              className='border-gray-600 text-gray-300 hover:bg-gray-700'
            >
              Task 1 Question
            </Button>
            <Button
              variant='outline'
              size='sm'
              onClick={() => handleGenerateQuestion('Task 2')}
              disabled={isLoading}
              className='border-gray-600 text-gray-300 hover:bg-gray-700'
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



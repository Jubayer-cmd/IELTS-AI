import React, { useState, useCallback, useRef, useEffect } from 'react'
import MessageList from '@/components/Chat/MessageList'
import ChatInput from '@/components/Chat/ChatInput'
import { chatAPI } from '@/services/api'

export default function ChatWindow({ currentThreadId, onUpdateThreadTitle }) {
  const [messages, setMessages] = useState([])
  const [isLoading, setIsLoading] = useState(false)
  const [isStreaming, setIsStreaming] = useState(false)
  const messagesEndRef = useRef(null)
  const abortStreamRef = useRef(null)
  const streamingMessageIdRef = useRef(null)

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' })
  }

  useEffect(() => {
    scrollToBottom()
  }, [messages])

  // Load messages when thread changes
  useEffect(() => {
    // Abort any ongoing stream when thread changes
    if (abortStreamRef.current) {
      abortStreamRef.current()
      abortStreamRef.current = null
    }
    setIsStreaming(false)
    streamingMessageIdRef.current = null

    if (currentThreadId) {
      loadThreadMessages(currentThreadId)
    } else {
      setMessages([])
      setIsLoading(false)
    }
  }, [currentThreadId])

  // Cleanup on unmount
  useEffect(() => {
    return () => {
      if (abortStreamRef.current) {
        abortStreamRef.current()
      }
    }
  }, [])

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
    if (!message.trim() || isLoading || isStreaming || !currentThreadId) {
      return
    }

    setIsLoading(true)

    // Optimistically add user message to UI
    const tempUserMsgId = `temp-user-${Date.now()}`
    const tempUserMsg = {
      id: tempUserMsgId,
      role: 'user',
      content: message,
      type: 'text',
      timestamp: new Date()
    }

    // Create placeholder for AI streaming response
    const streamingMsgId = `streaming-${Date.now()}`
    streamingMessageIdRef.current = streamingMsgId
    const streamingMsg = {
      id: streamingMsgId,
      role: 'ai',
      content: '',
      type: 'text',
      isStreaming: true,
      timestamp: null
    }

    setMessages(prev => [...prev, tempUserMsg, streamingMsg])
    setIsLoading(false)
    setIsStreaming(true)

    // Start streaming
    const abort = chatAPI.streamMessage(currentThreadId, message, {
      onChunk: (token) => {
        // Append token to streaming message
        setMessages(prev =>
          prev.map(msg =>
            msg.id === streamingMsgId
              ? { ...msg, content: msg.content + token }
              : msg
          )
        )
      },
      onComplete: (metadata) => {
        // Update message with server ID and timestamp
        setMessages(prev =>
          prev.map(msg =>
            msg.id === streamingMsgId
              ? {
                  ...msg,
                  id: metadata.id,
                  isStreaming: false,
                  timestamp: new Date(metadata.created_at)
                }
              : msg
          )
        )

        // Update thread title if auto-generated (first message)
        if (metadata.title && onUpdateThreadTitle) {
          onUpdateThreadTitle(currentThreadId, metadata.title)
        }

        setIsStreaming(false)
        streamingMessageIdRef.current = null
        abortStreamRef.current = null
      },
      onError: (error) => {
        console.error('Streaming error:', error)
        // Update streaming message to show error
        setMessages(prev =>
          prev.map(msg =>
            msg.id === streamingMsgId
              ? {
                  ...msg,
                  content: msg.content || 'Sorry, I encountered an error. Please try again.',
                  type: 'error',
                  isStreaming: false,
                  timestamp: new Date()
                }
              : msg
          )
        )
        setIsStreaming(false)
        streamingMessageIdRef.current = null
        abortStreamRef.current = null
      }
    })

    abortStreamRef.current = abort
  }, [currentThreadId, isLoading, isStreaming, onUpdateThreadTitle])

  return (
    <div className='h-full flex flex-col bg-transparent'>
      {/* Messages Area - scrollable */}
      <div className='flex-1 overflow-y-auto'>
        <MessageList messages={messages} isLoading={isLoading} />
        <div ref={messagesEndRef} />
      </div>

      {/* Input Area - fixed at bottom */}
      <div className='flex-shrink-0'>
        <ChatInput onSend={handleSendMessage} disabled={isLoading || isStreaming || !currentThreadId} />
      </div>
    </div>
  )
}

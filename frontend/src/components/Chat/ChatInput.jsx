import React, { useState, useRef, useEffect } from 'react'
import { Button } from '@/components/ui/button'
import { Send, Paperclip } from 'lucide-react'

export default function ChatInput({ onSend, disabled = false }) {
  const [message, setMessage] = useState('')
  const textareaRef = useRef(null)


  const handleSubmit = (e) => {
    if (e) e.preventDefault()
    
    if (!message.trim() || disabled) {
      return
    }
    
    onSend?.(message)
    setMessage('')
    
    // Reset textarea height
    if (textareaRef.current) {
      textareaRef.current.style.height = 'auto'
    }
  }

  const handleKeyDown = (e) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault()
      handleSubmit(e)
    }
  }

  const handleTextareaChange = (e) => {
    setMessage(e.target.value)
  }

  // Auto-resize textarea
  useEffect(() => {
    if (textareaRef.current) {
      textareaRef.current.style.height = 'auto'
      textareaRef.current.style.height = Math.min(textareaRef.current.scrollHeight, 200) + 'px'
    }
  }, [message])

  return (
    <div className='px-6 pt-6 bg-[#1a1a1a]'>
      <div className='max-w-4xl mx-auto'>
        <div className='relative bg-[#2f2f2f] border border-[#4a4a4a] rounded-t-xl overflow-hidden shadow-2xl'>
          {/* Textarea */}
          <div className='p-4'>
            <textarea
              ref={textareaRef}
              value={message}
              onChange={handleTextareaChange}
              onKeyDown={handleKeyDown}
              placeholder='Type your message here...'
              className='w-full bg-transparent text-white placeholder-gray-400 resize-none border-none outline-none text-base min-h-[24px] max-h-[200px]'
              rows={2}
              disabled={disabled}
            />
          </div>
          
          {/* Bottom Controls */}
          <div className='flex items-center justify-between px-4 pb-3'>
            <div className='flex items-center gap-3'>
              <button className='p-2 hover:bg-gray-600/50 rounded-lg transition-colors'>
                <Paperclip className='h-4 w-4 text-gray-400' />
              </button>
            </div>
            <Button
              onClick={handleSubmit}
              disabled={!message.trim() || disabled}
              className='h-8 w-8 bg-white hover:bg-gray-200 text-black rounded-full p-0 flex items-center justify-center disabled:opacity-30 disabled:cursor-not-allowed'
            >
              {disabled ? (
                <div className='h-4 w-4 border-2 border-gray-400 border-t-transparent rounded-full animate-spin' />
              ) : (
                <Send className='h-4 w-4' />
              )}
            </Button>
          </div>
        </div>
      </div>
    </div>
  )
}



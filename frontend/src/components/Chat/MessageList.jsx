import React from 'react'
import { Loader2, AlertCircle } from 'lucide-react'

export default function MessageList({ messages = [], isLoading = false }) {
  if (messages.length === 0) {
    return (
      <div className='p-4 h-full'>
        <div className='flex flex-col items-center justify-center h-full text-gray-400 space-y-6'>
          <div className='text-center max-w-2xl mx-auto'>
            <p className='text-lg mb-4'>
              I can help you practice IELTS writing by generating questions, evaluating your essays, 
              and providing detailed feedback.
            </p>
            <p className='text-sm text-gray-500'>
              Try asking me to generate a question or paste your essay for evaluation.
            </p>
          </div>
          <div className='flex flex-wrap gap-2 text-xs justify-center'>
            <span className='bg-gray-800 text-gray-300 px-3 py-2 rounded-lg border border-gray-700'>Generate questions</span>
            <span className='bg-gray-800 text-gray-300 px-3 py-2 rounded-lg border border-gray-700'>Evaluate essays</span>
            <span className='bg-gray-800 text-gray-300 px-3 py-2 rounded-lg border border-gray-700'>Get feedback</span>
          </div>
        </div>
      </div>
    )
  }

  return (
    <div className='bg-[#1a1a1a]'>
      <div className='p-4 space-y-6 max-w-4xl mx-auto'>
        {messages.map((message) => (
          <div key={message.id} className={`flex ${message.role === 'user' ? 'justify-end' : 'justify-start'}`}>
            <div className={`max-w-[70%] p-4 rounded-lg ${
              message.role === 'user' 
                ? 'bg-blue-600 text-white' 
                : message.type === 'error'
                  ? 'bg-red-900 text-red-200 border border-red-700'
                  : 'bg-[#2a2a2a] text-gray-200 border border-gray-700'
            }`}>
              <div className='text-sm whitespace-pre-wrap break-words'>
                {message.content || (
                  <div className='flex items-center gap-2 text-gray-400'>
                    <Loader2 className='h-4 w-4 animate-spin' />
                    <span>Thinking...</span>
                  </div>
                )}
              </div>
              
              {message.type === 'error' && (
                <div className='flex items-center gap-1 mt-2 text-red-300 text-xs'>
                  <AlertCircle className='h-3 w-3' />
                  <span>Error occurred</span>
                </div>
              )}
              
              {message.timestamp && (
                <div className='text-xs opacity-50 mt-2'>
                  {new Date(message.timestamp).toLocaleTimeString()}
                </div>
              )}
            </div>
          </div>
        ))}
      </div>
    </div>
  )
}



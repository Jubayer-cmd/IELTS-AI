import { Card, CardContent } from '@/components/ui/card'
import { ScrollArea } from '@/components/ui/scroll-area'
import { Separator } from '@/components/ui/separator'
import { Button } from '@/components/ui/button'
import { Input } from '@/components/ui/input'
import { Pin, Search, Plus, ChevronDown, Square, Settings, Sun, Menu } from 'lucide-react'
import { Avatar, AvatarFallback } from '@/components/ui/avatar'

export default function Sidebar({ items = [], collapsed = false, onToggle }) {
  const pinned = ['Telegram Mini Apps Overview']
  const older = items.length
    ? items
    : [
        'CINC Meeting Prep Add Call T…',
        'Meeting Summary and Issues',
        'Building TTS Difficulty',
        'Deleting MR in GitLab',
        'Flexible Call Direction Handlin…',
        'Need help with task, seniors n…',
        'Depends in API Calls',
        'POS Business Profitability in B…',
        'ERP Software Definition',
        'Islamic dream interpretation o…',
        'Outbound Cadence Entry Fiel…',
        'AI Agent for Inbound/Outbou…',
      ]
  if (collapsed) {
    return (
      <div className='h-full bg-[#1a1a1a] flex flex-col items-center'>
        {/* Collapse Toggle */}
        <div className='p-3'>
          <button onClick={onToggle} className='p-2 hover:bg-gray-700 rounded'>
            <Menu className='h-5 w-5 text-white' />
          </button>
        </div>

        {/* New Chat Button */}
        <div className='px-2 mb-4'>
          <Button className='w-10 h-10 bg-[#8B5A3C] hover:bg-[#7A4D33] text-white rounded-lg flex items-center justify-center p-0'>
            <Plus className='h-4 w-4' />
          </Button>
        </div>

        {/* Search Icon */}
        <div className='px-2 mb-4'>
          <button className='w-10 h-10 hover:bg-gray-700 rounded flex items-center justify-center'>
            <Search className='h-4 w-4 text-gray-400' />
          </button>
        </div>

        {/* Chat Icons */}
        <ScrollArea className='flex-1 px-2'>
          <div className='space-y-2'>
            {pinned.slice(0, 3).map((_, i) => (
              <div key={i} className='w-10 h-8 bg-[#2a2a2a] hover:bg-[#333333] rounded cursor-pointer' />
            ))}
          </div>
        </ScrollArea>

        {/* User Avatar */}
        <div className='p-3 border-t border-gray-700'>
          <Avatar className='h-8 w-8 bg-gray-600'>
            <AvatarFallback className='text-white text-sm'>J</AvatarFallback>
          </Avatar>
        </div>
      </div>
    )
  }

  return (
    <div className='h-full bg-[#1a1a1a] flex flex-col'>
      {/* Header */}
      <div className='flex items-center justify-between px-4 py-4'>
        <div className='flex items-center gap-2 text-white font-semibold text-lg'>
          <Square className='h-5 w-5' />
          T3.chat
        </div>
        <div className='flex items-center gap-2'>
          <button onClick={onToggle} className='p-1 hover:bg-gray-700 rounded'>
            <Menu className='h-4 w-4 text-gray-400' />
          </button>
          <button className='p-1 hover:bg-gray-700 rounded'>
            <Settings className='h-4 w-4 text-gray-400' />
          </button>
          <button className='p-1 hover:bg-gray-700 rounded'>
            <Sun className='h-4 w-4 text-gray-400' />
          </button>
        </div>
      </div>

      {/* New Chat Button */}
      <div className='px-3 mb-4'>
        <Button className='w-full bg-[#8B5A3C] hover:bg-[#7A4D33] text-white h-11 rounded-lg font-medium flex items-center justify-center gap-2'>
          <Plus className='h-4 w-4' />
          New Chat
        </Button>
      </div>

      {/* Search */}
      <div className='px-3 mb-4 relative'>
        <Input 
          placeholder='Search your threads...' 
          className='bg-[#2a2a2a] border-gray-600 text-white placeholder-gray-400 pl-9' 
        />
        <Search className='h-4 w-4 absolute left-6 top-1/2 -translate-y-1/2 text-gray-400 pointer-events-none' />
      </div>

      {/* Pinned Section */}
      <div className='px-3 mb-2'>
        <div className='flex items-center justify-between text-gray-400 text-sm font-medium px-2'>
          <span className='flex items-center gap-2'>
            <Pin className='h-3 w-3' />
            Pinned
          </span>
          <ChevronDown className='h-3 w-3' />
        </div>
      </div>

      {/* Chat List */}
      <ScrollArea className='flex-1 px-3'>
        <div className='space-y-1'>
          {pinned.map((label, i) => (
            <div key={i} className='px-3 py-2 rounded-lg hover:bg-[#2a2a2a] cursor-pointer text-white text-sm'>
              {label}
            </div>
          ))}
        </div>
        
        <div className='mt-6 mb-2'>
          <div className='text-gray-400 text-sm font-medium px-2'>Older</div>
        </div>
        
        <div className='space-y-1'>
          {older.map((label, i) => (
            <div key={i} className='px-3 py-2 rounded-lg hover:bg-[#2a2a2a] cursor-pointer text-white text-sm'>
              {label}
            </div>
          ))}
        </div>
      </ScrollArea>

      {/* User Profile */}
      <div className='px-3 py-4 border-t border-gray-700'>
        <div className='flex items-center gap-3'>
          <Avatar className='h-8 w-8 bg-gray-600'>
            <AvatarFallback className='text-white text-sm'>J</AvatarFallback>
          </Avatar>
          <div>
            <div className='text-white text-sm font-medium'>Jubayer</div>
            <div className='text-gray-400 text-xs'>Free</div>
          </div>
        </div>
      </div>
    </div>
  )
}



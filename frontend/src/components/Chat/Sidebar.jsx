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
      <div className='h-full bg-card border-r border-border flex flex-col items-center'>
        {/* Collapse Toggle */}
        <div className='p-3'>
          <button onClick={onToggle} className='p-2 hover:bg-accent rounded'>
            <Menu className='h-5 w-5 text-foreground' />
          </button>
        </div>

        {/* New Chat Button */}
        <div className='px-2 mb-4'>
          <Button className='w-10 h-10 bg-primary hover:bg-primary/90 text-primary-foreground rounded-lg flex items-center justify-center p-0'>
            <Plus className='h-4 w-4' />
          </Button>
        </div>

        {/* Search Icon */}
        <div className='px-2 mb-4'>
          <button className='w-10 h-10 hover:bg-accent rounded flex items-center justify-center'>
            <Search className='h-4 w-4 text-muted-foreground' />
          </button>
        </div>

        {/* Chat Icons */}
        <ScrollArea className='flex-1 px-2'>
          <div className='space-y-2'>
            {pinned.slice(0, 3).map((_, i) => (
              <div key={i} className='w-10 h-8 bg-background hover:bg-accent rounded cursor-pointer' />
            ))}
          </div>
        </ScrollArea>

        {/* User Avatar */}
        <div className='p-3 border-t border-border'>
          <Avatar className='h-8 w-8 bg-muted'>
            <AvatarFallback className='text-muted-foreground text-sm'>J</AvatarFallback>
          </Avatar>
        </div>
      </div>
    )
  }

  return (
    <div className='h-full bg-card border-r border-border flex flex-col'>
      {/* Header */}
      <div className='flex items-center justify-between px-4 py-4'>
        <div className='flex items-center gap-2 text-foreground font-semibold text-lg'>
        <button onClick={onToggle} className='p-1 hover:bg-accent rounded'>
            <Menu className='h-4 w-4 text-muted-foreground' />
          </button>
          IELTS-AI
        </div>
        <div className='flex items-center gap-2'>
          <button className='p-1 hover:bg-accent rounded'>
            <Settings className='h-4 w-4 text-muted-foreground' />
          </button>
          <button className='p-1 hover:bg-accent rounded'>
            <Sun className='h-4 w-4 text-muted-foreground' />
          </button>
        </div>
      </div>

      {/* New Chat Button */}
      <div className='px-3 mb-4'>
        <Button className='w-full bg-primary hover:bg-primary/90 text-primary-foreground h-11 rounded-lg font-medium flex items-center justify-center gap-2'>
          <Plus className='h-4 w-4' />
          New Chat
        </Button>
      </div>

      {/* Search */}
      <div className='px-3 mb-4 relative'>
        <Input
          placeholder='Search your threads...'
          className='bg-background border-border text-foreground placeholder-muted-foreground pl-9'
        />
        <Search className='h-4 w-4 absolute left-6 top-1/2 -translate-y-1/2 text-muted-foreground pointer-events-none' />
      </div>

      {/* Pinned Section */}
      <div className='px-3 mb-2'>
        <div className='flex items-center justify-between text-muted-foreground text-sm font-medium px-2'>
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
            <div key={i} className='px-3 py-2 rounded-lg hover:bg-accent cursor-pointer text-foreground text-sm'>
              {label}
            </div>
          ))}
        </div>

        <div className='mt-6 mb-2'>
          <div className='text-muted-foreground text-sm font-medium px-2'>Older</div>
        </div>

        <div className='space-y-1'>
          {older.map((label, i) => (
            <div key={i} className='px-3 py-2 rounded-lg hover:bg-accent cursor-pointer text-foreground text-sm'>
              {label}
            </div>
          ))}
        </div>
      </ScrollArea>

      {/* User Profile */}
      <div className='px-3 py-4 border-t border-border'>
        <div className='flex items-center gap-3'>
          <Avatar className='h-8 w-8 bg-muted'>
            <AvatarFallback className='text-muted-foreground text-sm'>J</AvatarFallback>
          </Avatar>
          <div>
            <div className='text-foreground text-sm font-medium'>Jubayer</div>
            <div className='text-muted-foreground text-xs'>Free</div>
          </div>
        </div>
      </div>
    </div>
  )
}



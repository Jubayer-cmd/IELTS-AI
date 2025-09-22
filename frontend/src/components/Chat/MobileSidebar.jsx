import { Sheet, SheetContent, SheetTrigger } from '@/components/ui/sheet'
import { ScrollArea } from '@/components/ui/scroll-area'
import { Button } from '@/components/ui/button'
import { Input } from '@/components/ui/input'
import { Pin, Search, Plus, ChevronDown, Settings, Sun, MessageSquarePlus } from 'lucide-react'
import { Avatar, AvatarFallback } from '@/components/ui/avatar'

export default function MobileSidebar({ open, onOpenChange, children }) {
  const pinned = ['Telegram Mini Apps Overview']
  const older = [
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

  return (
    <Sheet open={open} onOpenChange={onOpenChange}>
      {children && <SheetTrigger asChild>{children}</SheetTrigger>}
      <SheetContent side="left" className="w-80 p-0 bg-card border-border">
        <div className='h-full flex flex-col'>
          {/* Header */}
          <div className='flex items-center justify-between px-4 py-4 border-b border-border'>
            <div className='flex items-center gap-2 text-foreground font-semibold text-lg'>
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
          <div className='px-4 py-4'>
            <Button className='w-full bg-primary hover:bg-primary/90 text-primary-foreground h-11 rounded-lg font-medium flex items-center justify-center gap-2'>
              <MessageSquarePlus className='h-4 w-4' />
              New Chat
            </Button>
          </div>

          {/* Search */}
          <div className='px-4 mb-4 relative'>
            <Input
              placeholder='Search your threads...'
              className='bg-background border-border text-foreground placeholder-muted-foreground pl-9'
            />
            <Search className='h-4 w-4 absolute left-7 top-1/2 -translate-y-1/2 text-muted-foreground pointer-events-none' />
          </div>

          {/* Pinned Section */}
          <div className='px-4 mb-2'>
            <div className='flex items-center justify-between text-muted-foreground text-sm font-medium px-2'>
              <span className='flex items-center gap-2'>
                <Pin className='h-3 w-3' />
                Pinned
              </span>
              <ChevronDown className='h-3 w-3' />
            </div>
          </div>

          {/* Chat List */}
          <ScrollArea className='flex-1 px-4'>
            <div className='space-y-1'>
              {pinned.map((label, i) => (
                <div
                  key={i}
                  className='px-3 py-3 rounded-lg hover:bg-accent cursor-pointer text-foreground text-sm'
                  onClick={() => onOpenChange(false)}
                >
                  {label}
                </div>
              ))}
            </div>

            <div className='mt-6 mb-2'>
              <div className='text-muted-foreground text-sm font-medium px-2'>Older</div>
            </div>

            <div className='space-y-1'>
              {older.map((label, i) => (
                <div
                  key={i}
                  className='px-3 py-3 rounded-lg hover:bg-accent cursor-pointer text-foreground text-sm'
                  onClick={() => onOpenChange(false)}
                >
                  {label}
                </div>
              ))}
            </div>
          </ScrollArea>

          {/* User Profile */}
          <div className='px-4 py-4 border-t border-border'>
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
      </SheetContent>
    </Sheet>
  )
}
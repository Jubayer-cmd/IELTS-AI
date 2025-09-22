import { Button } from '@/components/ui/button'
import { Menu, Plus } from 'lucide-react'
import SettingsDialog from '@/components/Settings/SettingsDialog'

export default function MobileHeader({ onMenuClick }) {
  return (
    <header className='bg-card border-b border-border px-4 py-3 flex items-center justify-between'>
      <div className='flex items-center gap-3'>
        <Button
          variant='ghost'
          size='icon'
          onClick={onMenuClick}
          className='h-9 w-9'
        >
          <Menu className='h-5 w-5' />
        </Button>
        <h1 className='text-foreground font-semibold text-lg'>IELTS-AI</h1>
      </div>

      <div className='flex items-center gap-2'>
        <Button
          variant='ghost'
          size='icon'
          className='h-9 w-9 bg-primary hover:bg-primary/90 text-primary-foreground'
        >
          <Plus className='h-4 w-4' />
        </Button>

        <SettingsDialog>
          <Button variant='ghost' size='icon' className='h-9 w-9'>
            <div className='h-2 w-2 rounded-full bg-primary' />
          </Button>
        </SettingsDialog>
      </div>
    </header>
  )
}
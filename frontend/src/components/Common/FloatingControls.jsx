import SettingsDialog from '@/components/Settings/SettingsDialog'
import { Button } from '@/components/ui/button'
import { SlidersHorizontal } from 'lucide-react'

export default function FloatingControls() {
  return (
    <div className='fixed top-4 right-4 z-50'>
      <SettingsDialog>
        <Button
          variant='ghost'
          size='icon'
          className='h-8 w-8 text-muted-foreground hover:text-foreground hover:bg-accent/30'
          title='Theme'
        >
          <SlidersHorizontal className='h-4 w-4' />
        </Button>
      </SettingsDialog>
    </div>
  )
}

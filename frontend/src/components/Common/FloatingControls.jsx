import SettingsDialog from '@/components/Settings/SettingsDialog'
import { Button } from '@/components/ui/button'

export default function FloatingControls() {
  return (
    <div className='fixed right-4 md:right-6 top-4 md:top-6 z-50 flex items-center gap-2'>
      <SettingsDialog>
        <Button variant='outline' className='rounded-full text-xs md:text-sm px-3 md:px-4'>
          Theme
        </Button>
      </SettingsDialog>
    </div>
  )
}



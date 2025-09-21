import SettingsDialog from '@/components/Settings/SettingsDialog'
import { Button } from '@/components/ui/button'

export default function FloatingControls() {
  return (
    <div className='fixed right-6 top-6 z-50 flex items-center gap-2'>
      <SettingsDialog>
        <Button variant='outline' className='rounded-full'>Theme</Button>
      </SettingsDialog>
    </div>
  )
}



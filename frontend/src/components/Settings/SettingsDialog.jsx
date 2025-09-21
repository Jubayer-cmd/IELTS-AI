import { Dialog, DialogContent, DialogHeader, DialogTitle, DialogTrigger } from '@/components/ui/dialog'
import { Button } from '@/components/ui/button'
import { useTheme } from '@/context/ThemeProvider'

export default function SettingsDialog({ children }) {
  const { primary, setPrimary, options } = useTheme()
  return (
    <Dialog>
      <DialogTrigger asChild>{children}</DialogTrigger>
      <DialogContent>
        <DialogHeader>
          <DialogTitle>Appearance</DialogTitle>
        </DialogHeader>
        <div className='grid grid-cols-5 gap-3'>
          {options.map((opt) => (
            <button
              key={opt}
              onClick={() => setPrimary(opt)}
              className={`aspect-square rounded-md border flex items-center justify-center ${
                primary === opt ? 'ring-2 ring-primary' : ''
              } theme-${opt}`}
              title={opt}
            >
              <span className='h-6 w-6 rounded-full' style={{ backgroundColor: 'hsl(var(--primary))' }} />
            </button>
          ))}
        </div>
        <div className='pt-2 text-xs text-muted-foreground'>Theme persists in your browser.</div>
      </DialogContent>
    </Dialog>
  )
}



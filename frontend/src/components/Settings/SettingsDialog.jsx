import { Dialog, DialogContent, DialogHeader, DialogTitle, DialogTrigger } from '@/components/ui/dialog'
import { Button } from '@/components/ui/button'
import { useTheme } from '@/context/ThemeProvider'

const THEME_COLORS = {
  violet: 'hsl(262 83% 58%)',
  indigo: 'hsl(231 69% 58%)',
  emerald: 'hsl(152 76% 36%)',
  rose: 'hsl(346 77% 49%)',
  amber: 'hsl(38 92% 50%)'
}

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
              className={`aspect-square rounded-md border border-border bg-card hover:bg-accent flex items-center justify-center transition-colors ${
                primary === opt ? 'ring-2 ring-primary' : ''
              }`}
              title={opt}
            >
              <span
                className='h-6 w-6 rounded-full'
                style={{ backgroundColor: THEME_COLORS[opt] }}
              />
            </button>
          ))}
        </div>
        <div className='pt-2 text-xs text-muted-foreground'>Theme persists in your browser.</div>
      </DialogContent>
    </Dialog>
  )
}



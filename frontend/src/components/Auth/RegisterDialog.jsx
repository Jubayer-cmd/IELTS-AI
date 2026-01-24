import { useState } from 'react'
import { Dialog, DialogContent, DialogHeader, DialogTitle, DialogTrigger } from '@/components/ui/dialog'
import { Input } from '@/components/ui/input'
import { Label } from '@/components/ui/label'
import { Button } from '@/components/ui/button'
import { useRegister } from '@/hooks/useAuth'
import { Loader2 } from 'lucide-react'

export default function RegisterDialog({ children }) {
  const [open, setOpen] = useState(false)
  const [name, setName] = useState('')
  const [email, setEmail] = useState('')
  const [password, setPassword] = useState('')
  const [confirm, setConfirm] = useState('')
  const [validationError, setValidationError] = useState('')

  const registerMutation = useRegister()

  const onSubmit = async (e) => {
    e.preventDefault()
    setValidationError('')

    // Client-side validation
    if (password !== confirm) {
      setValidationError('Passwords do not match')
      return
    }

    if (password.length < 6) {
      setValidationError('Password must be at least 6 characters')
      return
    }

    registerMutation.mutate(
      { name: name || email.split('@')[0], email, password },
      {
        onSuccess: () => {
          setOpen(false)
          resetForm()
        },
      }
    )
  }

  const resetForm = () => {
    setName('')
    setEmail('')
    setPassword('')
    setConfirm('')
    setValidationError('')
    registerMutation.reset()
  }

  const handleOpenChange = (isOpen) => {
    setOpen(isOpen)
    if (!isOpen) {
      resetForm()
    }
  }

  const error = validationError ||
    (registerMutation.isError &&
      (registerMutation.error?.response?.data?.detail || 'Registration failed. Please try again.'))

  return (
    <Dialog open={open} onOpenChange={handleOpenChange}>
      <DialogTrigger asChild>{children}</DialogTrigger>
      <DialogContent>
        <DialogHeader>
          <DialogTitle>Create account</DialogTitle>
        </DialogHeader>
        <form onSubmit={onSubmit} className="space-y-4">
          <div className="space-y-2">
            <Label htmlFor="reg_name">Name (optional)</Label>
            <Input
              id="reg_name"
              type="text"
              placeholder="John Doe"
              value={name}
              onChange={(e) => setName(e.target.value)}
              disabled={registerMutation.isPending}
            />
          </div>
          <div className="space-y-2">
            <Label htmlFor="reg_email">Email</Label>
            <Input
              id="reg_email"
              type="email"
              placeholder="you@example.com"
              value={email}
              onChange={(e) => setEmail(e.target.value)}
              disabled={registerMutation.isPending}
              required
            />
          </div>
          <div className="space-y-2">
            <Label htmlFor="reg_password">Password</Label>
            <Input
              id="reg_password"
              type="password"
              placeholder="••••••••"
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              disabled={registerMutation.isPending}
              required
            />
          </div>
          <div className="space-y-2">
            <Label htmlFor="reg_confirm">Confirm password</Label>
            <Input
              id="reg_confirm"
              type="password"
              placeholder="••••••••"
              value={confirm}
              onChange={(e) => setConfirm(e.target.value)}
              disabled={registerMutation.isPending}
              required
            />
          </div>

          {error && (
            <div className="text-sm text-red-500 bg-red-50 dark:bg-red-950/50 p-3 rounded-md">
              {error}
            </div>
          )}

          <Button type="submit" className="w-full" disabled={registerMutation.isPending}>
            {registerMutation.isPending ? (
              <>
                <Loader2 className="mr-2 h-4 w-4 animate-spin" />
                Creating account...
              </>
            ) : (
              'Create account'
            )}
          </Button>
        </form>
      </DialogContent>
    </Dialog>
  )
}

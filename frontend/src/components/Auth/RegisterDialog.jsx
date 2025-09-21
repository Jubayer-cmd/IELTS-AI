import { useState } from 'react'
import { Dialog, DialogContent, DialogHeader, DialogTitle, DialogTrigger } from '@/components/ui/dialog'
import { Input } from '@/components/ui/input'
import { Label } from '@/components/ui/label'
import { Button } from '@/components/ui/button'
import { useAuth } from '@/services/auth'

export default function RegisterDialog({ children }) {
  const [open, setOpen] = useState(false)
  const [email, setEmail] = useState('')
  const [password, setPassword] = useState('')
  const [confirm, setConfirm] = useState('')
  const { register } = useAuth()
  const onSubmit = async () => {
    if (password !== confirm) return
    await register({ email, password })
    setOpen(false)
  }
  return (
    <Dialog open={open} onOpenChange={setOpen}>
      <DialogTrigger asChild>{children}</DialogTrigger>
      <DialogContent>
        <DialogHeader>
          <DialogTitle>Create account</DialogTitle>
        </DialogHeader>
        <div className='space-y-4'>
          <div className='space-y-2'>
            <Label htmlFor='reg_email'>Email</Label>
            <Input id='reg_email' type='email' placeholder='you@example.com' value={email} onChange={(e) => setEmail(e.target.value)} />
          </div>
          <div className='space-y-2'>
            <Label htmlFor='reg_password'>Password</Label>
            <Input id='reg_password' type='password' placeholder='••••••••' value={password} onChange={(e) => setPassword(e.target.value)} />
          </div>
          <div className='space-y-2'>
            <Label htmlFor='reg_confirm'>Confirm password</Label>
            <Input id='reg_confirm' type='password' placeholder='••••••••' value={confirm} onChange={(e) => setConfirm(e.target.value)} />
          </div>
          <Button className='w-full' onClick={onSubmit}>Create account</Button>
        </div>
      </DialogContent>
    </Dialog>
  )
}



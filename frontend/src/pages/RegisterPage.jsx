import { useState } from 'react'
import { Link, useNavigate } from 'react-router-dom'
import { Input } from '@/components/ui/input'
import { Label } from '@/components/ui/label'
import { Button } from '@/components/ui/button'
import { useRegister } from '@/hooks/useAuth'
import { Loader2 } from 'lucide-react'

export default function RegisterPage() {
  const navigate = useNavigate()
  const [name, setName] = useState('')
  const [email, setEmail] = useState('')
  const [password, setPassword] = useState('')
  const [confirmPassword, setConfirmPassword] = useState('')
  const [validationError, setValidationError] = useState('')

  const registerMutation = useRegister()

  const onSubmit = async (e) => {
    e.preventDefault()
    setValidationError('')

    if (password !== confirmPassword) {
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
          navigate('/')
        },
      }
    )
  }

  const error = validationError ||
    (registerMutation.isError &&
      (registerMutation.error?.response?.data?.detail || 'Registration failed. Please try again.'))

  return (
    <div className='min-h-screen bg-background flex items-center justify-center p-4'>
      <div className='w-full max-w-md'>
        <div className='text-center mb-8'>
          <h1 className='text-2xl font-bold text-foreground mb-2'>Create an account</h1>
          <p className='text-muted-foreground'>Get started with IELTS Writing AI</p>
        </div>

        <div className='bg-card rounded-xl p-6 border border-border'>
          <form onSubmit={onSubmit} className='space-y-4'>
            <div className='space-y-2'>
              <Label htmlFor='name'>Name (optional)</Label>
              <Input
                id='name'
                type='text'
                placeholder='John Doe'
                value={name}
                onChange={(e) => setName(e.target.value)}
                disabled={registerMutation.isPending}
              />
            </div>
            <div className='space-y-2'>
              <Label htmlFor='email'>Email</Label>
              <Input
                id='email'
                type='email'
                placeholder='you@example.com'
                value={email}
                onChange={(e) => setEmail(e.target.value)}
                disabled={registerMutation.isPending}
                required
              />
            </div>
            <div className='space-y-2'>
              <Label htmlFor='password'>Password</Label>
              <Input
                id='password'
                type='password'
                placeholder='••••••••'
                value={password}
                onChange={(e) => setPassword(e.target.value)}
                disabled={registerMutation.isPending}
                required
              />
            </div>
            <div className='space-y-2'>
              <Label htmlFor='confirmPassword'>Confirm password</Label>
              <Input
                id='confirmPassword'
                type='password'
                placeholder='••••••••'
                value={confirmPassword}
                onChange={(e) => setConfirmPassword(e.target.value)}
                disabled={registerMutation.isPending}
                required
              />
            </div>

            {error && (
              <div className='text-sm text-red-500 bg-red-50 dark:bg-red-950/50 p-3 rounded-md'>
                {error}
              </div>
            )}

            <Button type='submit' className='w-full' disabled={registerMutation.isPending}>
              {registerMutation.isPending ? (
                <>
                  <Loader2 className='mr-2 h-4 w-4 animate-spin' />
                  Creating account...
                </>
              ) : (
                'Create account'
              )}
            </Button>
          </form>

          <div className='mt-6 text-center text-sm text-muted-foreground'>
            Already have an account?{' '}
            <Link to='/login' className='text-primary hover:underline font-medium'>
              Sign in
            </Link>
          </div>
        </div>

        <div className='mt-4 text-center'>
          <Link to='/' className='text-sm text-muted-foreground hover:text-foreground'>
            ← Back to home
          </Link>
        </div>
      </div>
    </div>
  )
}

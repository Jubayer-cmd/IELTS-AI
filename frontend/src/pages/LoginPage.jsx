import { useState } from 'react'
import { Link, useNavigate } from 'react-router-dom'
import { Input } from '@/components/ui/input'
import { Label } from '@/components/ui/label'
import { Button } from '@/components/ui/button'
import { useLogin } from '@/hooks/useAuth'
import { Loader2 } from 'lucide-react'

export default function LoginPage() {
  const navigate = useNavigate()
  const [email, setEmail] = useState('')
  const [password, setPassword] = useState('')

  const loginMutation = useLogin()

  const onSubmit = async (e) => {
    e.preventDefault()
    loginMutation.mutate(
      { email, password },
      {
        onSuccess: () => {
          navigate('/')
        },
      }
    )
  }

  return (
    <div className='min-h-screen bg-background flex items-center justify-center p-4'>
      <div className='w-full max-w-md'>
        <div className='text-center mb-8'>
          <h1 className='text-2xl font-bold text-foreground mb-2'>Welcome back</h1>
          <p className='text-muted-foreground'>Sign in to your account to continue</p>
        </div>

        <div className='bg-card rounded-xl p-6 border border-border'>
          <form onSubmit={onSubmit} className='space-y-4'>
            <div className='space-y-2'>
              <Label htmlFor='email'>Email</Label>
              <Input
                id='email'
                type='email'
                placeholder='you@example.com'
                value={email}
                onChange={(e) => setEmail(e.target.value)}
                disabled={loginMutation.isPending}
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
                disabled={loginMutation.isPending}
                required
              />
            </div>

            {loginMutation.isError && (
              <div className='text-sm text-red-500 bg-red-50 dark:bg-red-950/50 p-3 rounded-md'>
                {loginMutation.error?.response?.data?.detail || 'Invalid email or password'}
              </div>
            )}

            <Button type='submit' className='w-full' disabled={loginMutation.isPending}>
              {loginMutation.isPending ? (
                <>
                  <Loader2 className='mr-2 h-4 w-4 animate-spin' />
                  Signing in...
                </>
              ) : (
                'Sign in'
              )}
            </Button>
          </form>

          <div className='mt-6 text-center text-sm text-muted-foreground'>
            Don't have an account?{' '}
            <Link to='/register' className='text-primary hover:underline font-medium'>
              Sign up
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

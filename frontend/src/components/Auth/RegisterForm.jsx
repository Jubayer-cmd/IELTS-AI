// Registration form component (standalone version)
// Note: RegisterDialog.jsx is the primary registration UI used in the app

import { useState } from 'react'
import { useRegister } from '@/hooks/useAuth'

export default function RegisterForm({ onSuccess }) {
  const [name, setName] = useState('')
  const [email, setEmail] = useState('')
  const [password, setPassword] = useState('')
  const [confirmPassword, setConfirmPassword] = useState('')
  const [validationError, setValidationError] = useState('')

  const registerMutation = useRegister()

  const handleSubmit = async (e) => {
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
          setName('')
          setEmail('')
          setPassword('')
          setConfirmPassword('')
          onSuccess?.()
        },
      }
    )
  }

  const error = validationError ||
    (registerMutation.isError &&
      (registerMutation.error?.response?.data?.detail || 'Registration failed'))

  return (
    <div className="max-w-md mx-auto">
      <form onSubmit={handleSubmit} className="space-y-4">
        <div>
          <label htmlFor="name">Name (optional)</label>
          <input
            type="text"
            name="name"
            value={name}
            onChange={(e) => setName(e.target.value)}
            disabled={registerMutation.isPending}
            className="w-full px-3 py-2 border rounded-md"
          />
        </div>

        <div>
          <label htmlFor="email">Email</label>
          <input
            type="email"
            name="email"
            value={email}
            onChange={(e) => setEmail(e.target.value)}
            disabled={registerMutation.isPending}
            required
            className="w-full px-3 py-2 border rounded-md"
          />
        </div>

        <div>
          <label htmlFor="password">Password</label>
          <input
            type="password"
            name="password"
            value={password}
            onChange={(e) => setPassword(e.target.value)}
            disabled={registerMutation.isPending}
            required
            className="w-full px-3 py-2 border rounded-md"
          />
        </div>

        <div>
          <label htmlFor="confirmPassword">Confirm Password</label>
          <input
            type="password"
            name="confirmPassword"
            value={confirmPassword}
            onChange={(e) => setConfirmPassword(e.target.value)}
            disabled={registerMutation.isPending}
            required
            className="w-full px-3 py-2 border rounded-md"
          />
        </div>

        {error && <div className="text-red-500">{error}</div>}

        <button
          type="submit"
          disabled={registerMutation.isPending}
          className="w-full bg-green-500 text-white py-2 rounded-md hover:bg-green-600 disabled:opacity-50"
        >
          {registerMutation.isPending ? 'Creating Account...' : 'Register'}
        </button>
      </form>
    </div>
  )
}

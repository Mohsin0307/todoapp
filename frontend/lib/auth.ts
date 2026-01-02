/**
 * Simple Auth Client for Demo Mode
 * Works with demo backend's mock authentication
 */

const API_BASE_URL = process.env["NEXT_PUBLIC_API_URL"] || "http://localhost:8002"

interface AuthResponse {
  user: {
    id: string
    email: string
    name: string
  }
  session: {
    token: string
  }
}

// Store session in localStorage for demo
function setSession(data: AuthResponse) {
  if (typeof window !== 'undefined') {
    localStorage.setItem('auth_token', data.session.token)
    localStorage.setItem('auth_user', JSON.stringify(data.user))
  }
}

function clearSession() {
  if (typeof window !== 'undefined') {
    localStorage.removeItem('auth_token')
    localStorage.removeItem('auth_user')
  }
}

function getSession() {
  if (typeof window === 'undefined') return null

  const token = localStorage.getItem('auth_token')
  const userStr = localStorage.getItem('auth_user')

  if (!token || !userStr) return null

  return {
    token,
    user: JSON.parse(userStr)
  }
}

export const signUp = {
  email: async ({ name, email, password }: { name: string; email: string; password: string }) => {
    const response = await fetch(\`\${API_BASE_URL}/api/auth/sign-up/email\`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ name, email, password })
    })

    if (!response.ok) {
      const error = await response.json().catch(() => ({ detail: 'Signup failed' }))
      throw new Error(error.detail || 'Signup failed')
    }

    const data: AuthResponse = await response.json()
    setSession(data)
    return data
  }
}

export const signIn = {
  email: async ({ email, password }: { email: string; password: string }) => {
    const response = await fetch(\`\${API_BASE_URL}/api/auth/sign-in/email\`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ email, password })
    })

    if (!response.ok) {
      const error = await response.json().catch(() => ({ detail: 'Login failed' }))
      throw new Error(error.detail || 'Login failed')
    }

    const data: AuthResponse = await response.json()
    setSession(data)
    return data
  }
}

export const signOut = async () => {
  clearSession()
}

export function useSession() {
  const session = getSession()

  return {
    data: session,
    isPending: false,
    error: null
  }
}

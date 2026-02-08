/**
 * Auth Client - Handles user authentication with backend JWT
 */

const API_BASE_URL = process.env["NEXT_PUBLIC_API_URL"] || "http://localhost:8000"

interface AuthUser {
  id: string
  email: string
  name: string
}

interface BackendAuthResponse {
  user: AuthUser
  token: string
  message: string
}

// Store session in localStorage
function setSession(user: AuthUser, token: string) {
  if (typeof window !== 'undefined') {
    localStorage.setItem('auth_token', token)
    localStorage.setItem('auth_user', JSON.stringify(user))
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
    user: JSON.parse(userStr) as AuthUser
  }
}

export const signUp = {
  email: async ({ name, email, password }: { name: string; email: string; password: string }) => {
    const response = await fetch(`${API_BASE_URL}/api/auth/signup`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      credentials: 'include',
      body: JSON.stringify({ name, email, password })
    })

    if (!response.ok) {
      const error = await response.json().catch(() => ({ detail: 'Signup failed' }))
      throw new Error(error.detail || 'Signup failed')
    }

    const data: BackendAuthResponse = await response.json()
    setSession(data.user, data.token)
    return data
  }
}

export const signIn = {
  email: async ({ email, password }: { email: string; password: string }) => {
    const response = await fetch(`${API_BASE_URL}/api/auth/login`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      credentials: 'include',
      body: JSON.stringify({ email, password })
    })

    if (!response.ok) {
      const error = await response.json().catch(() => ({ detail: 'Login failed' }))
      throw new Error(error.detail || 'Login failed')
    }

    const data: BackendAuthResponse = await response.json()
    setSession(data.user, data.token)
    return data
  }
}

export const signOut = async () => {
  try {
    await fetch(`${API_BASE_URL}/api/auth/logout`, {
      method: 'POST',
      credentials: 'include',
    })
  } catch {
    // Ignore network errors on logout
  }
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

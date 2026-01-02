/**
 * Better Auth Client Configuration
 *
 * Configures Better Auth with JWT plugin for authentication.
 * Uses httpOnly cookies for secure token storage.
 */

import { createAuthClient } from "better-auth/react"

export const authClient = createAuthClient({
  baseURL: process.env["NEXT_PUBLIC_API_URL"] || "http://localhost:8000",
})

export const { signIn, signUp, signOut, useSession } = authClient

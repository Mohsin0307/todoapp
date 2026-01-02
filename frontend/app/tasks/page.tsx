'use client'

import { useEffect } from 'react'
import { useRouter } from 'next/navigation'
import { useSession, signOut } from '@/lib/auth'
import TaskList from '@/components/TaskList'
import TaskForm from '@/components/TaskForm'

export default function TasksPage() {
  const router = useRouter()
  const { data: session, isPending } = useSession()

  useEffect(() => {
    if (!isPending && !session) {
      // Redirect to login if not authenticated
      router.push('/login')
    }
  }, [session, isPending, router])

  const handleSignOut = async () => {
    await signOut()
    router.push('/')
  }

  if (isPending) {
    return (
      <div className="flex min-h-screen items-center justify-center">
        <div className="text-center">
          <div className="inline-block h-8 w-8 animate-spin rounded-full border-4 border-solid border-current border-r-transparent align-[-0.125em] motion-reduce:animate-[spin_1.5s_linear_infinite]"></div>
          <p className="mt-4">Loading...</p>
        </div>
      </div>
    )
  }

  if (!session) {
    return null // Will redirect
  }

  return (
    <main className="min-h-screen p-8">
      <div className="max-w-4xl mx-auto">
        {/* Header */}
        <div className="mb-8 flex items-center justify-between">
          <div>
            <h1 className="text-3xl font-bold">My Tasks</h1>
            <p className="mt-2 text-sm text-gray-600 dark:text-gray-400">
              Welcome back, {session.user?.name || session.user?.email}
            </p>
          </div>
          <button
            onClick={handleSignOut}
            className="rounded-lg border border-gray-300 px-4 py-2 text-sm font-medium transition hover:bg-gray-100 focus:outline-none focus:ring focus:ring-gray-200 dark:border-gray-600 dark:hover:bg-gray-800"
          >
            Sign Out
          </button>
        </div>

        {/* Task Form */}
        <div className="mb-8">
          <TaskForm />
        </div>

        {/* Task List */}
        <TaskList />
      </div>
    </main>
  )
}

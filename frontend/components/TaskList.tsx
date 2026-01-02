'use client'

import { useState, useEffect } from 'react'
import { apiClient, type Task } from '@/lib/api'
import TaskItem from './TaskItem'

export default function TaskList() {
  const [tasks, setTasks] = useState<Task[]>([])
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState('')
  const [filter, setFilter] = useState<'all' | 'active' | 'completed'>('all')

  const loadTasks = async () => {
    try {
      setLoading(true)
      setError('')

      const completedFilter =
        filter === 'all' ? undefined : filter === 'completed' ? true : false

      const fetchedTasks = await apiClient.listTasks(
        completedFilter === undefined
          ? { limit: 100 }
          : { completed: completedFilter, limit: 100 }
      )

      setTasks(fetchedTasks)
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Failed to load tasks')
    } finally {
      setLoading(false)
    }
  }

  useEffect(() => {
    loadTasks()
  }, [filter])

  const handleTaskUpdate = () => {
    // Reload tasks after update/delete/toggle
    loadTasks()
  }

  if (loading) {
    return (
      <div className="text-center py-12">
        <div className="inline-block h-8 w-8 animate-spin rounded-full border-4 border-solid border-current border-r-transparent align-[-0.125em] motion-reduce:animate-[spin_1.5s_linear_infinite]"></div>
        <p className="mt-4 text-sm text-gray-600 dark:text-gray-400">Loading tasks...</p>
      </div>
    )
  }

  if (error) {
    return (
      <div className="rounded-lg bg-red-50 p-4 text-sm text-red-800 dark:bg-red-900/20 dark:text-red-400">
        {error}
      </div>
    )
  }

  return (
    <div>
      {/* Filter Tabs */}
      <div className="mb-6 flex gap-2 border-b border-gray-200 dark:border-gray-700">
        <button
          onClick={() => setFilter('all')}
          className={`px-4 py-2 text-sm font-medium transition ${
            filter === 'all'
              ? 'border-b-2 border-primary-600 text-primary-600'
              : 'text-gray-600 hover:text-gray-900 dark:text-gray-400 dark:hover:text-gray-200'
          }`}
        >
          All ({tasks.length})
        </button>
        <button
          onClick={() => setFilter('active')}
          className={`px-4 py-2 text-sm font-medium transition ${
            filter === 'active'
              ? 'border-b-2 border-primary-600 text-primary-600'
              : 'text-gray-600 hover:text-gray-900 dark:text-gray-400 dark:hover:text-gray-200'
          }`}
        >
          Active
        </button>
        <button
          onClick={() => setFilter('completed')}
          className={`px-4 py-2 text-sm font-medium transition ${
            filter === 'completed'
              ? 'border-b-2 border-primary-600 text-primary-600'
              : 'text-gray-600 hover:text-gray-900 dark:text-gray-400 dark:hover:text-gray-200'
          }`}
        >
          Completed
        </button>
      </div>

      {/* Task Items */}
      {tasks.length === 0 ? (
        <div className="text-center py-12">
          <p className="text-gray-600 dark:text-gray-400">
            {filter === 'all'
              ? 'No tasks yet. Create your first task above!'
              : filter === 'active'
              ? 'No active tasks.'
              : 'No completed tasks.'}
          </p>
        </div>
      ) : (
        <div className="space-y-4">
          {tasks.map((task) => (
            <TaskItem key={task.id} task={task} onUpdate={handleTaskUpdate} />
          ))}
        </div>
      )}
    </div>
  )
}

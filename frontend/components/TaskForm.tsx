'use client'

import { useState } from 'react'
import { useForm } from 'react-hook-form'
import { apiClient, type TaskCreate } from '@/lib/api'

interface TaskFormProps {
  onTaskCreated?: () => void
}

export default function TaskForm({ onTaskCreated }: TaskFormProps) {
  const [isSubmitting, setIsSubmitting] = useState(false)
  const [error, setError] = useState('')

  const {
    register,
    handleSubmit,
    reset,
    formState: { errors },
  } = useForm<TaskCreate>()

  const onSubmit = async (data: TaskCreate) => {
    try {
      setIsSubmitting(true)
      setError('')

      await apiClient.createTask(data)

      // Clear form
      reset()

      // Notify parent to refresh list
      if (onTaskCreated) {
        onTaskCreated()
      }

      // Refresh page to reload task list
      window.location.reload()
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Failed to create task')
    } finally {
      setIsSubmitting(false)
    }
  }

  return (
    <div className="rounded-lg border border-gray-200 p-6 dark:border-gray-700">
      <h2 className="mb-4 text-xl font-semibold">Create New Task</h2>

      <form onSubmit={handleSubmit(onSubmit)} className="space-y-4">
        {error && (
          <div className="rounded-lg bg-red-50 p-3 text-sm text-red-800 dark:bg-red-900/20 dark:text-red-400">
            {error}
          </div>
        )}

        <div>
          <label htmlFor="title" className="block text-sm font-medium mb-2">
            Title <span className="text-red-500">*</span>
          </label>
          <input
            id="title"
            {...register('title', {
              required: 'Title is required',
              minLength: {
                value: 1,
                message: 'Title must be at least 1 character',
              },
              maxLength: {
                value: 200,
                message: 'Title must be at most 200 characters',
              },
            })}
            className="w-full rounded-lg border border-gray-300 px-4 py-2 focus:border-primary-500 focus:outline-none focus:ring focus:ring-primary-200 dark:border-gray-600 dark:bg-gray-800"
            placeholder="What needs to be done?"
          />
          {errors.title && (
            <p className="mt-1 text-sm text-red-600 dark:text-red-400">
              {errors.title.message}
            </p>
          )}
        </div>

        <div>
          <label htmlFor="description" className="block text-sm font-medium mb-2">
            Description
          </label>
          <textarea
            id="description"
            {...register('description')}
            rows={3}
            className="w-full rounded-lg border border-gray-300 px-4 py-2 focus:border-primary-500 focus:outline-none focus:ring focus:ring-primary-200 dark:border-gray-600 dark:bg-gray-800"
            placeholder="Additional details (optional)"
          />
        </div>

        <button
          type="submit"
          disabled={isSubmitting}
          className="w-full rounded-lg bg-primary-600 px-4 py-2 text-sm font-medium text-white transition hover:bg-primary-700 focus:outline-none focus:ring focus:ring-primary-300 disabled:opacity-50 disabled:cursor-not-allowed"
        >
          {isSubmitting ? 'Creating...' : 'Create Task'}
        </button>
      </form>
    </div>
  )
}

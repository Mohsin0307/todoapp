'use client'

import { useState } from 'react'
import { apiClient, type Task } from '@/lib/api'

interface TaskItemProps {
  task: Task
  onUpdate: () => void
}

export default function TaskItem({ task, onUpdate }: TaskItemProps) {
  const [isEditing, setIsEditing] = useState(false)
  const [title, setTitle] = useState(task.title)
  const [description, setDescription] = useState(task.description || '')
  const [isSubmitting, setIsSubmitting] = useState(false)

  const handleToggleComplete = async () => {
    try {
      await apiClient.toggleComplete(task.id)
      onUpdate()
    } catch (err) {
      console.error('Failed to toggle completion:', err)
    }
  }

  const handleDelete = async () => {
    if (!confirm('Are you sure you want to delete this task?')) {
      return
    }

    try {
      await apiClient.deleteTask(task.id)
      onUpdate()
    } catch (err) {
      console.error('Failed to delete task:', err)
    }
  }

  const handleUpdate = async () => {
    try {
      setIsSubmitting(true)
      await apiClient.updateTask(task.id, {
        title: title.trim(),
        description: description.trim() || null,
      })
      setIsEditing(false)
      onUpdate()
    } catch (err) {
      console.error('Failed to update task:', err)
    } finally {
      setIsSubmitting(false)
    }
  }

  const handleCancelEdit = () => {
    setTitle(task.title)
    setDescription(task.description || '')
    setIsEditing(false)
  }

  return (
    <div className="rounded-lg border border-gray-200 p-4 transition hover:shadow-md dark:border-gray-700">
      {isEditing ? (
        // Edit mode
        <div className="space-y-4">
          <input
            type="text"
            value={title}
            onChange={(e) => setTitle(e.target.value)}
            className="w-full rounded-lg border border-gray-300 px-3 py-2 focus:border-primary-500 focus:outline-none focus:ring focus:ring-primary-200 dark:border-gray-600 dark:bg-gray-800"
            placeholder="Task title"
          />
          <textarea
            value={description}
            onChange={(e) => setDescription(e.target.value)}
            rows={3}
            className="w-full rounded-lg border border-gray-300 px-3 py-2 focus:border-primary-500 focus:outline-none focus:ring focus:ring-primary-200 dark:border-gray-600 dark:bg-gray-800"
            placeholder="Description (optional)"
          />
          <div className="flex gap-2">
            <button
              onClick={handleUpdate}
              disabled={isSubmitting || !title.trim()}
              className="rounded-lg bg-primary-600 px-4 py-2 text-sm font-medium text-white transition hover:bg-primary-700 disabled:opacity-50 disabled:cursor-not-allowed"
            >
              {isSubmitting ? 'Saving...' : 'Save'}
            </button>
            <button
              onClick={handleCancelEdit}
              disabled={isSubmitting}
              className="rounded-lg border border-gray-300 px-4 py-2 text-sm font-medium transition hover:bg-gray-100 dark:border-gray-600 dark:hover:bg-gray-800 disabled:opacity-50 disabled:cursor-not-allowed"
            >
              Cancel
            </button>
          </div>
        </div>
      ) : (
        // View mode
        <div>
          <div className="flex items-start gap-3">
            <input
              type="checkbox"
              checked={task.completed}
              onChange={handleToggleComplete}
              className="mt-1 h-5 w-5 rounded border-gray-300 text-primary-600 focus:ring-primary-500 cursor-pointer"
            />
            <div className="flex-1">
              <h3
                className={`font-medium ${
                  task.completed
                    ? 'text-gray-500 line-through dark:text-gray-400'
                    : 'text-gray-900 dark:text-gray-100'
                }`}
              >
                {task.title}
              </h3>
              {task.description && (
                <p
                  className={`mt-1 text-sm ${
                    task.completed
                      ? 'text-gray-400 line-through dark:text-gray-500'
                      : 'text-gray-600 dark:text-gray-400'
                  }`}
                >
                  {task.description}
                </p>
              )}
              <p className="mt-2 text-xs text-gray-500 dark:text-gray-500">
                Created {new Date(task.created_at).toLocaleString()}
              </p>
            </div>
          </div>

          <div className="mt-3 flex gap-2">
            <button
              onClick={() => setIsEditing(true)}
              className="text-sm text-primary-600 hover:text-primary-700 dark:text-primary-400"
            >
              Edit
            </button>
            <button
              onClick={handleDelete}
              className="text-sm text-red-600 hover:text-red-700 dark:text-red-400"
            >
              Delete
            </button>
          </div>
        </div>
      )}
    </div>
  )
}

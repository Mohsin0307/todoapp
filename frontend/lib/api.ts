/**
 * API Client - HTTP requests to backend
 *
 * Handles API communication with JWT token injection and error handling.
 */

const API_BASE_URL = process.env["NEXT_PUBLIC_API_URL"] || "http://localhost:8000"

export interface Task {
  id: string
  user_id: string
  title: string
  description: string | null
  completed: boolean
  created_at: string
  updated_at: string
}

export interface TaskCreate {
  title: string
  description?: string | null
}

export interface TaskUpdate {
  title?: string
  description?: string | null
  completed?: boolean
}

class APIClient {
  private baseURL: string

  constructor(baseURL: string) {
    this.baseURL = baseURL
  }

  private async request<T>(
    endpoint: string,
    options: RequestInit = {}
  ): Promise<T> {
    const url = `${this.baseURL}${endpoint}`

    // Get token from Better Auth session (stored in httpOnly cookie)
    // The cookie is automatically sent with requests

    const response = await fetch(url, {
      ...options,
      credentials: "include", // Include cookies in requests
      headers: {
        "Content-Type": "application/json",
        ...options.headers,
      },
    })

    if (!response.ok) {
      const error = await response.json().catch(() => ({
        detail: response.statusText,
      }))
      throw new Error(error.detail || `HTTP ${response.status}`)
    }

    // Handle 204 No Content responses
    if (response.status === 204) {
      return null as T
    }

    return response.json()
  }

  // Task API endpoints

  async listTasks(params?: {
    skip?: number
    limit?: number
    completed?: boolean
  }): Promise<Task[]> {
    const queryParams = new URLSearchParams()
    if (params?.skip !== undefined) queryParams.append("skip", String(params.skip))
    if (params?.limit !== undefined) queryParams.append("limit", String(params.limit))
    if (params?.completed !== undefined)
      queryParams.append("completed", String(params.completed))

    const query = queryParams.toString()
    return this.request<Task[]>(`/api/tasks${query ? `?${query}` : ""}`)
  }

  async createTask(data: TaskCreate): Promise<Task> {
    return this.request<Task>("/api/tasks", {
      method: "POST",
      body: JSON.stringify(data),
    })
  }

  async getTask(taskId: string): Promise<Task> {
    return this.request<Task>(`/api/tasks/${taskId}`)
  }

  async updateTask(taskId: string, data: TaskUpdate): Promise<Task> {
    return this.request<Task>(`/api/tasks/${taskId}`, {
      method: "PUT",
      body: JSON.stringify(data),
    })
  }

  async deleteTask(taskId: string): Promise<void> {
    return this.request<void>(`/api/tasks/${taskId}`, {
      method: "DELETE",
    })
  }

  async toggleComplete(taskId: string): Promise<Task> {
    return this.request<Task>(`/api/tasks/${taskId}/complete`, {
      method: "PATCH",
    })
  }

  async healthCheck(): Promise<{ service: string; status: string; version: string }> {
    return this.request<{ service: string; status: string; version: string }>("/health")
  }
}

export const apiClient = new APIClient(API_BASE_URL)

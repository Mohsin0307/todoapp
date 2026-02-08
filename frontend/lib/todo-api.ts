/**
 * Todo API client for the advanced todo management endpoints.
 */

const API_URL = process.env["NEXT_PUBLIC_API_URL"] || "http://localhost:8000";

export interface TodoItem {
  id: string;
  user_id: string;
  title: string;
  description: string | null;
  status: string;
  priority: string;
  due_date: string | null;
  tags: string[] | null;
  created_at: string;
  updated_at: string;
  is_recurring: boolean;
  recurrence_pattern: string | null;
  recurrence_interval: number | null;
  reminder_enabled: boolean;
  reminder_offset_hours: number | null;
  parent_id: string | null;
}

export interface CreateTodoRequest {
  title: string;
  description?: string;
  priority?: string;
  due_date?: string;
  tags?: string[];
  is_recurring?: boolean;
  recurrence_pattern?: string;
  recurrence_interval?: number;
  recurrence_end_date?: string;
  reminder_enabled?: boolean;
  reminder_offset_hours?: number;
}

export interface UpdateTodoRequest {
  title?: string;
  description?: string;
  status?: string;
  priority?: string;
  due_date?: string;
  tags?: string[];
  is_recurring?: boolean;
  recurrence_pattern?: string;
  recurrence_interval?: number;
  reminder_enabled?: boolean;
  reminder_offset_hours?: number;
}

function getHeaders(): HeadersInit {
  return {
    "Content-Type": "application/json",
  };
}

export async function fetchTodos(
  status?: string,
  priority?: string,
  skip = 0,
  limit = 50
): Promise<TodoItem[]> {
  const params = new URLSearchParams();
  if (status) params.set("status", status);
  if (priority) params.set("priority", priority);
  params.set("skip", String(skip));
  params.set("limit", String(limit));

  const res = await fetch(`${API_URL}/api/todos?${params}`, {
    headers: getHeaders(),
  });
  if (!res.ok) throw new Error("Failed to fetch todos");
  return res.json();
}

export async function fetchTodo(id: string): Promise<TodoItem> {
  const res = await fetch(`${API_URL}/api/todos/${id}`, {
    headers: getHeaders(),
  });
  if (!res.ok) throw new Error("Todo not found");
  return res.json();
}

export async function createTodo(data: CreateTodoRequest): Promise<TodoItem> {
  const res = await fetch(`${API_URL}/api/todos`, {
    method: "POST",
    headers: getHeaders(),
    body: JSON.stringify(data),
  });
  if (!res.ok) throw new Error("Failed to create todo");
  return res.json();
}

export async function updateTodo(
  id: string,
  data: UpdateTodoRequest
): Promise<TodoItem> {
  const res = await fetch(`${API_URL}/api/todos/${id}`, {
    method: "PUT",
    headers: getHeaders(),
    body: JSON.stringify(data),
  });
  if (!res.ok) throw new Error("Failed to update todo");
  return res.json();
}

export async function deleteTodo(id: string): Promise<void> {
  const res = await fetch(`${API_URL}/api/todos/${id}`, {
    method: "DELETE",
    headers: getHeaders(),
  });
  if (!res.ok) throw new Error("Failed to delete todo");
}

export async function fetchRecurringTodos(): Promise<TodoItem[]> {
  const res = await fetch(`${API_URL}/api/todos/recurring`, {
    headers: getHeaders(),
  });
  if (!res.ok) throw new Error("Failed to fetch recurring todos");
  return res.json();
}

export async function generateRecurringInstance(
  todoId: string
): Promise<TodoItem> {
  const res = await fetch(`${API_URL}/api/todos/recurring/${todoId}/generate`, {
    method: "POST",
    headers: getHeaders(),
  });
  if (!res.ok) throw new Error("Failed to generate recurring instance");
  return res.json();
}

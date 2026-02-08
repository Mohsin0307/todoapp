/**
 * Notification service for managing in-app notifications.
 */

const API_URL = process.env["NEXT_PUBLIC_API_URL"] || "http://localhost:8000";

export interface AppNotification {
  id: string;
  type: string;
  title: string;
  message: string;
  priority: string;
  is_read: boolean;
  created_at: string;
  todo_id?: string;
}

function getHeaders(): HeadersInit {
  return {
    "Content-Type": "application/json",
  };
}

export async function fetchNotifications(
  unreadOnly = false,
  limit = 50
): Promise<AppNotification[]> {
  const params = new URLSearchParams();
  if (unreadOnly) params.set("unread_only", "true");
  params.set("limit", String(limit));

  try {
    const res = await fetch(`${API_URL}/api/notifications?${params}`, {
      headers: getHeaders(),
    });
    if (!res.ok) return [];
    return res.json();
  } catch {
    return [];
  }
}

export async function markNotificationRead(
  id: string
): Promise<void> {
  await fetch(`${API_URL}/api/notifications/${id}/read`, {
    method: "PUT",
    headers: getHeaders(),
  });
}

export async function markAllRead(): Promise<void> {
  await fetch(`${API_URL}/api/notifications/read-all`, {
    method: "PUT",
    headers: getHeaders(),
  });
}

export async function getUnreadCount(): Promise<number> {
  try {
    const res = await fetch(`${API_URL}/api/notifications/unread-count`, {
      headers: getHeaders(),
    });
    if (!res.ok) return 0;
    const data = await res.json();
    return data.count || 0;
  } catch {
    return 0;
  }
}

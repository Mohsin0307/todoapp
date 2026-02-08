/**
 * Chat API Client
 *
 * Handles communication with the backend chat endpoint
 * Includes JWT authentication and conversation management
 */

export interface ChatMessage {
  role: "user" | "assistant";
  content: string;
  timestamp: Date;
}

export interface ChatRequest {
  message: string;
  conversation_id?: number | null;
}

export interface ChatResponse {
  conversation_id: number;
  response: string;
  created_at: string;
}

export interface ChatError {
  detail?: string;
  message?: string;
}

/**
 * Send a chat message to the AI assistant
 */
export async function sendChatMessage(
  userId: string,
  message: string,
  conversationId?: number | null,
  token?: string
): Promise<ChatResponse> {
  const apiUrl = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000";

  const headers: HeadersInit = {
    "Content-Type": "application/json",
  };

  // Add JWT token if provided, otherwise try localStorage
  const authToken = token || getAuthToken();
  if (authToken) {
    headers["Authorization"] = `Bearer ${authToken}`;
  }

  const response = await fetch(`${apiUrl}/api/${userId}/chat`, {
    method: "POST",
    headers,
    credentials: "include",
    body: JSON.stringify({
      message,
      conversation_id: conversationId,
    } as ChatRequest),
  });

  if (!response.ok) {
    const errorData: ChatError = await response.json().catch(() => ({
      message: `HTTP error! status: ${response.status}`,
    }));

    throw new Error(errorData.detail || errorData.message || "Failed to send message");
  }

  return response.json();
}

/**
 * Get conversation history
 */
export async function getConversationHistory(
  userId: string,
  conversationId: number,
  token?: string
): Promise<ChatMessage[]> {
  const apiUrl = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000";

  const headers: HeadersInit = {
    "Content-Type": "application/json",
  };

  const authToken = token || getAuthToken();
  if (authToken) {
    headers["Authorization"] = `Bearer ${authToken}`;
  }

  const response = await fetch(`${apiUrl}/api/${userId}/conversations/${conversationId}/messages`, {
    method: "GET",
    headers,
    credentials: "include",
  });

  if (!response.ok) {
    throw new Error(`Failed to load conversation history: ${response.status}`);
  }

  const data = await response.json();

  return data.messages?.map((msg: any) => ({
    role: msg.role,
    content: msg.content,
    timestamp: new Date(msg.created_at),
  })) || [];
}

/**
 * Get authentication token from localStorage
 */
export function getAuthToken(): string | null {
  if (typeof window === "undefined") return null;
  return localStorage.getItem("auth_token");
}

/**
 * Get current user ID from JWT token
 */
export function getCurrentUserId(): string {
  const token = getAuthToken();

  if (!token) {
    return "demo-user";
  }

  try {
    const payload = JSON.parse(atob(token.split(".")[1]));
    return payload.sub || "demo-user";
  } catch {
    return "demo-user";
  }
}

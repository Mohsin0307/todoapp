/**
 * Event streaming service for real-time todo updates.
 * Connects to the backend event stream for live notifications.
 */

const API_URL = process.env["NEXT_PUBLIC_API_URL"] || "http://localhost:8000";

export interface TodoEvent {
  id: string;
  type: string;
  source: string;
  timestamp: string;
  payload: Record<string, unknown>;
  userId?: string;
  todoId?: string;
}

type EventHandler = (event: TodoEvent) => void;

export class EventStreamingService {
  private handlers: Map<string, EventHandler[]> = new Map();
  private pollingInterval: ReturnType<typeof setInterval> | null = null;

  on(eventType: string, handler: EventHandler) {
    const existing = this.handlers.get(eventType) || [];
    existing.push(handler);
    this.handlers.set(eventType, existing);
  }

  off(eventType: string, handler: EventHandler) {
    const existing = this.handlers.get(eventType) || [];
    this.handlers.set(
      eventType,
      existing.filter((h) => h !== handler)
    );
  }

  startPolling(intervalMs = 5000) {
    if (this.pollingInterval) return;
    this.pollingInterval = setInterval(async () => {
      try {
        const res = await fetch(`${API_URL}/api/events/health/dapr`);
        if (res.ok) {
          const data = await res.json();
          if (data.dapr_healthy) {
            this.emit("dapr.connected", {
              id: "health",
              type: "dapr.connected",
              source: "frontend",
              timestamp: new Date().toISOString(),
              payload: {},
            });
          }
        }
      } catch {
        // Dapr not available
      }
    }, intervalMs);
  }

  stopPolling() {
    if (this.pollingInterval) {
      clearInterval(this.pollingInterval);
      this.pollingInterval = null;
    }
  }

  private emit(eventType: string, event: TodoEvent) {
    const handlers = this.handlers.get(eventType) || [];
    const wildcardHandlers = this.handlers.get("*") || [];
    [...handlers, ...wildcardHandlers].forEach((h) => h(event));
  }
}

export const eventStreaming = new EventStreamingService();

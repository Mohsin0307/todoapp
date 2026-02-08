"use client";

import { useState } from "react";
import { TodoItem, todoApi, UpdateTodoRequest } from "@/lib/todo-api";

interface Props {
  todo: TodoItem;
  onUpdate: () => void;
  onDelete: () => void;
}

const priorityColors: Record<string, string> = {
  low: "bg-gray-100 text-gray-700",
  medium: "bg-blue-100 text-blue-700",
  high: "bg-orange-100 text-orange-700",
  urgent: "bg-red-100 text-red-700",
};

const statusColors: Record<string, string> = {
  pending: "bg-yellow-100 text-yellow-800",
  in_progress: "bg-blue-100 text-blue-800",
  completed: "bg-green-100 text-green-800",
  cancelled: "bg-gray-100 text-gray-800",
};

export default function AdvancedTodoItem({ todo, onUpdate, onDelete }: Props) {
  const [loading, setLoading] = useState(false);

  const handleStatusChange = async (newStatus: string) => {
    setLoading(true);
    try {
      await todoApi.update(todo.id, { status: newStatus });
      onUpdate();
    } catch (err) {
      console.error("Failed to update status:", err);
    } finally {
      setLoading(false);
    }
  };

  const handleDelete = async () => {
    setLoading(true);
    try {
      await todoApi.delete(todo.id);
      onDelete();
    } catch (err) {
      console.error("Failed to delete:", err);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className={`border rounded-lg p-4 mb-3 ${todo.status === "completed" ? "opacity-60" : ""}`}>
      <div className="flex items-start justify-between">
        <div className="flex-1">
          <div className="flex items-center gap-2 mb-1">
            <h3 className={`font-medium ${todo.status === "completed" ? "line-through" : ""}`}>
              {todo.title}
            </h3>
            <span className={`text-xs px-2 py-0.5 rounded ${priorityColors[todo.priority] || ""}`}>
              {todo.priority}
            </span>
            <span className={`text-xs px-2 py-0.5 rounded ${statusColors[todo.status] || ""}`}>
              {todo.status}
            </span>
            {todo.is_recurring && (
              <span className="text-xs px-2 py-0.5 rounded bg-purple-100 text-purple-700">
                recurring
              </span>
            )}
          </div>
          {todo.description && <p className="text-sm text-gray-600 mb-2">{todo.description}</p>}
          <div className="flex items-center gap-3 text-xs text-gray-500">
            {todo.due_date && <span>Due: {new Date(todo.due_date).toLocaleDateString()}</span>}
            {todo.tags && todo.tags.length > 0 && (
              <div className="flex gap-1">
                {todo.tags.map((tag) => (
                  <span key={tag} className="bg-gray-200 px-1.5 py-0.5 rounded">
                    {tag}
                  </span>
                ))}
              </div>
            )}
            {todo.reminder_enabled && <span>Reminder on</span>}
          </div>
        </div>
        <div className="flex items-center gap-1 ml-4">
          {todo.status === "pending" && (
            <button
              onClick={() => handleStatusChange("in_progress")}
              disabled={loading}
              className="text-xs px-2 py-1 bg-blue-500 text-white rounded hover:bg-blue-600"
            >
              Start
            </button>
          )}
          {todo.status === "in_progress" && (
            <button
              onClick={() => handleStatusChange("completed")}
              disabled={loading}
              className="text-xs px-2 py-1 bg-green-500 text-white rounded hover:bg-green-600"
            >
              Complete
            </button>
          )}
          <button
            onClick={handleDelete}
            disabled={loading}
            className="text-xs px-2 py-1 bg-red-500 text-white rounded hover:bg-red-600"
          >
            Delete
          </button>
        </div>
      </div>
    </div>
  );
}

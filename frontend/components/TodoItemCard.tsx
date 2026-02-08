"use client";

import { TodoItem, updateTodo, deleteTodo } from "@/lib/todo-api";

interface Props {
  todo: TodoItem;
  onUpdate: () => void;
}

const priorityColors: Record<string, string> = {
  low: "bg-gray-100 text-gray-700",
  medium: "bg-blue-100 text-blue-700",
  high: "bg-orange-100 text-orange-700",
  urgent: "bg-red-100 text-red-700",
};

const statusColors: Record<string, string> = {
  pending: "bg-yellow-100 text-yellow-700",
  in_progress: "bg-blue-100 text-blue-700",
  completed: "bg-green-100 text-green-700",
  cancelled: "bg-gray-100 text-gray-500",
};

export default function TodoItemCard({ todo, onUpdate }: Props) {
  const handleToggleStatus = async () => {
    const nextStatus = todo.status === "completed" ? "pending" : "completed";
    await updateTodo(todo.id, { status: nextStatus });
    onUpdate();
  };

  const handleDelete = async () => {
    await deleteTodo(todo.id);
    onUpdate();
  };

  const tags = todo.tags || [];

  return (
    <div className="border rounded-lg p-4 mb-3 bg-white shadow-sm hover:shadow-md transition-shadow">
      <div className="flex items-start justify-between">
        <div className="flex items-start gap-3 flex-1">
          <button
            onClick={handleToggleStatus}
            className={`mt-1 w-5 h-5 rounded border-2 flex-shrink-0 ${
              todo.status === "completed"
                ? "bg-green-500 border-green-500"
                : "border-gray-300"
            }`}
          />
          <div className="flex-1">
            <h3
              className={`font-medium ${
                todo.status === "completed" ? "line-through text-gray-400" : ""
              }`}
            >
              {todo.title}
            </h3>
            {todo.description && (
              <p className="text-sm text-gray-500 mt-1">{todo.description}</p>
            )}
            <div className="flex flex-wrap gap-2 mt-2">
              <span
                className={`text-xs px-2 py-0.5 rounded ${
                  priorityColors[todo.priority] || ""
                }`}
              >
                {todo.priority}
              </span>
              <span
                className={`text-xs px-2 py-0.5 rounded ${
                  statusColors[todo.status] || ""
                }`}
              >
                {todo.status}
              </span>
              {todo.due_date && (
                <span className="text-xs px-2 py-0.5 rounded bg-purple-100 text-purple-700">
                  Due: {new Date(todo.due_date).toLocaleDateString()}
                </span>
              )}
              {todo.is_recurring && (
                <span className="text-xs px-2 py-0.5 rounded bg-indigo-100 text-indigo-700">
                  Recurring: {todo.recurrence_pattern}
                </span>
              )}
              {todo.reminder_enabled && (
                <span className="text-xs px-2 py-0.5 rounded bg-pink-100 text-pink-700">
                  Reminder
                </span>
              )}
              {tags.map((tag) => (
                <span
                  key={tag}
                  className="text-xs px-2 py-0.5 rounded bg-gray-200 text-gray-600"
                >
                  #{tag}
                </span>
              ))}
            </div>
          </div>
        </div>
        <button
          onClick={handleDelete}
          className="text-gray-400 hover:text-red-500 ml-2"
          title="Delete"
        >
          &times;
        </button>
      </div>
    </div>
  );
}

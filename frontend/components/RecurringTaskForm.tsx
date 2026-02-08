"use client";

import { useState } from "react";
import { fetchRecurringTodos, generateRecurringInstance, TodoItem } from "@/lib/todo-api";
import { useEffect } from "react";

export default function RecurringTaskForm() {
  const [recurringTodos, setRecurringTodos] = useState<TodoItem[]>([]);
  const [loading, setLoading] = useState(true);

  const loadRecurring = async () => {
    setLoading(true);
    try {
      const data = await fetchRecurringTodos();
      setRecurringTodos(data);
    } catch {
      // API may not be available
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    loadRecurring();
  }, []);

  const handleGenerate = async (todoId: string) => {
    try {
      await generateRecurringInstance(todoId);
      loadRecurring();
    } catch (err) {
      console.error("Failed to generate instance:", err);
    }
  };

  if (loading) {
    return <div className="text-gray-500 text-sm py-4">Loading recurring tasks...</div>;
  }

  if (recurringTodos.length === 0) {
    return (
      <div className="text-gray-400 text-sm py-4">
        No recurring tasks. Create a todo with the "Recurring" option enabled.
      </div>
    );
  }

  return (
    <div className="space-y-3">
      <h3 className="text-sm font-semibold text-gray-700">Recurring Tasks</h3>
      {recurringTodos.map((todo) => (
        <div key={todo.id} className="border rounded-lg p-3 bg-white flex items-center justify-between">
          <div>
            <div className="font-medium text-sm">{todo.title}</div>
            <div className="text-xs text-gray-500">
              {todo.recurrence_pattern} / every {todo.recurrence_interval || 1}
            </div>
          </div>
          <button
            onClick={() => handleGenerate(todo.id)}
            className="text-xs px-3 py-1 bg-indigo-500 text-white rounded hover:bg-indigo-600"
          >
            Generate Next
          </button>
        </div>
      ))}
    </div>
  );
}

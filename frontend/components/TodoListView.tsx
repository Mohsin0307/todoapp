"use client";

import { useEffect, useState } from "react";
import { TodoItem, fetchTodos } from "@/lib/todo-api";
import TodoItemCard from "./TodoItemCard";
import TodoFilterBar from "./TodoFilterBar";

export default function TodoListView() {
  const [todos, setTodos] = useState<TodoItem[]>([]);
  const [statusFilter, setStatusFilter] = useState<string>("");
  const [priorityFilter, setPriorityFilter] = useState<string>("");
  const [loading, setLoading] = useState(true);

  const loadTodos = async () => {
    setLoading(true);
    try {
      const data = await fetchTodos(
        statusFilter || undefined,
        priorityFilter || undefined
      );
      setTodos(data);
    } catch (err) {
      console.error("Failed to load todos:", err);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    loadTodos();
  }, [statusFilter, priorityFilter]);

  return (
    <div>
      <TodoFilterBar
        statusFilter={statusFilter}
        priorityFilter={priorityFilter}
        onStatusChange={setStatusFilter}
        onPriorityChange={setPriorityFilter}
      />
      {loading ? (
        <div className="text-center py-8 text-gray-500">Loading todos...</div>
      ) : todos.length === 0 ? (
        <div className="text-center py-8 text-gray-400">
          No todos found. Create one to get started!
        </div>
      ) : (
        <div className="mt-4">
          {todos.map((todo) => (
            <TodoItemCard key={todo.id} todo={todo} onUpdate={loadTodos} />
          ))}
        </div>
      )}
    </div>
  );
}

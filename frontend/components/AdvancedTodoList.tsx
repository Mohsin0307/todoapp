"use client";

import { useEffect, useState } from "react";
import { TodoItem, fetchTodos as fetchTodosApi } from "@/lib/todo-api";
import AdvancedTodoItem from "./AdvancedTodoItem";
import TodoFilter from "./TodoFilter";

export default function AdvancedTodoList() {
  const [todos, setTodos] = useState<TodoItem[]>([]);
  const [loading, setLoading] = useState(true);
  const [filters, setFilters] = useState<{ status?: string | undefined; priority?: string | undefined }>({});

  const fetchTodos = async () => {
    setLoading(true);
    try {
      const data = await fetchTodosApi(filters.status, filters.priority);
      setTodos(data);
    } catch (err) {
      console.error("Failed to fetch todos:", err);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchTodos();
  }, [filters]);

  if (loading) {
    return <div className="text-center py-8 text-gray-500">Loading todos...</div>;
  }

  return (
    <div>
      <TodoFilter filters={filters} onFilterChange={setFilters} />
      {todos.length === 0 ? (
        <div className="text-center py-8 text-gray-500">
          No todos found. Create your first one!
        </div>
      ) : (
        <div className="mt-4">
          {todos.map((todo) => (
            <AdvancedTodoItem
              key={todo.id}
              todo={todo}
              onUpdate={fetchTodos}
              onDelete={fetchTodos}
            />
          ))}
        </div>
      )}
    </div>
  );
}

"use client";

import TodoListView from "@/components/TodoListView";
import TodoCreateForm from "@/components/TodoCreateForm";
import NotificationPanel from "@/components/NotificationPanel";
import { useState } from "react";

export default function TodoManagerPage() {
  const [refreshKey, setRefreshKey] = useState(0);

  return (
    <div className="min-h-screen bg-gray-50">
      <header className="bg-white shadow-sm border-b">
        <div className="max-w-4xl mx-auto px-4 py-4 flex items-center justify-between">
          <h1 className="text-xl font-bold text-gray-800">Todo Manager</h1>
          <div className="flex items-center gap-3">
            <NotificationPanel />
            <a href="/" className="text-sm text-blue-500 hover:text-blue-700">
              Home
            </a>
          </div>
        </div>
      </header>
      <main className="max-w-4xl mx-auto px-4 py-6">
        <TodoCreateForm
          key={`form-${refreshKey}`}
          onCreated={() => setRefreshKey((k) => k + 1)}
        />
        <div className="mt-4">
          <TodoListView key={`list-${refreshKey}`} />
        </div>
      </main>
    </div>
  );
}

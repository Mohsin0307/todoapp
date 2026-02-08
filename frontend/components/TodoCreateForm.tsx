"use client";

import { useState } from "react";
import { createTodo, CreateTodoRequest } from "@/lib/todo-api";

interface Props {
  onCreated: () => void;
}

export default function TodoCreateForm({ onCreated }: Props) {
  const [isOpen, setIsOpen] = useState(false);
  const [title, setTitle] = useState("");
  const [description, setDescription] = useState("");
  const [priority, setPriority] = useState("medium");
  const [dueDate, setDueDate] = useState("");
  const [tags, setTags] = useState("");
  const [isRecurring, setIsRecurring] = useState(false);
  const [recurrencePattern, setRecurrencePattern] = useState("daily");
  const [recurrenceInterval, setRecurrenceInterval] = useState(1);
  const [reminderEnabled, setReminderEnabled] = useState(false);
  const [reminderHours, setReminderHours] = useState(1);
  const [submitting, setSubmitting] = useState(false);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!title.trim()) return;
    setSubmitting(true);
    try {
      const data: CreateTodoRequest = {
        title: title.trim(),
        priority,
        is_recurring: isRecurring,
        reminder_enabled: reminderEnabled,
        ...(description.trim() ? { description: description.trim() } : {}),
        ...(dueDate ? { due_date: dueDate } : {}),
        ...(tags ? { tags: tags.split(",").map((t) => t.trim()).filter(Boolean) } : {}),
        ...(isRecurring ? { recurrence_pattern: recurrencePattern, recurrence_interval: recurrenceInterval } : {}),
        ...(reminderEnabled ? { reminder_offset_hours: reminderHours } : {}),
      };
      await createTodo(data);
      setTitle("");
      setDescription("");
      setPriority("medium");
      setDueDate("");
      setTags("");
      setIsRecurring(false);
      setReminderEnabled(false);
      setIsOpen(false);
      onCreated();
    } catch (err) {
      console.error("Failed to create todo:", err);
    } finally {
      setSubmitting(false);
    }
  };

  if (!isOpen) {
    return (
      <button
        onClick={() => setIsOpen(true)}
        className="w-full py-3 border-2 border-dashed border-gray-300 rounded-lg text-gray-500 hover:border-blue-400 hover:text-blue-500 transition-colors"
      >
        + Add New Todo
      </button>
    );
  }

  return (
    <form onSubmit={handleSubmit} className="border rounded-lg p-4 bg-white shadow-sm mb-4">
      <div className="grid gap-3">
        <input
          type="text"
          placeholder="Todo title..."
          value={title}
          onChange={(e) => setTitle(e.target.value)}
          className="border rounded px-3 py-2 w-full"
          required
        />
        <textarea
          placeholder="Description (optional)"
          value={description}
          onChange={(e) => setDescription(e.target.value)}
          className="border rounded px-3 py-2 w-full"
          rows={2}
        />
        <div className="grid grid-cols-2 gap-3">
          <div>
            <label className="text-xs text-gray-500">Priority</label>
            <select
              value={priority}
              onChange={(e) => setPriority(e.target.value)}
              className="border rounded px-3 py-2 w-full"
            >
              <option value="low">Low</option>
              <option value="medium">Medium</option>
              <option value="high">High</option>
              <option value="urgent">Urgent</option>
            </select>
          </div>
          <div>
            <label className="text-xs text-gray-500">Due Date</label>
            <input
              type="date"
              value={dueDate}
              onChange={(e) => setDueDate(e.target.value)}
              className="border rounded px-3 py-2 w-full"
            />
          </div>
        </div>
        <input
          type="text"
          placeholder="Tags (comma-separated)"
          value={tags}
          onChange={(e) => setTags(e.target.value)}
          className="border rounded px-3 py-2 w-full"
        />
        <div className="flex gap-4">
          <label className="flex items-center gap-2 text-sm">
            <input
              type="checkbox"
              checked={isRecurring}
              onChange={(e) => setIsRecurring(e.target.checked)}
            />
            Recurring
          </label>
          <label className="flex items-center gap-2 text-sm">
            <input
              type="checkbox"
              checked={reminderEnabled}
              onChange={(e) => setReminderEnabled(e.target.checked)}
            />
            Reminder
          </label>
        </div>
        {isRecurring && (
          <div className="grid grid-cols-2 gap-3">
            <div>
              <label className="text-xs text-gray-500">Pattern</label>
              <select
                value={recurrencePattern}
                onChange={(e) => setRecurrencePattern(e.target.value)}
                className="border rounded px-3 py-2 w-full"
              >
                <option value="daily">Daily</option>
                <option value="weekly">Weekly</option>
                <option value="monthly">Monthly</option>
                <option value="yearly">Yearly</option>
              </select>
            </div>
            <div>
              <label className="text-xs text-gray-500">Every N</label>
              <input
                type="number"
                min={1}
                value={recurrenceInterval}
                onChange={(e) => setRecurrenceInterval(Number(e.target.value))}
                className="border rounded px-3 py-2 w-full"
              />
            </div>
          </div>
        )}
        {reminderEnabled && (
          <div>
            <label className="text-xs text-gray-500">Remind hours before due</label>
            <input
              type="number"
              min={1}
              value={reminderHours}
              onChange={(e) => setReminderHours(Number(e.target.value))}
              className="border rounded px-3 py-2 w-full"
            />
          </div>
        )}
      </div>
      <div className="flex justify-end gap-2 mt-4">
        <button
          type="button"
          onClick={() => setIsOpen(false)}
          className="px-4 py-2 text-sm text-gray-600 hover:text-gray-800"
        >
          Cancel
        </button>
        <button
          type="submit"
          disabled={submitting || !title.trim()}
          className="px-4 py-2 text-sm bg-blue-500 text-white rounded hover:bg-blue-600 disabled:opacity-50"
        >
          {submitting ? "Creating..." : "Create Todo"}
        </button>
      </div>
    </form>
  );
}

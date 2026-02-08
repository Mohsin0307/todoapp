"use client";

interface Props {
  statusFilter: string;
  priorityFilter: string;
  onStatusChange: (val: string) => void;
  onPriorityChange: (val: string) => void;
}

export default function TodoFilterBar({
  statusFilter,
  priorityFilter,
  onStatusChange,
  onPriorityChange,
}: Props) {
  return (
    <div className="flex flex-wrap gap-3 items-center">
      <div>
        <label className="text-sm text-gray-600 mr-1">Status:</label>
        <select
          value={statusFilter}
          onChange={(e) => onStatusChange(e.target.value)}
          className="border rounded px-2 py-1 text-sm"
        >
          <option value="">All</option>
          <option value="pending">Pending</option>
          <option value="in_progress">In Progress</option>
          <option value="completed">Completed</option>
          <option value="cancelled">Cancelled</option>
        </select>
      </div>
      <div>
        <label className="text-sm text-gray-600 mr-1">Priority:</label>
        <select
          value={priorityFilter}
          onChange={(e) => onPriorityChange(e.target.value)}
          className="border rounded px-2 py-1 text-sm"
        >
          <option value="">All</option>
          <option value="low">Low</option>
          <option value="medium">Medium</option>
          <option value="high">High</option>
          <option value="urgent">Urgent</option>
        </select>
      </div>
    </div>
  );
}

"use client";

interface FilterState {
  status?: string | undefined;
  priority?: string | undefined;
}

interface Props {
  filters: FilterState;
  onFilterChange: (filters: FilterState) => void;
}

const statuses = ["", "pending", "in_progress", "completed", "cancelled"];
const priorities = ["", "low", "medium", "high", "urgent"];

export default function TodoFilter({ filters, onFilterChange }: Props) {
  return (
    <div className="flex gap-4 items-center flex-wrap">
      <div className="flex items-center gap-2">
        <label className="text-sm font-medium text-gray-700">Status:</label>
        <select
          value={filters.status || ""}
          onChange={(e) => onFilterChange({ ...filters, status: e.target.value || undefined })}
          className="text-sm border rounded px-2 py-1"
        >
          {statuses.map((s) => (
            <option key={s} value={s}>
              {s || "All"}
            </option>
          ))}
        </select>
      </div>
      <div className="flex items-center gap-2">
        <label className="text-sm font-medium text-gray-700">Priority:</label>
        <select
          value={filters.priority || ""}
          onChange={(e) => onFilterChange({ ...filters, priority: e.target.value || undefined })}
          className="text-sm border rounded px-2 py-1"
        >
          {priorities.map((p) => (
            <option key={p} value={p}>
              {p || "All"}
            </option>
          ))}
        </select>
      </div>
    </div>
  );
}

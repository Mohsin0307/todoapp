"use client";

interface Props {
  enabled: boolean;
  offsetHours: number;
  onToggle: (enabled: boolean) => void;
  onChangeHours: (hours: number) => void;
}

export default function ReminderSettings({
  enabled,
  offsetHours,
  onToggle,
  onChangeHours,
}: Props) {
  return (
    <div className="border rounded-lg p-3 bg-white">
      <div className="flex items-center justify-between">
        <label className="text-sm font-medium text-gray-700">Reminders</label>
        <button
          onClick={() => onToggle(!enabled)}
          className={`relative inline-flex h-6 w-11 items-center rounded-full transition-colors ${
            enabled ? "bg-blue-500" : "bg-gray-300"
          }`}
        >
          <span
            className={`inline-block h-4 w-4 transform rounded-full bg-white transition-transform ${
              enabled ? "translate-x-6" : "translate-x-1"
            }`}
          />
        </button>
      </div>
      {enabled && (
        <div className="mt-3">
          <label className="text-xs text-gray-500">Remind me before due date</label>
          <div className="flex items-center gap-2 mt-1">
            <input
              type="number"
              min={1}
              max={168}
              value={offsetHours}
              onChange={(e) => onChangeHours(Number(e.target.value))}
              className="border rounded px-2 py-1 w-20 text-sm"
            />
            <span className="text-sm text-gray-600">hours before</span>
          </div>
        </div>
      )}
    </div>
  );
}

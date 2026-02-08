import ChatInterface from "@/components/ChatInterface";

export default function ChatPage() {
  return (
    <div className="min-h-screen bg-gray-50 p-4">
      <div className="max-w-4xl mx-auto h-[calc(100vh-2rem)]">
        <div className="bg-white rounded-lg shadow-lg overflow-hidden h-full flex flex-col">
          <ChatInterface />
        </div>

        {/* Setup Instructions */}
        <div className="mt-4 bg-yellow-50 border border-yellow-200 rounded-lg p-4">
          <h3 className="font-bold text-yellow-800 mb-2">Setup Instructions</h3>
          <ol className="text-sm text-yellow-700 space-y-1 list-decimal list-inside">
            <li>Backend: <code className="bg-yellow-100 px-1 rounded">cd backend && uvicorn main:app --reload --port 8000</code></li>
            <li>Add OpenAI API key to <code className="bg-yellow-100 px-1 rounded">backend/.env</code></li>
            <li>Run migrations: <code className="bg-yellow-100 px-1 rounded">python -m alembic upgrade head</code></li>
            <li>Restart backend to enable full AI chat</li>
          </ol>
        </div>
      </div>
    </div>
  );
}

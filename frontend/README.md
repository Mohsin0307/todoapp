# Frontend - AI-Powered Todo App

**Phase III**: AI Chatbot Interface with Claude
**Tech Stack**: Next.js 16, React 19, TypeScript, Tailwind CSS, Better Auth

---

## 🚀 Quick Start

### Prerequisites

- Node.js 20+
- npm or yarn
- Backend server running (see `../backend/README.md`)

### Installation

```bash
# Install dependencies
npm install

# Run development server
npm run dev

# Build for production
npm run build
npm start
```

### Configuration

Create `.env.local` file:

```bash
# Better Auth (from Phase II)
BETTER_AUTH_URL=http://localhost:3000
BETTER_AUTH_SECRET=your-secret-key-min-32-chars

# Backend API
NEXT_PUBLIC_API_URL=http://localhost:8000
```

---

## 📁 Project Structure

```
frontend/
├── app/
│   ├── layout.tsx            # Root layout
│   ├── page.tsx              # Home page
│   ├── auth/                 # Authentication pages
│   ├── tasks/                # Task management UI
│   └── chat/                 # AI Chat Interface (Phase III)
│       └── page.tsx          # Chat page
├── components/               # Reusable components
│   ├── ui/                   # UI primitives
│   └── ...
├── lib/                      # Utilities
│   ├── auth.ts              # Better Auth configuration
│   └── chat-api.ts          # Chat API client (Phase III)
├── public/                   # Static assets
├── package.json
└── tailwind.config.ts
```

---

## 💬 Phase III: Chat Interface

### Chat Page Documentation

The chat interface is located at `/chat` route (`app/chat/page.tsx`).

**Features**:
- Real-time messaging with Claude AI
- Message history display
- Loading states and error handling
- Responsive design
- Markdown support for AI responses

**Usage**:
1. Navigate to http://localhost:3000/chat
2. Type a message in the input field
3. Press Enter or click Send
4. AI responds with task management assistance

**Example Interactions**:
```
User: "Add a task to buy groceries"
AI: "✅ Created task: Buy groceries"

User: "Show my pending tasks"
AI: "You have 3 pending tasks:
1. Buy groceries
2. Call dentist
3. Finish report"

User: "Mark buy groceries as done"
AI: "✅ Marked 'Buy groceries' as complete"
```

### Chat Component Structure

```typescript
// app/chat/page.tsx
interface Message {
  role: "user" | "assistant";
  content: string;
  timestamp: Date;
}

const [messages, setMessages] = useState<Message[]>([]);
const [input, setInput] = useState("");
const [loading, setLoading] = useState(false);

const handleSubmit = async (e: React.FormEvent) => {
  // Send message to backend
  const response = await fetch("http://localhost:8001/api/demo-user/chat", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({
      message: input,
      conversation_id: null
    })
  });

  const data = await response.json();
  // Display AI response
};
```

### API Integration Guide

#### Chat API Client

Location: `lib/chat-api.ts` (to be created)

```typescript
export interface ChatRequest {
  message: string;
  conversation_id?: number;
}

export interface ChatResponse {
  conversation_id: number;
  response: string;
  created_at: string;
  tools_used?: string[];
}

export async function sendChatMessage(
  userId: string,
  request: ChatRequest,
  token?: string
): Promise<ChatResponse> {
  const response = await fetch(
    `${process.env.NEXT_PUBLIC_API_URL}/api/${userId}/chat`,
    {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
        ...(token && { Authorization: `Bearer ${token}` })
      },
      body: JSON.stringify(request)
    }
  );

  if (!response.ok) {
    throw new Error(`Chat API error: ${response.status}`);
  }

  return response.json();
}
```

#### Authentication Integration

```typescript
// Get JWT token from Better Auth
import { auth } from "@/lib/auth";

const session = await auth();
const token = session?.accessToken;

// Pass token to chat API
const response = await sendChatMessage(
  session.user.id,
  { message: userInput },
  token
);
```

### Styling and Theming

**Tailwind Classes**:
```tsx
{/* Chat container */}
<div className="min-h-screen bg-gray-50 p-4">

  {/* Messages area */}
  <div className="max-w-4xl mx-auto bg-white rounded-lg shadow-lg">

    {/* User message */}
    <div className="flex justify-end mb-4">
      <div className="bg-blue-500 text-white rounded-lg px-4 py-2">
        {message.content}
      </div>
    </div>

    {/* AI message */}
    <div className="flex justify-start mb-4">
      <div className="bg-gray-200 text-gray-900 rounded-lg px-4 py-2">
        {message.content}
      </div>
    </div>
  </div>
</div>
```

### Error Handling

```typescript
try {
  const response = await sendChatMessage(userId, { message: input });
  setMessages(prev => [...prev, {
    role: "assistant",
    content: response.response,
    timestamp: new Date(response.created_at)
  }]);
} catch (error) {
  // Display error message
  setMessages(prev => [...prev, {
    role: "assistant",
    content: "❌ Error: Could not connect to backend. " +
             "Make sure the server is running on port 8001.",
    timestamp: new Date()
  }]);
}
```

---

## 🔧 Environment Variables

### Required

| Variable | Description | Example |
|----------|-------------|---------|
| `BETTER_AUTH_SECRET` | Secret for Better Auth (min 32 chars) | `your-secret-key-here` |
| `NEXT_PUBLIC_API_URL` | Backend API base URL | `http://localhost:8000` |

### Optional

| Variable | Description | Default |
|----------|-------------|---------|
| `BETTER_AUTH_URL` | Frontend URL for auth | `http://localhost:3000` |
| `NODE_ENV` | Environment mode | `development` |

---

## 🎨 Component Library

### UI Components (Shadcn/ui)

The project uses Shadcn/ui for UI primitives:

```bash
# Add new components
npx shadcn-ui@latest add button
npx shadcn-ui@latest add card
npx shadcn-ui@latest add input
```

**Available Components**:
- Button
- Card
- Input
- Dialog
- Toast
- Loading Spinner

### Custom Components

**MessageList** (to be created):
```typescript
// components/MessageList.tsx
interface MessageListProps {
  messages: Message[];
}

export function MessageList({ messages }: MessageListProps) {
  return (
    <div className="space-y-4 p-4 overflow-y-auto max-h-[60vh]">
      {messages.map((msg, idx) => (
        <MessageBubble key={idx} message={msg} />
      ))}
    </div>
  );
}
```

**ChatInput** (to be created):
```typescript
// components/ChatInput.tsx
interface ChatInputProps {
  onSubmit: (message: string) => void;
  loading?: boolean;
}

export function ChatInput({ onSubmit, loading }: ChatInputProps) {
  const [input, setInput] = useState("");

  return (
    <form onSubmit={(e) => {
      e.preventDefault();
      onSubmit(input);
      setInput("");
    }}>
      <input
        type="text"
        value={input}
        onChange={(e) => setInput(e.target.value)}
        disabled={loading}
        placeholder="Type a message..."
        className="w-full px-4 py-2 border rounded-lg"
      />
    </form>
  );
}
```

---

## 🧪 Testing

```bash
# Run unit tests
npm test

# Run end-to-end tests
npm run test:e2e

# Run with coverage
npm run test:coverage
```

---

## 🐛 Troubleshooting

### Backend Connection Error

**Symptom**: "Could not connect to backend"

**Solutions**:
1. Verify backend is running: http://localhost:8001/api/health
2. Check `NEXT_PUBLIC_API_URL` in `.env.local`
3. Ensure CORS is configured in backend
4. Check browser console for detailed errors

### Authentication Errors

**Symptom**: 401 Unauthorized

**Solutions**:
1. Verify Better Auth is configured
2. Check JWT token is being sent
3. Test auth endpoints: http://localhost:3000/api/auth/session
4. Clear browser cookies and re-login

### Styling Not Applied

**Symptom**: Components appear unstyled

**Solutions**:
```bash
# Rebuild Tailwind
npm run dev

# Check tailwind.config.ts includes all paths
content: [
  "./app/**/*.{ts,tsx}",
  "./components/**/*.{ts,tsx}",
]

# Clear Next.js cache
rm -rf .next
npm run dev
```

### Port Already in Use

**Symptom**: "Port 3000 is already in use"

**Solutions**:
```bash
# Kill process on port 3000
# Windows
netstat -ano | findstr :3000
taskkill /PID <PID> /F

# Linux/Mac
lsof -i :3000
kill -9 <PID>

# OR use different port
npm run dev -- -p 3001
```

---

## 📦 Dependencies

Key dependencies:

- **Next.js** (16.x): React framework
- **React** (19.x): UI library
- **TypeScript** (5.x): Type safety
- **Tailwind CSS** (3.x): Styling
- **Better Auth**: Authentication
- **Shadcn/ui**: UI components

See `package.json` for full list.

---

## 🚢 Deployment

### Vercel Deployment (Recommended)

```bash
# Install Vercel CLI
npm i -g vercel

# Deploy
vercel

# Set environment variables in Vercel dashboard:
# - BETTER_AUTH_SECRET
# - NEXT_PUBLIC_API_URL (production backend URL)
```

### Docker Deployment

```bash
# Build Docker image
docker build -t todo-frontend .

# Run container
docker run -p 3000:3000 \
  -e NEXT_PUBLIC_API_URL=http://backend:8000 \
  todo-frontend
```

### Manual Deployment

```bash
# Build for production
npm run build

# Start production server
npm start

# Or use PM2 for process management
pm2 start npm --name "todo-frontend" -- start
```

---

## 📚 Additional Resources

- **Next.js Documentation**: https://nextjs.org/docs
- **React Documentation**: https://react.dev
- **Tailwind CSS**: https://tailwindcss.com/docs
- **Better Auth**: https://better-auth.dev

---

**For backend API documentation, see**: `../backend/README.md`
**For full project setup, see**: `../README.md`

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
- Conversation state management
- Message history loading from database
- JWT authentication with Better Auth
- Loading states with typing indicators
- Error handling with helpful messages
- Responsive design
- Auto-scroll to latest message

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
AI: "📋 Here are your pending tasks:
1. [#1] Buy groceries (pending)
2. [#2] Call dentist (pending)
3. [#3] Finish report (pending)"

User: "Mark buy groceries as done"
AI: "✅ Marked 'Buy groceries' as completed"

User: "How am I doing?"
AI: "📊 You're making great progress!

Total tasks: 10
Completed: 3 (30%)
Pending: 7

📅 Today: Created 2, Completed 1"
```

### Chat Component Architecture

The chat interface is built with three modular components:

```typescript
// app/chat/page.tsx - Minimal wrapper
import ChatInterface from "@/components/ChatInterface";

export default function ChatPage() {
  return <ChatInterface />;
}

// components/ChatInterface.tsx - Main controller
// - Manages conversation state (messages, conversation_id)
// - Handles API calls via chat-api.ts
// - Loads message history on mount
// - Integrates JWT authentication
// - Renders MessageList and ChatInput

// components/MessageList.tsx - Message display
// - Renders messages with proper styling
// - Auto-scrolls to latest message
// - Shows typing indicator during loading
// - Handles loading history state

// components/ChatInput.tsx - User input
// - Input field with submit button
// - Enter key support
// - Loading state management
// - Helpful tips display
```

### API Integration Guide

#### Chat API Client

Location: `lib/chat-api.ts`

The chat API client provides type-safe functions for communicating with the backend:

```typescript
import { sendChatMessage, getConversationHistory, getAuthToken, getCurrentUserId } from "@/lib/chat-api";

// Send a message to Claude AI
const response = await sendChatMessage(
  getCurrentUserId(),      // User ID (from JWT or "demo-user")
  "Add task to buy milk",  // User's message
  conversationId,          // Optional: continue existing conversation
  getAuthToken()           // Optional: JWT token for authentication
);

// Load previous conversation history
const messages = await getConversationHistory(
  getCurrentUserId(),
  conversationId,
  getAuthToken()
);
```

**Key Functions**:

- `sendChatMessage()` - Send user message and get AI response
- `getConversationHistory()` - Load past messages for a conversation
- `getAuthToken()` - Get JWT token from localStorage or Better Auth session
- `getCurrentUserId()` - Get user ID from JWT or default to "demo-user"

**Type Definitions**:

```typescript
export interface ChatMessage {
  role: "user" | "assistant";
  content: string;
  timestamp: Date;
}

export interface ChatRequest {
  message: string;
  conversation_id?: number | null;
}

export interface ChatResponse {
  conversation_id: number;
  response: string;
  created_at: string;
}
```

#### Authentication Integration

The chat API automatically handles authentication:

```typescript
// In demo mode (no auth):
// - Uses "demo-user" as userId
// - No JWT token sent

// In authenticated mode:
// - Decodes JWT token to get user_id
// - Includes "Authorization: Bearer <token>" header
// - Backend filters tasks by user_id from JWT
```

**Demo Mode**:
Chat works without authentication using "demo-user" as the default user ID. Perfect for testing!

**Production Mode**:
Integrate with Better Auth by storing JWT token in localStorage after login.

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

#### ChatInterface (`components/ChatInterface.tsx`)

Main controller component that manages chat state and orchestrates MessageList and ChatInput.

**Key Features**:
- Conversation state management (messages, conversationId)
- Message history loading from database
- JWT token integration
- Error handling with user-friendly messages
- Real-time message updates

**Props**:
```typescript
interface ChatInterfaceProps {
  initialMessage?: string;  // Optional welcome message override
}
```

#### MessageList (`components/MessageList.tsx`)

Displays chat messages with auto-scroll and loading indicators.

**Key Features**:
- Auto-scrolls to latest message
- Typing indicator animation during loading
- Loading history spinner
- Responsive message bubbles
- Timestamp display

**Props**:
```typescript
interface MessageListProps {
  messages: ChatMessage[];
  loading: boolean;
  isLoadingHistory?: boolean;
}
```

**Usage**:
```typescript
<MessageList
  messages={messages}
  loading={isAgentTyping}
  isLoadingHistory={isLoadingHistory}
/>
```

#### ChatInput (`components/ChatInput.tsx`)

User input field with submit button and helpful tips.

**Key Features**:
- Enter key submission support
- Loading state handling
- Input validation
- Helpful example prompts
- Disabled state during loading

**Props**:
```typescript
interface ChatInputProps {
  value: string;
  onChange: (value: string) => void;
  onSubmit: (e: React.FormEvent) => void;
  loading: boolean;
  placeholder?: string;
}
```

**Usage**:
```typescript
<ChatInput
  value={input}
  onChange={setInput}
  onSubmit={handleSubmit}
  loading={loading}
  placeholder="Type your message..."
/>
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

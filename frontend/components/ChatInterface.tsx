"use client";

import { useState, useEffect, useRef } from "react";
import { sendChatMessage, getConversationHistory, getAuthToken, getCurrentUserId, type ChatMessage } from "@/lib/chat-api";
import MessageList from "./MessageList";
import ChatInput from "./ChatInput";

interface ChatInterfaceProps {
  initialMessage?: string;
}

export default function ChatInterface({ initialMessage }: ChatInterfaceProps) {
  const [messages, setMessages] = useState<ChatMessage[]>([]);
  const [input, setInput] = useState("");
  const [loading, setLoading] = useState(false);
  const [conversationId, setConversationId] = useState<number | null>(null);
  const [error, setError] = useState<string | null>(null);
  const [isLoadingHistory, setIsLoadingHistory] = useState(false);

  const userId = useRef(getCurrentUserId());
  const token = useRef(getAuthToken());

  // Load conversation history on mount if conversationId exists
  useEffect(() => {
    const loadHistory = async () => {
      if (!conversationId) return;

      setIsLoadingHistory(true);
      try {
        const history = await getConversationHistory(
          userId.current,
          conversationId,
          token.current || undefined
        );
        setMessages(history);
      } catch (err) {
        console.error("Failed to load conversation history:", err);
        setError("Failed to load conversation history");
      } finally {
        setIsLoadingHistory(false);
      }
    };

    loadHistory();
  }, [conversationId]);

  // Add initial welcome message
  useEffect(() => {
    if (messages.length === 0 && !isLoadingHistory) {
      setMessages([
        {
          role: "assistant",
          content: initialMessage || "👋 Welcome to AI Todo Chatbot!\n\n**What I can do:**\n- ✅ Create tasks: \"Add a task to buy groceries\"\n- ✅ View tasks: \"Show my pending tasks\"\n- ✅ Update tasks: \"Mark buy groceries as done\"\n- ✅ Delete tasks: \"Delete the groceries task\"\n- ✅ Get stats: \"How am I doing today?\"\n\nType 'help' for more information!",
          timestamp: new Date(),
        },
      ]);
    }
  }, [messages.length, isLoadingHistory, initialMessage]);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!input.trim() || loading) return;

    const userMessage: ChatMessage = {
      role: "user",
      content: input,
      timestamp: new Date(),
    };

    setMessages((prev) => [...prev, userMessage]);
    setInput("");
    setLoading(true);
    setError(null);

    try {
      const response = await sendChatMessage(
        userId.current,
        input,
        conversationId,
        token.current || undefined
      );

      // Update conversation ID if this is the first message
      if (!conversationId) {
        setConversationId(response.conversation_id);
      }

      const assistantMessage: ChatMessage = {
        role: "assistant",
        content: response.response,
        timestamp: new Date(response.created_at),
      };

      setMessages((prev) => [...prev, assistantMessage]);
    } catch (err) {
      console.error("Chat error:", err);
      const errorMessage = err instanceof Error ? err.message : "Failed to send message";

      setError(errorMessage);

      const errorResponse: ChatMessage = {
        role: "assistant",
        content: `Error: ${errorMessage}\n\nMake sure:\n1. Backend server is running (port 8000)\n2. OPENAI_API_KEY is configured in backend/.env\n3. Database migrations are up to date`,
        timestamp: new Date(),
      };

      setMessages((prev) => [...prev, errorResponse]);
    } finally {
      setLoading(false);
    }
  };

  const handleInputChange = (value: string) => {
    setInput(value);
    setError(null); // Clear error when user starts typing
  };

  return (
    <div className="flex flex-col h-full">
      {/* Header */}
      <div className="bg-blue-600 text-white p-4 flex-shrink-0">
        <h1 className="text-2xl font-bold">🤖 AI Todo Chatbot</h1>
        <p className="text-blue-100 text-sm">
          Natural Language Task Management
          {conversationId && <span className="ml-2">• Conversation #{conversationId}</span>}
        </p>
      </div>

      {/* Error Banner */}
      {error && (
        <div className="bg-red-50 border-b border-red-200 p-3 flex-shrink-0">
          <p className="text-red-700 text-sm">
            ⚠️ {error}
          </p>
        </div>
      )}

      {/* Messages */}
      <div className="flex-1 overflow-hidden">
        <MessageList
          messages={messages}
          loading={loading}
          isLoadingHistory={isLoadingHistory}
        />
      </div>

      {/* Input */}
      <div className="flex-shrink-0 border-t">
        <ChatInput
          value={input}
          onChange={handleInputChange}
          onSubmit={handleSubmit}
          loading={loading}
          placeholder="Type your message... (e.g., 'add task to buy groceries')"
        />
      </div>
    </div>
  );
}

"use client";

import { useEffect, useRef } from "react";
import { type ChatMessage } from "@/lib/chat-api";

interface MessageListProps {
  messages: ChatMessage[];
  loading: boolean;
  isLoadingHistory?: boolean;
}

export default function MessageList({ messages, loading, isLoadingHistory = false }: MessageListProps) {
  const messagesEndRef = useRef<HTMLDivElement>(null);
  const containerRef = useRef<HTMLDivElement>(null);

  // Auto-scroll to bottom when new messages arrive
  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
  }, [messages, loading]);

  if (isLoadingHistory) {
    return (
      <div className="h-full flex items-center justify-center bg-gray-50">
        <div className="text-center">
          <div className="inline-block animate-spin rounded-full h-8 w-8 border-b-2 border-blue-600"></div>
          <p className="text-gray-600 mt-2">Loading conversation history...</p>
        </div>
      </div>
    );
  }

  return (
    <div
      ref={containerRef}
      className="h-full overflow-y-auto p-4 space-y-4 bg-gray-50"
    >
      {messages.map((message, index) => (
        <div
          key={index}
          className={`flex ${message.role === "user" ? "justify-end" : "justify-start"}`}
        >
          <div
            className={`max-w-[80%] rounded-lg p-3 shadow-sm ${
              message.role === "user"
                ? "bg-blue-500 text-white"
                : "bg-white text-gray-800 border border-gray-200"
            }`}
          >
            {/* Message Content */}
            <div className="whitespace-pre-wrap break-words">
              {message.content}
            </div>

            {/* Timestamp */}
            <div
              className={`text-xs mt-1 ${
                message.role === "user" ? "text-blue-100" : "text-gray-500"
              }`}
            >
              {message.timestamp.toLocaleTimeString([], {
                hour: "2-digit",
                minute: "2-digit",
              })}
            </div>
          </div>
        </div>
      ))}

      {/* Typing Indicator */}
      {loading && (
        <div className="flex justify-start">
          <div className="bg-white rounded-lg p-3 shadow-sm border border-gray-200">
            <div className="flex space-x-2">
              <div className="w-2 h-2 bg-gray-400 rounded-full animate-bounce"></div>
              <div
                className="w-2 h-2 bg-gray-400 rounded-full animate-bounce"
                style={{ animationDelay: "0.1s" }}
              ></div>
              <div
                className="w-2 h-2 bg-gray-400 rounded-full animate-bounce"
                style={{ animationDelay: "0.2s" }}
              ></div>
            </div>
          </div>
        </div>
      )}

      {/* Scroll anchor */}
      <div ref={messagesEndRef} />
    </div>
  );
}

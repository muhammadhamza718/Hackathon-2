"use client";

import React, { useState, useRef, useEffect } from "react";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Card } from "@/components/ui/card";
import { Send, Bot, User, Loader2, Sparkles } from "lucide-react";
import { apiClient } from "@/lib/api";
import { motion, AnimatePresence } from "framer-motion";
import { cn } from "@/lib/utils";

interface Message {
  id: string;
  role: "user" | "assistant";
  content: string;
  timestamp: Date;
}

export default function TodoChat() {
  const [messages, setMessages] = useState<Message[]>([
    {
      id: "welcome",
      role: "assistant",
      content:
        "Hello! I'm your AI Todo Assistant. How can I help you manage your tasks today?",
      timestamp: new Date(),
    },
  ]);
  const [inputValue, setInputValue] = useState("");
  const [isLoading, setIsLoading] = useState(false);
  const messagesEndRef = useRef<HTMLDivElement>(null);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  const handleSubmit = async (e?: React.FormEvent) => {
    e?.preventDefault();
    if (!inputValue.trim() || isLoading) return;

    const userMessage: Message = {
      id: Date.now().toString(),
      role: "user",
      content: inputValue,
      timestamp: new Date(),
    };

    setMessages((prev) => [...prev, userMessage]);
    setInputValue("");
    setIsLoading(true);

    try {
      const response = await apiClient.sendChatMessage(userMessage.content);

      const botMessage: Message = {
        id: (Date.now() + 1).toString(),
        role: "assistant",
        content: response.response,
        timestamp: new Date(),
      };

      setMessages((prev) => [...prev, botMessage]);
    } catch (error) {
      const errorMessage: Message = {
        id: (Date.now() + 1).toString(),
        role: "assistant",
        content:
          "Sorry, I encountered an error communicating with the server. Please try again.",
        timestamp: new Date(),
      };
      setMessages((prev) => [...prev, errorMessage]);
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <Card className="glass border-white/60 shadow-xl overflow-hidden flex flex-col h-[600px] w-full max-w-2xl mx-auto rounded-3xl">
      {/* Header */}
      <div className="p-4 border-b border-black/5 flex items-center gap-3 bg-white/40 backdrop-blur-md">
        <div className="h-10 w-10 bg-linear-to-tr from-indigo-500 to-purple-600 rounded-2xl flex items-center justify-center shadow-lg shadow-indigo-500/20">
          <Bot className="h-6 w-6 text-white" />
        </div>
        <div>
          <h3 className="font-bold text-lg leading-tight flex items-center gap-2">
            AI Assistant <Sparkles className="h-3 w-3 text-indigo-500" />
          </h3>
          <p className="text-xs text-muted-foreground font-medium">
            Powered by MCP Agents
          </p>
        </div>
      </div>

      {/* Messages */}
      <div className="flex-1 overflow-y-auto p-4 space-y-4 custom-scrollbar">
        <AnimatePresence initial={false}>
          {messages.map((message) => (
            <motion.div
              key={message.id}
              initial={{ opacity: 0, y: 10, scale: 0.95 }}
              animate={{ opacity: 1, y: 0, scale: 1 }}
              transition={{ duration: 0.2 }}
              className={cn(
                "flex items-start gap-3 max-w-[85%]",
                message.role === "user" ? "ml-auto flex-row-reverse" : "mr-auto"
              )}
            >
              <div
                className={cn(
                  "h-8 w-8 rounded-full flex items-center justify-center shrink-0 shadow-sm",
                  message.role === "user"
                    ? "bg-slate-900 text-white"
                    : "bg-white text-indigo-600 border border-indigo-100"
                )}
              >
                {message.role === "user" ? (
                  <User className="h-4 w-4" />
                ) : (
                  <Bot className="h-4 w-4" />
                )}
              </div>

              <div
                className={cn(
                  "p-3 rounded-2xl text-sm leading-relaxed shadow-sm",
                  message.role === "user"
                    ? "bg-slate-900 text-white rounded-tr-none"
                    : "bg-white border border-white/60 rounded-tl-none"
                )}
              >
                {message.content.split("\n").map((line, i) => (
                  <p key={i} className={i > 0 ? "mt-1" : ""}>
                    {line}
                  </p>
                ))}
                <span
                  className={cn(
                    "text-[10px] block mt-1 opacity-50",
                    message.role === "user"
                      ? "text-slate-300"
                      : "text-slate-500"
                  )}
                >
                  {message.timestamp.toLocaleTimeString([], {
                    hour: "2-digit",
                    minute: "2-digit",
                  })}
                </span>
              </div>
            </motion.div>
          ))}
        </AnimatePresence>

        {isLoading && (
          <motion.div
            initial={{ opacity: 0, y: 10 }}
            animate={{ opacity: 1, y: 0 }}
            className="flex items-start gap-3 mr-auto"
          >
            <div className="h-8 w-8 rounded-full bg-white text-indigo-600 border border-indigo-100 flex items-center justify-center shrink-0 shadow-sm">
              <Bot className="h-4 w-4" />
            </div>
            <div className="bg-white/50 border border-white/60 p-4 rounded-2xl rounded-tl-none flex items-center gap-2">
              <Loader2 className="h-4 w-4 animate-spin text-indigo-600" />
              <span className="text-xs font-medium text-muted-foreground">
                Thinking...
              </span>
            </div>
          </motion.div>
        )}
        <div ref={messagesEndRef} />
      </div>

      {/* Input */}
      <div className="p-4 bg-white/40 backdrop-blur-md border-t border-black/5">
        <form onSubmit={handleSubmit} className="flex gap-2 relative">
          <Input
            value={inputValue}
            onChange={(e) => setInputValue(e.target.value)}
            placeholder="Type a command (e.g., 'Add a task to buy milk')..."
            className="rounded-xl h-12 pr-12 border-black/5 bg-white/80 focus:bg-white transition-all shadow-inner"
            disabled={isLoading}
          />
          <Button
            type="submit"
            size="icon"
            disabled={!inputValue.trim() || isLoading}
            className={cn(
              "absolute right-1 top-1 h-10 w-10 rounded-lg transition-all",
              inputValue.trim()
                ? "bg-indigo-600 hover:bg-indigo-700 text-white shadow-lg shadow-indigo-500/20"
                : "bg-transparent text-muted-foreground hover:bg-black/5 shadow-none"
            )}
          >
            {isLoading ? (
              <Loader2 className="h-5 w-5 animate-spin" />
            ) : (
              <Send className="h-5 w-5" />
            )}
          </Button>
        </form>
      </div>
    </Card>
  );
}

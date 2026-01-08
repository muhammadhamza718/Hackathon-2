"use client";

import { ChatKit, useChatKit } from "@openai/chatkit-react";
import type { ChatKitOptions, HeaderIcon } from "@openai/chatkit-react";
import { useTheme } from "next-themes";
import { useMemo, useState, useEffect } from "react";
import dynamic from "next/dynamic";
import { useSidebar } from "../ui/sidebar";
import { authClient } from "@/lib/auth-client";
import { useAuth } from "@/contexts/AuthContext";

/**
 * Todo ChatKit Component
 * Uses ChatKit React for real-time streaming chat with the todo agent
 */

function TodoChatKitComponent() {
  const { toggleSidebar } = useSidebar();
  const { resolvedTheme, theme: activeTheme } = useTheme();
  const { user, session, isLoading: authLoading } = useAuth();
  const [mounted, setMounted] = useState(false);
  const isDark = resolvedTheme === "dark" || activeTheme === "dark";

  // Resolve backend URL with robustness for 8000/8001 port confusion
  const backendUrl = useMemo(() => {
    const envUrl =
      process.env.NEXT_PUBLIC_BACKEND_URL || process.env.NEXT_PUBLIC_API_URL;

    // If it's localhost and port 8001, but we know our ChatKit server is on 8000, force 8000
    if (
      envUrl?.includes("localhost:8001") ||
      envUrl?.includes("127.0.0.1:8001")
    ) {
      return envUrl.replace("8001", "8000");
    }

    return envUrl || "http://localhost:8000";
  }, []);

  // Prevent hydration mismatch
  useEffect(() => {
    setMounted(true);
    if (user) {
      const finalUrl = `${backendUrl.replace(/\/$/, "")}/chatkit`;
      console.log("🚀 TodoChatKit mounting for:", user.email);
      console.log("🔌 Backend URL:", finalUrl);
    }
  }, [backendUrl, user]);

  // Extract token from session
  const token = useMemo(() => session?.token ?? null, [session]);

  // ChatKit options
  const chatkitOptions: ChatKitOptions = useMemo(
    () => ({
      api: {
        url: `${backendUrl.replace(/\/$/, "")}/chatkit`,
        domainKey: "domain_pk_694e660b27cc8194af36166984c678920dffab26d4b3cd54", // Production domain key
        headers: {
          ...(token && { Authorization: `Bearer ${token}` }),
        },
      },
      header: {
        title: {
          text: "Todo Assistant 🤖",
        },
        leftAction: {
          icon: "close" as HeaderIcon,
          onClick: toggleSidebar,
        },
      },
      theme: (isDark ? "dark" : "light") as "dark" | "light",
    }),
    [backendUrl, isDark, toggleSidebar, token]
  );

  // Initialize ChatKit
  const { control } = useChatKit(chatkitOptions);

  // Don't render if not mounted, auth is loading, or user is not logged in
  if (!mounted || authLoading || !user) {
    return null;
  }

  return (
    <div className="w-full h-full overflow-hidden flex flex-col">
      <ChatKit control={control} />
    </div>
  );
}

// Dynamically import to avoid SSR issues
const TodoChatKit = dynamic(() => Promise.resolve(TodoChatKitComponent), {
  ssr: false,
  loading: () => (
    <div className="flex items-center justify-center h-full">
      <div className="animate-pulse text-muted-foreground space-y-2 text-center">
        <div className="text-sm font-bold tracking-widest uppercase opacity-50">
          AI Twin
        </div>
        <div>Initializing interface...</div>
      </div>
    </div>
  ),
});

export default TodoChatKit;

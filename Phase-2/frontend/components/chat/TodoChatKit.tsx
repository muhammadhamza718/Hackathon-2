"use client";

import { useTheme } from "next-themes";
import { useMemo, useState, useEffect, useRef } from "react";
import dynamic from "next/dynamic";
import { useSidebar } from "../ui/sidebar";
import { authClient } from "@/lib/auth-client";
import { useAuth } from "@/contexts/AuthContext";
import { ErrorBoundary } from "../ui/error-boundary";

/**
 * Todo ChatKit Component
 * Uses ChatKit Web Component directly to avoid React wrapper issues
 */

function TodoChatKitComponent() {
  const { toggleSidebar } = useSidebar();
  const { resolvedTheme, theme: activeTheme } = useTheme();
  const { user, session, isLoading: authLoading } = useAuth();
  const [mounted, setMounted] = useState(false);
  const isDark = resolvedTheme === "dark" || activeTheme === "dark";
  const chatRef = useRef<any>(null);

  // Resolve backend URL with robustness for 8000/8001 port confusion
  const backendUrl = useMemo(() => {
    const envUrl =
      process.env.NEXT_PUBLIC_BACKEND_URL || process.env.NEXT_PUBLIC_API_URL;

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
  }, []);

  // Extract token from session
  const token = useMemo(() => session?.token ?? null, [session]);

  useEffect(() => {
    const el = chatRef.current;
    if (!el || !mounted || !user) return;

    const options = {
      api: {
        url: `${backendUrl.replace(/\/$/, "")}/chatkit?token=${token}`,
        domainKey: "domain_pk_694e660b27cc8194af36166984c678920dffab26d4b3cd54",
      } as any,
      header: {
        title: {
          text: "Todo Assistant 🤖",
        },
        leftAction: {
          icon: "close",
          onClick: toggleSidebar,
        },
      },
      theme: (isDark ? "dark" : "light") as any,
    };

    console.log(
      "🛠️ ChatKit options (Manual Set):",
      JSON.stringify(options, null, 2),
    );

    customElements
      .whenDefined("openai-chatkit")
      .then(() => {
        // Small delay to ensure element is ready
        setTimeout(() => {
          if (el && typeof el.setOptions === "function") {
            try {
              el.setOptions(options);
              console.log("✅ ChatKit options set successfully");
            } catch (e) {
              console.error("❌ Error setting ChatKit options:", e);
            }
          } else {
            console.warn(
              "⚠️ ChatKit element not ready or setOptions missing",
              el,
            );
          }
        }, 100);
      })
      .catch((err) => {
        console.error("Failed to define openai-chatkit:", err);
      });
  }, [backendUrl, token, isDark, toggleSidebar, mounted, user]);

  // Don't render if not mounted, auth is loading, or user is not logged in
  if (!mounted || authLoading || !user) {
    return (
      <div className="p-4 text-xs text-muted-foreground">
        <p>Debug Status:</p>
        <ul className="list-disc pl-4">
          <li>Mounted: {mounted.toString()}</li>
          <li>Auth Loading: {authLoading.toString()}</li>
          <li>User: {user ? "Logged In" : "Null"}</li>
        </ul>
      </div>
    );
  }

  return (
    <div className="w-full h-full overflow-hidden flex flex-col">
      <ErrorBoundary>
        {/* @ts-ignore - Custom element not typed */}
        <openai-chatkit ref={chatRef} class="w-full h-full" />
      </ErrorBoundary>
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

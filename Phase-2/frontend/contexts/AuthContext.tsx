"use client";

import { createContext, useContext, ReactNode, useMemo } from "react";
import { useSession } from "@/lib/auth-client";

interface AuthContextType {
  user: any | null;
  userId: string | null;
  session: any | null;
  isLoading: boolean;
  error: Error | null;
}

const AuthContext = createContext<AuthContextType | undefined>(undefined);

export function AuthProvider({ children }: { children: ReactNode }) {
  const { data: session, isPending, error } = useSession();

  const value = useMemo(
    () => ({
      user: session?.user ?? null,
      userId: session?.user?.id ?? null,
      session: session?.session ?? null,
      isLoading: isPending,
      error: error ?? null,
    }),
    [session, isPending, error]
  );

  return <AuthContext.Provider value={value}>{children}</AuthContext.Provider>;
}

export function useAuth() {
  const context = useContext(AuthContext);
  if (!context) {
    throw new Error("useAuth must be used within AuthProvider");
  }
  return context;
}

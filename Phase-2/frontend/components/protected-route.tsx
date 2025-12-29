"use client";

import { useSession } from "@/lib/auth-client";
import { useRouter } from "next/navigation";
import { useEffect } from "react";
import { Loader2 } from "lucide-react";

interface ProtectedRouteProps {
  children: React.ReactNode;
  requireAdmin?: boolean;
  unauthorizedPath?: string;
}

export function ProtectedRoute({
  children,
  requireAdmin = false,
  unauthorizedPath = "/dashboard",
}: ProtectedRouteProps) {
  const { data: session, isPending } = useSession();
  const router = useRouter();

  useEffect(() => {
    if (!isPending && !session) {
      router.push("/auth/signin");
      return;
    }

    if (
      !isPending &&
      session &&
      requireAdmin &&
      (session.user as any).role !== "admin"
    ) {
      router.push(unauthorizedPath);
    }
  }, [session, isPending, requireAdmin, router, unauthorizedPath]);

  if (isPending) {
    return (
      <div className="min-h-screen flex items-center justify-center">
        <Loader2 className="h-8 w-8 animate-spin text-primary" />
      </div>
    );
  }

  if (!session) return null;
  if (requireAdmin && (session.user as any).role !== "admin") return null;

  return <>{children}</>;
}

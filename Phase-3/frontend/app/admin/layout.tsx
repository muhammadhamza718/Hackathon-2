"use client";

import { Sidebar } from "@/components/admin/sidebar";
import { ProtectedRoute } from "@/components/protected-route";

export default function AdminLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <ProtectedRoute requireAdmin={true} unauthorizedPath="/dashboard">
      <div className="flex min-h-screen bg-neutral-100/50">
        <Sidebar />
        <main className="flex-1 transition-all duration-300 ease-in-out">
          {children}
        </main>
      </div>
    </ProtectedRoute>
  );
}

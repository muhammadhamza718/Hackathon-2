"use client";

import * as React from "react";
import { Button } from "@/components/ui/button";
import Link from "next/link";
import { usePathname } from "next/navigation";
import { useAuth } from "@/contexts/AuthContext";
import { signOut } from "@/lib/auth-client";
import { useRouter } from "next/navigation";

import { useSidebar } from "./ui/sidebar";
import { MessageSquare } from "lucide-react";

interface NavItem {
  label: string;
  href: string;
}

const navItems: NavItem[] = [
  { label: "Dashboard", href: "/dashboard" },
  { label: "Admin", href: "/admin/dashboard" },
];

const Navigation = () => {
  const pathname = usePathname();
  const router = useRouter();
  const { user, isLoading } = useAuth();
  const { toggleSidebar } = useSidebar();

  const handleLogout = async () => {
    await signOut();
    router.push("/auth/signin");
  };

  return (
    <header className="glass sticky top-0 z-50 border-x-0 border-t-0 rounded-none">
      <div className="max-w-6xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex justify-between items-center h-16">
          <Link href="/" className="text-xl font-bold text-foreground">
            TaskManager
          </Link>

          <nav className="hidden md:flex space-x-8">
            {user ? (
              <>
                {navItems.map((item) => {
                  if (item.label === "Admin" && user.role !== "admin") {
                    return null;
                  }

                  return (
                    <Link
                      key={item.href}
                      href={item.href}
                      className={`text-sm font-medium transition-colors ${
                        pathname === item.href
                          ? "text-foreground"
                          : "text-muted-foreground hover:text-foreground"
                      }`}
                    >
                      {item.label}
                    </Link>
                  );
                })}
              </>
            ) : null}
          </nav>

          <div className="flex items-center space-x-4">
            {isLoading ? (
              <span className="text-sm text-muted-foreground">Loading...</span>
            ) : user ? (
              <>
                <Button
                  variant="ghost"
                  size="sm"
                  onClick={toggleSidebar}
                  className="gap-2 text-primary hover:text-primary hover:bg-primary/10"
                >
                  <MessageSquare className="h-4 w-4" />
                  <span>AI Chat</span>
                </Button>

                <div className="h-4 w-px bg-border mx-2" />

                <span className="text-sm text-muted-foreground hidden md:block">
                  {user.name || user.email}
                </span>
                <Button
                  variant="ghost"
                  onClick={handleLogout}
                  className="text-sm"
                >
                  Logout
                </Button>
              </>
            ) : (
              <>
                <Button variant="ghost" asChild>
                  <Link href="/auth/signin">Sign In</Link>
                </Button>
                <Button asChild>
                  <Link href="/auth/signup">Sign Up</Link>
                </Button>
              </>
            )}
          </div>
        </div>
      </div>
    </header>
  );
};

export { Navigation };

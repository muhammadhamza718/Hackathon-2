"use client";

import * as React from "react";
import Link from "next/link";
import { usePathname, useRouter } from "next/navigation";
import { cn } from "@/lib/utils";
import {
  LayoutDashboard,
  Users,
  Settings,
  LogOut,
  ShieldCheck,
} from "lucide-react";
import { signOut } from "@/lib/auth-client";

export function Sidebar() {
  const pathname = usePathname();
  const router = useRouter();

  const handleSignOut = async () => {
    await signOut();
    router.push("/auth/signin");
  };

  const menuItems = [
    { icon: LayoutDashboard, label: "Dashboard", href: "/admin/dashboard" },
  ];

  return (
    <div className="w-[280px] h-full glass border-r border-white/60 flex flex-col p-6 fixed left-0 top-0 z-40 shadow-xl bg-white/50 backdrop-blur-xl">
      <div className="flex items-center gap-3 mb-10 px-2 pt-2">
        <div className="h-10 w-10 bg-linear-to-br from-primary to-indigo-600 rounded-xl flex items-center justify-center shadow-lg shadow-primary/20">
          <ShieldCheck className="h-6 w-6 text-white" />
        </div>
        <div className="flex flex-col">
          <span className="font-black text-lg tracking-tight leading-none">
            ADMIN
          </span>
          <span className="text-[10px] font-bold uppercase tracking-[0.2em] text-muted-foreground">
            Console
          </span>
        </div>
      </div>

      <div className="space-y-6 flex-1">
        <div className="px-2">
          <p className="text-[10px] font-black uppercase tracking-widest text-muted-foreground/50 mb-4">
            Navigation
          </p>
          <nav className="space-y-2">
            {menuItems.map((item) => (
              <Link
                key={item.label}
                href={item.href}
                className={cn(
                  "flex items-center gap-3 px-4 py-3 rounded-xl transition-all font-bold text-sm",
                  pathname === item.href
                    ? "bg-primary text-white shadow-lg shadow-primary/30"
                    : "text-muted-foreground hover:bg-white/60 hover:text-foreground hover:shadow-sm"
                )}
              >
                <item.icon className="h-5 w-5" />
                {item.label}
              </Link>
            ))}
          </nav>
        </div>
      </div>

      <div className="mt-auto px-2">
        <button
          onClick={handleSignOut}
          className="w-full flex items-center gap-3 px-4 py-3 rounded-xl text-muted-foreground hover:bg-destructive/10 hover:text-destructive transition-all font-bold text-sm group"
        >
          <LogOut className="h-5 w-5 group-hover:translate-x-1 transition-transform" />
          Terminate Session
        </button>
      </div>
    </div>
  );
}

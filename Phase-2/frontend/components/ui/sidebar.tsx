"use client";

import * as React from "react";
import { createContext, useContext, useState, useEffect } from "react";
import { AnimatePresence, motion } from "framer-motion";
import { cn } from "@/lib/utils";

interface SidebarContextType {
  isOpen: boolean;
  setIsOpen: (open: boolean) => void;
  toggleSidebar: () => void;
}

const SidebarContext = createContext<SidebarContextType | undefined>(undefined);

export function SidebarProvider({ children }: { children: React.ReactNode }) {
  const [isOpen, setIsOpen] = useState(false);

  const toggleSidebar = () => setIsOpen((prev) => !prev);

  // Close on escape key
  useEffect(() => {
    const handleKeyDown = (event: KeyboardEvent) => {
      if (event.key === "Escape") setIsOpen(false);
    };
    window.addEventListener("keydown", handleKeyDown);
    return () => window.removeEventListener("keydown", handleKeyDown);
  }, []);

  return (
    <SidebarContext.Provider value={{ isOpen, setIsOpen, toggleSidebar }}>
      {children}
    </SidebarContext.Provider>
  );
}

export function useSidebar() {
  const context = useContext(SidebarContext);
  if (!context) {
    throw new Error("useSidebar must be used within a SidebarProvider");
  }
  return context;
}

interface SidebarProps {
  children: React.ReactNode;
  side?: "left" | "right";
  className?: string;
}

export function Sidebar({ children, side = "right", className }: SidebarProps) {
  const { isOpen, setIsOpen } = useSidebar();

  return (
    <AnimatePresence>
      {isOpen && (
        <div className="fixed inset-0 z-[100] flex">
          {/* Backdrop */}
          <motion.div
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            exit={{ opacity: 0 }}
            onClick={() => setIsOpen(false)}
            className="fixed inset-0 bg-black/40 backdrop-blur-sm transition-opacity"
          />

          {/* Sidebar Content */}
          <motion.div
            initial={{ x: side === "right" ? "100%" : "-100%" }}
            animate={{ x: 0 }}
            exit={{ x: side === "right" ? "100%" : "-100%" }}
            transition={{ type: "spring", damping: 25, stiffness: 200 }}
            className={cn(
              "absolute inset-y-0 z-[110] w-full max-w-md bg-white dark:bg-black shadow-2xl flex flex-col border-white/10 overflow-hidden",
              side === "right" ? "right-0 border-l" : "left-0 border-r",
              className
            )}
          >
            {children}
          </motion.div>
        </div>
      )}
    </AnimatePresence>
  );
}

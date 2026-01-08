"use client";

import * as React from "react";
import { motion } from "framer-motion";
import { LucideIcon, TrendingUp, TrendingDown } from "lucide-react";
import { cn } from "@/lib/utils";

interface StatCardProps {
  label: string;
  value: string | number;
  icon: LucideIcon;
  trend?: string;
  trendUp?: boolean;
  color?: string;
  className?: string;
}

export function StatCard({
  label,
  value,
  icon: Icon,
  trend,
  trendUp,
  color = "primary",
  className,
}: StatCardProps) {
  // Map simple color names to tailwind classes if needed, or use as is
  // The usage passed "blue-600", "indigo-600", etc. which are probably tailwind colors.
  // We'll assume these are used for text/bg classes.

  return (
    <motion.div
      whileHover={{ y: -5 }}
      className={cn(
        "glass p-6 rounded-3xl border-white/60 shadow-lg relative overflow-hidden group",
        className
      )}
    >
      <div className="flex justify-between items-start mb-4">
        <div
          className={cn(
            "p-3 rounded-2xl transition-transform group-hover:scale-110",
            `bg-${color}/10 text-${color}`
          )}
        >
          <Icon className="h-6 w-6" />
        </div>
        {trend && (
          <div
            className={cn(
              "flex items-center gap-1 text-xs font-bold px-2 py-1 rounded-full",
              trendUp
                ? "bg-green-100 text-green-700"
                : "bg-red-100 text-red-700"
            )}
          >
            {trendUp ? (
              <TrendingUp className="h-3 w-3" />
            ) : (
              <TrendingDown className="h-3 w-3" />
            )}
            {trend}
          </div>
        )}
      </div>

      <div className="space-y-1">
        <h3 className="text-2xl font-black tracking-tight text-foreground">
          {value}
        </h3>
        <p className="text-xs font-bold uppercase tracking-widest text-muted-foreground/60">
          {label}
        </p>
      </div>

      {/* Decorative gradient blob */}
      <div
        className={cn(
          "absolute -right-6 -bottom-6 h-24 w-24 rounded-full opacity-10 blur-2xl transition-opacity group-hover:opacity-20",
          `bg-${color}`
        )}
      />
    </motion.div>
  );
}

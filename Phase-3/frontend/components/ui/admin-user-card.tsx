"use client";

import * as React from "react";
import { Card, CardContent, CardFooter } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { cn } from "@/lib/utils";

interface AdminUserCardProps {
  id: string;
  name: string;
  email: string;
  role: string;
  createdAt: string;
  onEdit: (id: string) => void;
  onDelete: (id: string) => void;
  onToggleStatus: (id: string) => void;
  isActive: boolean;
}

const AdminUserCard = ({
  id,
  name,
  email,
  role,
  createdAt,
  onEdit,
  onDelete,
  onToggleStatus,
  isActive,
}: AdminUserCardProps) => {
  return (
    <Card
      className={cn(
        "transition-all duration-300 hover:shadow-2xl border-white/40 shadow-lg group/user",
        "bg-white/40 backdrop-blur-xl saturate-150",
        !isActive && "opacity-60 bg-gray-100/20"
      )}
    >
      <CardContent className="p-6">
        <div className="flex items-start gap-4">
          <div className="flex h-14 w-14 flex-shrink-0 items-center justify-center rounded-2xl bg-linear-to-br from-indigo-500/20 to-cyan-500/20 text-indigo-600 font-bold text-xl shadow-inner border border-white/50 group-hover/user:scale-110 transition-transform">
            {name.charAt(0).toUpperCase()}
          </div>
          <div className="flex-1 min-w-0">
            <div className="flex justify-between items-start">
              <h3 className="font-bold text-xl tracking-tight truncate text-foreground decoration-indigo-500/30">
                {name}
              </h3>
              <span
                className={cn(
                  "inline-flex items-center px-3 py-1 rounded-full text-[10px] font-bold uppercase tracking-widest shadow-sm",
                  role === "admin"
                    ? "bg-indigo-600 text-white shadow-indigo-200"
                    : "bg-white/80 text-muted-foreground border border-white/40"
                )}
              >
                {role}
              </span>
            </div>
            <p className="text-sm font-medium text-muted-foreground/80 truncate mt-0.5">
              {email}
            </p>

            <div className="flex items-center gap-4 mt-4">
              <div className="flex flex-col">
                <span className="text-[10px] uppercase font-bold text-muted-foreground/40 tracking-tighter">
                  User Role
                </span>
                <span className="text-xs font-semibold text-indigo-600/70">
                  {role === "admin" ? "Administrator" : "Standard User"}
                </span>
              </div>
              <div className="flex flex-col">
                <span className="text-[10px] uppercase font-bold text-muted-foreground/40 tracking-tighter">
                  Status
                </span>
                <div className="flex items-center gap-1.5">
                  <span
                    className={cn(
                      "h-1.5 w-1.5 rounded-full animate-pulse",
                      isActive ? "bg-green-500" : "bg-red-500"
                    )}
                  />
                  <span className="text-xs font-semibold text-muted-foreground">
                    {isActive ? "Active" : "Inactive"}
                  </span>
                </div>
              </div>
            </div>
          </div>
        </div>
      </CardContent>
      <CardFooter className="flex justify-between p-6 pt-0 gap-3">
        <div className="text-[10px] items-center flex font-mono text-muted-foreground/50">
          ID: {id.slice(0, 8)}...
        </div>
        <div className="flex gap-2">
          <Button
            variant="ghost"
            size="sm"
            onClick={() => onToggleStatus(id)}
            className="text-xs font-bold rounded-lg hover:bg-black/5"
          >
            {isActive ? "Deactivate" : "Activate"}
          </Button>
          <Button
            variant="outline"
            size="sm"
            onClick={() => onEdit(id)}
            className="text-xs font-bold rounded-lg border-white/40 bg-white/30 hover:bg-white"
          >
            Change Role
          </Button>
          <Button
            variant="ghost"
            size="sm"
            onClick={() => onDelete(id)}
            className="text-destructive hover:text-white hover:bg-destructive rounded-lg text-xs font-bold transition-all"
          >
            Delete
          </Button>
        </div>
      </CardFooter>
    </Card>
  );
};

export { AdminUserCard };

"use client";

import * as React from "react";
import { useState, useEffect } from "react";
import { motion, AnimatePresence } from "framer-motion";
import {
  adminGetUsers,
  adminGetUserTasks,
  adminDeleteUser,
  adminUpdateUserRole,
  adminDeleteTask,
} from "@/lib/api";
import { Task, User } from "@/lib/types";
import { StatCard } from "@/components/admin/stat-card";
import { ConfirmationModal } from "@/components/admin/confirmation-modal";
import { AdminUserCard } from "@/components/ui/admin-user-card";
import {
  ShieldCheck,
  Users,
  Search,
  RefreshCcw,
  ListTodo,
  Clock,
  ShieldAlert,
  LayoutGrid,
  Table as TableIcon,
} from "lucide-react";
import { Input } from "@/components/ui/input";
import { Button } from "@/components/ui/button";

/**
 * Admin Dashboard - Refactored for Professional Routing
 * Note: Sidebar and Protection are handled at the Layout/Middleware level.
 */
const AdminDashboardPage = () => {
  const [users, setUsers] = useState<User[]>([]);
  const [userTasks, setUserTasks] = useState<Record<string, Task[]>>({});
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [searchQuery, setSearchQuery] = useState("");
  const [viewMode, setViewMode] = useState<"grid" | "table">("grid");

  // Modal States
  const [deleteModal, setDeleteModal] = useState<{
    isOpen: boolean;
    userId: string | null;
    userName: string | null;
  }>({
    isOpen: false,
    userId: null,
    userName: null,
  });
  const [isProcessing, setIsProcessing] = useState(false);

  useEffect(() => {
    fetchData();
  }, []);

  const fetchData = async () => {
    try {
      setLoading(true);
      setError(null);
      const usersData = await adminGetUsers();
      setUsers(usersData);

      const tasksMap: Record<string, Task[]> = {};
      await Promise.all(
        usersData.map(async (user) => {
          try {
            const data = await adminGetUserTasks(user.id);
            tasksMap[user.id] = data;
          } catch (err) {
            tasksMap[user.id] = [];
          }
        })
      );
      setUserTasks(tasksMap);
    } catch (err) {
      setError(
        "System Access Denied: Secure communication with the management service failed."
      );
    } finally {
      setLoading(false);
    }
  };

  const handleDeleteUser = async () => {
    if (!deleteModal.userId) return;
    try {
      setIsProcessing(true);
      await adminDeleteUser(deleteModal.userId);
      setUsers(users.filter((u) => u.id !== deleteModal.userId));
      setDeleteModal({ isOpen: false, userId: null, userName: null });
    } catch (err) {
      setError("Critical: Failed to de-authorize subject.");
    } finally {
      setIsProcessing(false);
    }
  };

  const handleToggleRole = async (userId: string, currentRole: string) => {
    try {
      const newRole = currentRole === "admin" ? "user" : "admin";
      await adminUpdateUserRole(userId, newRole);
      setUsers(
        users.map((u) => (u.id === userId ? { ...u, role: newRole } : u))
      );
    } catch (err) {
      setError("Role transition failed.");
    }
  };

  const handleAdminDeleteTask = async (userId: string, taskId: string) => {
    try {
      await adminDeleteTask(userId, taskId);
      setUserTasks((prev) => ({
        ...prev,
        [userId]: prev[userId].filter((t) => t.id !== taskId),
      }));
    } catch (err) {
      console.error("Failed to delete user task", err);
    }
  };

  const filteredUsers = users.filter(
    (user) =>
      user.name.toLowerCase().includes(searchQuery.toLowerCase()) ||
      user.email.toLowerCase().includes(searchQuery.toLowerCase())
  );

  const totalTasks = Object.values(userTasks).flat().length;
  const completedTasks = Object.values(userTasks)
    .flat()
    .filter((t) => t.completed).length;

  if (loading) {
    return (
      <div className="min-h-screen flex flex-col items-center justify-center gap-4">
        <motion.div
          animate={{ rotate: 360 }}
          transition={{ duration: 4, repeat: Infinity, ease: "linear" }}
        >
          <ShieldCheck className="h-16 w-16 text-primary" />
        </motion.div>
        <p className="text-sm font-bold animate-pulse text-primary uppercase tracking-[0.3em]">
          Syncing User Data
        </p>
      </div>
    );
  }

  return (
    <div className="p-8 ml-[280px] max-w-[1600px]">
      {/* Header Section */}
      <div className="flex justify-between items-center mb-10">
        <div>
          <h1 className="text-4xl font-extrabold tracking-tight text-foreground flex items-center gap-3">
            Overview
            <span className="text-xs bg-primary/10 text-primary px-3 py-1 rounded-full font-bold uppercase tracking-widest">
              Live
            </span>
          </h1>
          <p className="text-muted-foreground font-medium mt-1">
            System-wide operational management and user oversight.
          </p>
        </div>

        <div className="flex items-center gap-4">
          <div className="relative w-64">
            <Search className="absolute left-3 top-1/2 -translate-y-1/2 h-4 w-4 text-muted-foreground" />
            <Input
              placeholder="Search users..."
              className="pl-10 glass border-white/60 focus:bg-white rounded-xl shadow-inner h-11"
              value={searchQuery}
              onChange={(e) => setSearchQuery(e.target.value)}
            />
          </div>
          <Button
            onClick={fetchData}
            variant="outline"
            className="rounded-xl h-11 border-white/60 bg-white/40 shadow-sm gap-2"
          >
            <RefreshCcw className="h-4 w-4" /> Sync
          </Button>
        </div>
      </div>

      {/* KPI Dashboard */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 mb-12">
        <StatCard
          label="Total Users"
          value={users.length}
          icon={Users}
          trend="12%"
          trendUp
          color="blue-600"
        />
        <StatCard
          label="Total Tasks"
          value={totalTasks}
          icon={ListTodo}
          trend="5.2%"
          trendUp
          color="indigo-600"
        />
        <StatCard
          label="Completion Rate"
          value={`${Math.round((completedTasks / totalTasks) * 100) || 0}%`}
          icon={Clock}
          trend="2.1%"
          trendUp
          color="green-600"
        />
        <StatCard
          label="Security Alerts"
          value="0"
          icon={ShieldAlert}
          trend="100%"
          trendUp={false}
          color="red-600"
        />
      </div>

      {/* Main Content Area */}
      <div className="space-y-8">
        <div className="flex items-center justify-between border-b border-black/5 pb-4">
          <h2 className="text-xl font-bold flex items-center gap-2">
            User Management
            <span className="text-xs font-mono text-muted-foreground/50">
              [{filteredUsers.length} FOUND]
            </span>
          </h2>
          <div className="flex bg-white/40 p-1 rounded-xl border border-white/60 shadow-inner">
            <Button
              size="sm"
              variant={viewMode === "grid" ? "default" : "ghost"}
              className="rounded-lg h-8 w-8 p-0"
              onClick={() => setViewMode("grid")}
            >
              <LayoutGrid className="h-4 w-4" />
            </Button>
            <Button
              size="sm"
              variant={viewMode === "table" ? "default" : "ghost"}
              className="rounded-lg h-8 w-8 p-0"
              onClick={() => setViewMode("table")}
            >
              <TableIcon className="h-4 w-4" />
            </Button>
          </div>
        </div>

        {error && (
          <div className="bg-destructive/10 border border-destructive/20 p-4 rounded-2xl text-destructive text-sm font-bold flex items-center gap-3 animate-head-shake">
            <ShieldAlert className="h-5 w-5" />
            {error}
          </div>
        )}

        <motion.div layout className="grid gap-6">
          <AnimatePresence mode="popLayout">
            {filteredUsers.map((user) => (
              <motion.div
                key={user.id}
                initial={{ opacity: 0, y: 20 }}
                animate={{ opacity: 1, y: 0 }}
                exit={{ opacity: 0, scale: 0.95 }}
                className="glass rounded-4xl border-white/50 shadow-xl overflow-hidden group"
              >
                <div className="p-8 flex flex-col gap-8">
                  <AdminUserCard
                    id={user.id}
                    name={user.name}
                    email={user.email}
                    role={user.role}
                    createdAt={user.created_at}
                    isActive={user.is_active ?? true}
                    onEdit={() => handleToggleRole(user.id, user.role)}
                    onToggleStatus={() => {}}
                    onDelete={() =>
                      setDeleteModal({
                        isOpen: true,
                        userId: user.id,
                        userName: user.name,
                      })
                    }
                  />

                  {/* User's Task Snapshot */}
                  <div className="space-y-4">
                    <div className="flex items-center gap-3">
                      <span className="h-px flex-1 bg-black/5"></span>
                      <span className="text-[10px] font-extrabold uppercase tracking-[0.2em] text-muted-foreground/40 whitespace-nowrap">
                        Last Active Tasks
                      </span>
                      <span className="h-px flex-1 bg-black/5"></span>
                    </div>

                    {userTasks[user.id] && userTasks[user.id].length > 0 ? (
                      <div className="flex gap-4 overflow-x-auto pb-4 hide-scrollbar">
                        {userTasks[user.id].map((task) => (
                          <motion.div
                            key={task.id}
                            whileHover={{ scale: 1.02 }}
                            className="shrink-0 w-72 h-32 glass border-white/60 p-4 rounded-2xl flex flex-col justify-between group/task transition-all hover:shadow-lg"
                          >
                            <div>
                              <div className="flex justify-between items-start">
                                <h4
                                  className={`font-bold text-sm truncate pr-4 ${
                                    task.completed
                                      ? "line-through text-muted-foreground"
                                      : ""
                                  }`}
                                >
                                  {task.title}
                                </h4>
                                <span
                                  className={`h-1.5 w-1.5 rounded-full ${
                                    task.completed
                                      ? "bg-green-500"
                                      : "bg-primary"
                                  }`}
                                />
                              </div>
                              <p className="text-xs text-muted-foreground/70 line-clamp-2 mt-1">
                                {task.description}
                              </p>
                            </div>
                            <div className="flex justify-between items-center opacity-0 group-hover/task:opacity-100 transition-opacity">
                              <span className="text-[10px] font-mono text-muted-foreground/50">
                                {new Date(task.created_at).toLocaleDateString()}
                              </span>
                              <Button
                                size="sm"
                                variant="ghost"
                                className="h-6 text-[10px] text-destructive hover:bg-destructive/10 font-bold uppercase tracking-tighter"
                                onClick={() =>
                                  handleAdminDeleteTask(user.id, task.id)
                                }
                              >
                                {" "}
                                Delete Task{" "}
                              </Button>
                            </div>
                          </motion.div>
                        ))}
                      </div>
                    ) : (
                      <div className="bg-black/5 rounded-2xl p-6 text-center border-dashed border border-black/10">
                        <p className="text-xs font-bold text-muted-foreground opacity-50 uppercase tracking-widest">
                          No tasks found
                        </p>
                      </div>
                    )}
                  </div>
                </div>
              </motion.div>
            ))}
          </AnimatePresence>
        </motion.div>
      </div>

      <ConfirmationModal
        isOpen={deleteModal.isOpen}
        onClose={() =>
          setDeleteModal({ isOpen: false, userId: null, userName: null })
        }
        onConfirm={handleDeleteUser}
        title="Delete User"
        description={`Are you sure you want to permanently delete the account for ${deleteModal.userName}? This action cannot be undone.`}
        confirmText="Delete User"
        variant="destructive"
        isLoading={isProcessing}
      />
    </div>
  );
};

export default AdminDashboardPage;

"use client";

import * as React from "react";
import { useState, useEffect } from "react";
import { motion, AnimatePresence } from "framer-motion";
import { apiClient } from "@/lib/api";
import { Task } from "@/lib/types";
import { TaskCard } from "@/components/ui/task-card";
import { CreateTaskDialog } from "@/components/create-task-dialog";
import { Button } from "@/components/ui/button";
import { Navigation } from "@/components/navigation";
import {
  Plus,
  Loader2,
  LayoutDashboard,
  ListTodo,
  CheckCircle2,
  Clock,
  Sparkles,
  Search,
  Filter,
  ShieldAlert,
} from "lucide-react";
import { Input } from "@/components/ui/input";
import { useSession } from "@/lib/auth-client";

/**
 * User Dashboard - Refactored for Professional Routing
 * Note: Middleware handles the base protection. Navigation is consistent.
 */
export default function DashboardPage() {
  const [tasks, setTasks] = useState<Task[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [searchQuery, setSearchQuery] = useState("");
  const [isCreateOpen, setIsCreateOpen] = useState(false);
  const { data: session } = useSession();

  const fetchTasks = async () => {
    try {
      setLoading(true);
      setError(null);
      const data = await apiClient.getTasks();
      setTasks(data);
    } catch (err) {
      setError("Failed to load your tasks.");
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchTasks();
  }, []);

  const handleDeleteTask = async (id: string) => {
    try {
      await apiClient.deleteTask(id);
      setTasks(tasks.filter((t) => t.id !== id));
    } catch (err) {
      setError("Failed to delete task.");
    }
  };

  const handleToggleTask = async (task: Task) => {
    try {
      await apiClient.toggleTask(task.id, !task.completed);
      setTasks(
        tasks.map((t) =>
          t.id === task.id ? { ...t, completed: !t.completed } : t
        )
      );
    } catch (err) {
      setError("Failed to update task status.");
    }
  };

  const filteredTasks = tasks.filter(
    (t) =>
      t.title.toLowerCase().includes(searchQuery.toLowerCase()) ||
      t.description?.toLowerCase().includes(searchQuery.toLowerCase())
  );

  const completedCount = tasks.filter((t) => t.completed).length;

  return (
    <div className="min-h-screen bg-aurora animate-aurora">
      <Navigation />

      <main className="max-w-7xl mx-auto px-4 md:px-8 pt-28 pb-20">
        {/* Header Section */}
        <motion.div
          initial={{ opacity: 0, y: -20 }}
          animate={{ opacity: 1, y: 0 }}
          className="flex flex-col md:flex-row justify-between items-start md:items-center gap-6 mb-12"
        >
          <div>
            <div className="flex items-center gap-3 mb-2">
              <div className="h-10 w-10 bg-primary/20 rounded-2xl flex items-center justify-center border border-primary/20">
                <LayoutDashboard className="h-6 w-6 text-primary" />
              </div>
              <h1 className="text-4xl font-extrabold tracking-tight text-foreground">
                Task <span className="text-primary">Manager</span>
              </h1>
            </div>
            <p className="text-muted-foreground font-medium">
              Welcome back, {session?.user?.name || "User"}
            </p>
          </div>

          <div className="flex flex-wrap gap-3 w-full md:w-auto">
            <div className="relative flex-1 md:w-64">
              <Search className="absolute left-3 top-1/2 -translate-y-1/2 h-4 w-4 text-muted-foreground" />
              <Input
                placeholder="Search tasks..."
                className="glass pl-10 h-12 rounded-2xl border-white/60 focus:bg-white transition-all shadow-inner"
                value={searchQuery}
                onChange={(e) => setSearchQuery(e.target.value)}
              />
            </div>
            <Button
              onClick={() => setIsCreateOpen(true)}
              className="h-12 rounded-2xl px-6 font-bold shadow-lg shadow-primary/25 gap-2 active:scale-95 transition-transform"
            >
              <Plus className="h-5 w-5" /> New Task
            </Button>
          </div>
        </motion.div>

        {/* Stats Grid */}
        <div className="grid grid-cols-1 sm:grid-cols-3 gap-6 mb-12">
          <StatMini
            label="Active Tasks"
            value={tasks.length - completedCount}
            icon={Clock}
            color="indigo"
          />
          <StatMini
            label="Completed"
            value={completedCount}
            icon={CheckCircle2}
            color="green"
          />
          <StatMini
            label="Completion Rate"
            value={`${Math.round((completedCount / tasks.length) * 100) || 0}%`}
            icon={Sparkles}
            color="cyan"
          />
        </div>

        {error && (
          <motion.div
            initial={{ opacity: 0, scale: 0.95 }}
            animate={{ opacity: 1, scale: 1 }}
            className="mb-8 p-4 bg-destructive/10 border border-destructive/20 text-destructive rounded-2xl text-sm font-bold flex items-center gap-3"
          >
            <ShieldAlert className="h-5 w-5" /> {error}
          </motion.div>
        )}

        {/* Tasks Stream */}
        <div className="relative">
          <div className="flex items-center gap-3 mb-6 opacity-60">
            <ListTodo className="h-4 w-4" />
            <h2 className="text-xs font-black uppercase tracking-[0.3em]">
              Your Tasks
            </h2>
            <div className="h-px flex-1 bg-black/5" />
          </div>

          {loading ? (
            <div className="flex flex-col items-center justify-center py-20 gap-4 opacity-40">
              <Loader2 className="h-10 w-10 animate-spin text-primary" />
              <p className="text-sm font-bold uppercase tracking-widest">
                Loading Tasks...
              </p>
            </div>
          ) : filteredTasks.length > 0 ? (
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
              <AnimatePresence mode="popLayout">
                {filteredTasks.map((task, idx) => (
                  <motion.div
                    key={task.id}
                    initial={{ opacity: 0, y: 20 }}
                    animate={{ opacity: 1, y: 0 }}
                    transition={{ delay: idx * 0.05 }}
                    exit={{ opacity: 0, scale: 0.9 }}
                    layout
                  >
                    <TaskCard
                      task={task}
                      onDelete={() => handleDeleteTask(task.id)}
                      onToggle={handleToggleTask}
                      onEdit={(task) => console.log("Edit task", task)}
                    />
                  </motion.div>
                ))}
              </AnimatePresence>
            </div>
          ) : (
            <motion.div
              initial={{ opacity: 0 }}
              animate={{ opacity: 1 }}
              className="glass rounded-[3rem] p-20 text-center border-dashed border-2 border-black/5"
            >
              <div className="h-20 w-20 bg-black/5 rounded-full flex items-center justify-center mx-auto mb-6">
                <ListTodo className="h-10 w-10 text-muted-foreground/30" />
              </div>
              <h3 className="text-2xl font-black tracking-tight mb-2">
                No Tasks Found
              </h3>
              <p className="text-muted-foreground font-medium mb-8">
                Get organized by adding your first task.
              </p>
              <Button
                onClick={() => setIsCreateOpen(true)}
                variant="outline"
                className="rounded-2xl h-12 px-8 border-black/10 hover:bg-black/5 font-bold"
              >
                Add First Task
              </Button>
            </motion.div>
          )}
        </div>

        <CreateTaskDialog
          open={isCreateOpen}
          onOpenChange={setIsCreateOpen}
          onTaskCreated={(newTask) => setTasks([newTask, ...tasks])}
        />
      </main>
    </div>
  );
}

function StatMini({ label, value, icon: Icon, color }: any) {
  const colors: any = {
    indigo: "text-indigo-600 bg-indigo-50",
    green: "text-green-600 bg-green-50",
    cyan: "text-cyan-600 bg-cyan-50",
  };
  return (
    <motion.div
      whileHover={{ y: -5 }}
      className="glass p-6 rounded-3xl border-white/60 shadow-lg flex items-center gap-5 group"
    >
      <div
        className={`h-12 w-12 rounded-2xl flex items-center justify-center shrink-0 border border-white/40 shadow-inner group-hover:scale-110 transition-transform ${colors[color]}`}
      >
        <Icon className="h-6 w-6" />
      </div>
      <div>
        <p className="text-[10px] font-black uppercase tracking-widest text-muted-foreground/60">
          {label}
        </p>
        <p className="text-2xl font-black tracking-tight">{value}</p>
      </div>
    </motion.div>
  );
}

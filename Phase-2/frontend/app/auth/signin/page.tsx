"use client";

import * as React from "react";
import { useState } from "react";
import { motion, AnimatePresence } from "framer-motion";
import { Card } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import Link from "next/link";
import { signIn } from "@/lib/auth-client";
import { useRouter } from "next/navigation";
import { ShieldCheck, Lock, Loader2, Mail, Key } from "lucide-react";

/**
 * Unified Operational Access Portal
 * Detects role upon entry and routes to the appropriate quadrant.
 */
export default function SignInPage() {
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [error, setError] = useState("");
  const [loading, setLoading] = useState(false);
  const router = useRouter();

  const handleSignIn = async (e: React.FormEvent) => {
    e.preventDefault();
    setError("");
    setLoading(true);

    try {
      console.log("🔍 SIGN-IN ATTEMPT:", {
        email,
        apiUrl: process.env.NEXT_PUBLIC_API_URL,
      });
      const { data, error } = await signIn.email({
        email,
        password,
      });

      if (error) {
        console.error("❌ SIGN-IN ERROR (Better-Auth):", error);
        setError(error.message || "Invalid email or password.");
        setLoading(false);
        return;
      }

      console.log("✅ SIGN-IN SUCCESS (Better-Auth):", { data });

      // Transition Logic: Admin goes to Administration, User goes to Personal Dashboard
      const user = data?.user as any;
      const isAdmin = user?.role === "admin";

      console.log("🛠️ USER ROLE ANALYSIS:", {
        id: user?.id,
        email: user?.email,
        role: user?.role,
        isAdmin,
      });

      if (isAdmin) {
        console.log("🚀 REDIRECTING TO: /admin/dashboard");
        router.push("/admin/dashboard");
      } else {
        console.log("🚀 REDIRECTING TO: /dashboard");
        router.push("/dashboard");
      }

      router.refresh();
    } catch (err) {
      setError("Failed to sign in. Please try again.");
      setLoading(false);
    }
  };

  return (
    <div className="min-h-screen bg-aurora animate-aurora flex items-center justify-center p-4">
      <motion.div
        initial={{ opacity: 0, scale: 0.95 }}
        animate={{ opacity: 1, scale: 1 }}
        className="w-full max-w-md"
      >
        <Card className="glass p-10 border-white/60 shadow-2xl relative overflow-hidden rounded-[2.5rem]">
          <div className="text-center mb-10">
            <div className="h-16 w-16 bg-primary/10 rounded-2xl flex items-center justify-center mx-auto mb-4 border border-primary/20">
              <ShieldCheck className="h-8 w-8 text-primary" />
            </div>
            <h1 className="text-3xl font-black tracking-tighter text-foreground uppercase">
              Welcome <span className="text-primary">Back</span>
            </h1>
            <p className="text-muted-foreground font-medium mt-1 tracking-tight">
              Sign in to your account
            </p>
          </div>

          <AnimatePresence>
            {error && (
              <motion.div
                initial={{ opacity: 0, height: 0 }}
                animate={{ opacity: 1, height: "auto" }}
                exit={{ opacity: 0, height: 0 }}
                className="mb-8 p-4 bg-destructive/10 border border-destructive/20 text-destructive rounded-2xl text-[11px] font-bold flex items-center gap-3 backdrop-blur-md"
              >
                <Lock className="h-4 w-4 shrink-0" />
                {error}
              </motion.div>
            )}
          </AnimatePresence>

          <form onSubmit={handleSignIn} className="space-y-6">
            <div className="space-y-2">
              <Label className="text-[10px] font-black uppercase tracking-[0.2em] text-muted-foreground/60 ml-1">
                Email Address
              </Label>
              <div className="relative group">
                <Mail className="absolute left-4 top-1/2 -translate-y-1/2 h-4 w-4 text-muted-foreground/40 group-focus-within:text-primary transition-colors" />
                <Input
                  type="email"
                  value={email}
                  onChange={(e) => setEmail(e.target.value)}
                  placeholder="name@agency.net"
                  className="bg-white/40 border-white/60 h-14 pl-12 rounded-2xl focus:bg-white transition-all shadow-inner ring-0"
                  required
                />
              </div>
            </div>

            <div className="space-y-2">
              <Label className="text-[10px] font-black uppercase tracking-[0.2em] text-muted-foreground/60 ml-1">
                Password
              </Label>
              <div className="relative group">
                <Key className="absolute left-4 top-1/2 -translate-y-1/2 h-4 w-4 text-muted-foreground/40 group-focus-within:text-primary transition-colors" />
                <Input
                  type="password"
                  value={password}
                  onChange={(e) => setPassword(e.target.value)}
                  placeholder="••••••••"
                  className="bg-white/40 border-white/60 h-14 pl-12 rounded-2xl focus:bg-white transition-all shadow-inner ring-0"
                  required
                />
              </div>
            </div>

            <Button
              type="submit"
              className="w-full h-14 text-sm font-black uppercase tracking-[0.2em] rounded-2xl shadow-lg shadow-primary/20 hover:shadow-primary/40 transition-all active:scale-95 mt-4"
              disabled={loading}
            >
              {loading ? (
                <div className="flex items-center gap-2">
                  <Loader2 className="h-4 w-4 animate-spin" /> Signing in...
                </div>
              ) : (
                "Sign In"
              )}
            </Button>
          </form>

          <div className="mt-10 pt-8 border-t border-black/5 text-center">
            <p className="text-sm text-muted-foreground font-medium">
              Don't have an account?{" "}
              <Link
                href="/auth/signup"
                className="text-primary font-black uppercase tracking-tighter hover:underline"
              >
                Create Account
              </Link>
            </p>
          </div>
        </Card>
      </motion.div>
    </div>
  );
}

"use client";

import * as React from "react";
import { useState } from "react";
import { motion, AnimatePresence } from "framer-motion";
import { Card } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import Link from "next/link";
import { Navigation } from "@/components/navigation";
import { signIn, useSession, signOut } from "@/lib/auth-client";
import { useRouter } from "next/navigation";
import { ShieldCheck, Lock, ArrowRight, Loader2 } from "lucide-react";

const AdminSignInPage = () => {
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [error, setError] = useState("");
  const [loading, setLoading] = useState(false);
  const router = useRouter();
  const { data: session } = useSession();

  // Session Handling Effect
  React.useEffect(() => {
    if (session?.user) {
      if (session.user.role === "admin") {
        router.push("/admin/dashboard");
      } else {
        signOut();
      }
    }
  }, [session, router]);

  const handleSignIn = async (e: React.FormEvent) => {
    e.preventDefault();
    setError("");
    setLoading(true);

    try {
      const result = await signIn.email({
        email,
        password,
      });

      if (result.error) {
        setError(result.error.message || "Invalid admin credentials");
        setLoading(false);
        return;
      }
      router.push("/admin/dashboard");
    } catch (err) {
      setError("An unexpected error occurred");
      setLoading(false);
    }
  };

  return (
    <div className="min-h-screen bg-aurora animate-aurora overflow-hidden">
      <Navigation />
      <div className="min-h-screen flex items-center justify-center p-4 pt-24">
        <motion.div
          initial={{ opacity: 0, scale: 0.9, y: 20 }}
          animate={{ opacity: 1, scale: 1, y: 0 }}
          transition={{ duration: 0.5 }}
          className="w-full max-w-md"
        >
          <Card className="glass p-8 border-white/40 shadow-2xl relative overflow-hidden">
            {/* Decorative security glow */}
            <div className="absolute -top-24 -right-24 h-48 w-48 bg-primary/10 rounded-full blur-3xl" />

            <div className="text-center mb-8">
              <motion.div
                initial={{ rotate: -10, opacity: 0 }}
                animate={{ rotate: 0, opacity: 1 }}
                transition={{ delay: 0.2 }}
                className="flex justify-center mb-4"
              >
                <div className="h-16 w-16 bg-primary/10 rounded-2xl flex items-center justify-center rotate-3 group-hover:rotate-0 transition-transform">
                  <ShieldCheck className="h-8 w-8 text-primary shadow-sm" />
                </div>
              </motion.div>
              <h1 className="text-3xl font-extrabold tracking-tight text-foreground">
                Admin <span className="text-primary">Portal</span>
              </h1>
              <p className="text-muted-foreground mt-2 font-medium">
                Encrypted Administrative Access
              </p>
            </div>

            <AnimatePresence>
              {error && (
                <motion.div
                  initial={{ opacity: 0, height: 0 }}
                  animate={{ opacity: 1, height: "auto" }}
                  exit={{ opacity: 0, height: 0 }}
                  className="mb-6 p-4 bg-destructive/10 border border-destructive/20 text-destructive rounded-xl text-sm font-medium flex items-center gap-2"
                >
                  <Lock className="h-4 w-4" />
                  {error}
                </motion.div>
              )}
            </AnimatePresence>

            <form onSubmit={handleSignIn} className="space-y-6">
              <div className="space-y-2">
                <Label
                  htmlFor="email"
                  className="text-xs font-bold uppercase tracking-widest text-muted-foreground"
                >
                  Admin Identifier
                </Label>
                <Input
                  id="email"
                  type="email"
                  value={email}
                  onChange={(e) => setEmail(e.target.value)}
                  placeholder="admin@terminal.io"
                  className="bg-white/50 border-white/30 h-12 rounded-xl focus:bg-white transition-all shadow-inner"
                  required
                  disabled={loading}
                />
              </div>

              <div className="space-y-2">
                <Label
                  htmlFor="password"
                  title="Access Key"
                  className="text-xs font-bold uppercase tracking-widest text-muted-foreground"
                >
                  Secure Passkey
                </Label>
                <Input
                  id="password"
                  type="password"
                  value={password}
                  onChange={(e) => setPassword(e.target.value)}
                  placeholder="••••••••"
                  className="bg-white/50 border-white/30 h-12 rounded-xl focus:bg-white transition-all shadow-inner"
                  required
                  disabled={loading}
                />
              </div>

              <Button
                type="submit"
                className="w-full h-12 text-lg font-bold rounded-xl shadow-lg shadow-primary/20 hover:shadow-primary/40 transition-all active:scale-[0.98]"
                disabled={loading}
              >
                {loading ? (
                  <div className="flex items-center gap-2">
                    <Loader2 className="h-5 w-5 animate-spin" />
                    Verifying...
                  </div>
                ) : (
                  <div className="flex items-center gap-2">
                    Initialize Access <ArrowRight className="h-5 w-5" />
                  </div>
                )}
              </Button>
            </form>

            <div className="mt-8 pt-6 border-t border-black/5 text-center">
              <p className="text-sm text-muted-foreground">
                Standard clearance?{" "}
                <Link
                  href="/auth/signin"
                  className="text-primary font-bold hover:underline"
                >
                  Switch to User Terminal
                </Link>
              </p>
            </div>
          </Card>
        </motion.div>
      </div>
    </div>
  );
};

export default AdminSignInPage;

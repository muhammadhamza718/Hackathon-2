"use client";

import * as React from "react";
import { Button } from "@/components/ui/button";
import { Card } from "@/components/ui/card";
import Link from "next/link";
import { Navigation } from "@/components/navigation";

const HomePage = () => {
  const isLoggedIn =
    typeof window !== "undefined" && !!localStorage.getItem("auth_token");

  return (
    <>
      <Navigation />
      <div className="min-h-screen pt-24">
        <div className="max-w-6xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="text-center py-16 md:py-24">
            <h1 className="text-4xl md:text-6xl mb-6">
              Task Management Dashboard
            </h1>
            <p className="text-lg md:text-xl mb-10 max-w-2xl mx-auto">
              A modern, glassmorphism-inspired task management application with
              admin capabilities. Organize your work, track progress, and manage
              your team efficiently.
            </p>

            <div className="flex flex-col sm:flex-row justify-center gap-4">
              {isLoggedIn ? (
                <Button asChild size="lg">
                  <Link href="/dashboard">Go to Dashboard</Link>
                </Button>
              ) : (
                <>
                  <Button asChild size="lg">
                    <Link href="/auth/signup">Get Started</Link>
                  </Button>
                  <Button variant="outline" asChild size="lg">
                    <Link href="/auth/signin">Sign In</Link>
                  </Button>
                </>
              )}
            </div>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-3 gap-8 mb-16">
            <Card className="glass p-6 text-center">
              <h3 className="text-xl mb-3">Task Management</h3>
              <p>
                Create, update, and track your tasks with an intuitive interface
                designed for productivity.
              </p>
            </Card>

            <Card className="glass p-6 text-center">
              <h3 className="text-xl mb-3">Admin Dashboard</h3>
              <p>
                Oversee user activities and manage tasks across your
                organization with powerful admin tools.
              </p>
            </Card>

            <Card className="glass p-6 text-center">
              <h3 className="text-xl mb-3">Secure & Modern</h3>
              <p>
                Built with the latest technologies ensuring security,
                performance, and a premium user experience.
              </p>
            </Card>
          </div>
        </div>
      </div>
    </>
  );
};

export default HomePage;

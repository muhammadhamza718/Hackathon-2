"use client";

import React, { Component, ErrorInfo, ReactNode } from "react";
import { AlertCircle } from "lucide-react";
import { Alert, AlertDescription, AlertTitle } from "@/components/ui/alert";
import { Button } from "@/components/ui/button";

interface Props {
  children?: ReactNode;
  fallback?: ReactNode;
}

interface State {
  hasError: boolean;
  error: Error | null;
}

export class ErrorBoundary extends Component<Props, State> {
  public state: State = {
    hasError: false,
    error: null,
  };

  public static getDerivedStateFromError(error: Error): State {
    return { hasError: true, error };
  }

  public componentDidCatch(error: Error, errorInfo: ErrorInfo) {
    console.error("Uncaught error:", error, errorInfo);
  }

  public render() {
    if (this.state.hasError) {
      if (this.props.fallback) {
        return this.props.fallback;
      }

      return (
        <div className="p-4 rounded-lg bg-red-50 border border-red-200">
          <div className="flex items-center gap-2 text-red-800 font-bold mb-2">
            <AlertCircle className="h-4 w-4" />
            <span>Something went wrong</span>
          </div>
          <p className="text-sm text-red-600 mb-4">
            {this.state.error?.message || "An unexpected error occurred."}
          </p>
          <Button
            variant="outline"
            size="sm"
            onClick={() => this.setState({ hasError: false, error: null })}
            className="bg-white border-red-200 hover:bg-red-50 text-red-700"
          >
            Try again
          </Button>
        </div>
      );
    }

    return this.props.children;
  }
}

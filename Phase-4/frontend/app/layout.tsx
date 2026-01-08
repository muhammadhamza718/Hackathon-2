import type { Metadata } from "next";
import { Geist, Geist_Mono } from "next/font/google";
import "./globals.css";
import { AuthProvider } from "@/contexts/AuthContext";
import { SidebarProvider, Sidebar } from "@/components/ui/sidebar";
import TodoChatKit from "@/components/chat/TodoChatKit";
import Script from "next/script";

const geistSans = Geist({
  variable: "--font-geist-sans",
  subsets: ["latin"],
});

const geistMono = Geist_Mono({
  variable: "--font-geist-mono",
  subsets: ["latin"],
});

export const metadata: Metadata = {
  title: "TaskManager - AI Powered",
  description: "Modern Task Management with AI Assistant",
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="en" suppressHydrationWarning>
      <body
        className={`${geistSans.variable} ${geistMono.variable} antialiased`}
      >
        <AuthProvider>
          <Script
            src="https://cdn.platform.openai.com/deployments/chatkit/chatkit.js"
            strategy="beforeInteractive"
          />
          <SidebarProvider>
            {children}
            <Sidebar side="right">
              <TodoChatKit />
            </Sidebar>
          </SidebarProvider>
        </AuthProvider>
      </body>
    </html>
  );
}

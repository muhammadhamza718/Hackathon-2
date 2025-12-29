import { auth } from "@/lib/auth";
import { NextRequest } from "next/server";

export async function GET(request: NextRequest) {
  try {
    const session = await auth.api.getSession({
      headers: request.headers,
    });

    if (session) {
      return Response.json({
        authenticated: true,
        user: session.user,
      });
    } else {
      return Response.json({
        authenticated: false,
        message: "No active session",
      });
    }
  } catch (error) {
    return Response.json({
      authenticated: false,
      error: error instanceof Error ? error.message : "Authentication check failed",
    });
  }
}
import { NextResponse } from 'next/server';

export async function GET() {
  // Perform readiness checks
  const startTime = Date.now();

  // Check if we can reach the backend API
  let backendReady = false;
  try {
    const backendResponse = await fetch(`${process.env.NEXT_PUBLIC_API_URL}/ready`, {
      method: 'GET',
      headers: {
        'Content-Type': 'application/json',
      },
    });
    backendReady = backendResponse.ok;
  } catch (error) {
    console.error('Backend readiness check failed:', error);
    backendReady = false;
  }

  // Calculate response time
  const responseTime = Date.now() - startTime;

  // Determine readiness status
  const isReady = backendReady;

  return NextResponse.json({
    status: isReady ? 'ready' : 'not ready',
    service: 'todo-chatbot-frontend',
    timestamp: new Date().toISOString(),
    response_time_ms: responseTime,
    checks: {
      backend_api: backendReady ? 'ready' : 'not ready',
    },
  });
}
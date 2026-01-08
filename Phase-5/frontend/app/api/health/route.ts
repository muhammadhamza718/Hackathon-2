import { NextResponse } from 'next/server';

export async function GET() {
  // Perform health checks
  const startTime = Date.now();

  // Check if we can reach the backend API
  let backendHealthy = false;
  try {
    const backendResponse = await fetch(`${process.env.NEXT_PUBLIC_API_URL}/health`, {
      method: 'GET',
      headers: {
        'Content-Type': 'application/json',
      },
    });
    backendHealthy = backendResponse.ok;
  } catch (error) {
    console.error('Backend health check failed:', error);
    backendHealthy = false;
  }

  // Calculate response time
  const responseTime = Date.now() - startTime;

  // Determine overall health status
  const isHealthy = backendHealthy;

  return NextResponse.json({
    status: isHealthy ? 'healthy' : 'unhealthy',
    service: 'todo-chatbot-frontend',
    timestamp: new Date().toISOString(),
    response_time_ms: responseTime,
    checks: {
      backend_api: backendHealthy ? 'healthy' : 'unhealthy',
    },
  });
}
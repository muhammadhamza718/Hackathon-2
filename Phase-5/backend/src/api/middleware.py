"""
Middleware for the Todo Backend API
"""
from typing import Callable
from fastapi import Request, Response
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.trustedhost import TrustedHostMiddleware
import time
import logging

logger = logging.getLogger(__name__)


class RequestLoggingMiddleware:
    """
    Middleware to log incoming requests
    """
    def __init__(self, app):
        self.app = app

    async def __call__(self, scope, receive, send):
        if scope["type"] != "http":
            return await self.app(scope, receive, send)

        request = Request(scope)
        start_time = time.time()

        async def send_wrapper(message):
            if message["type"] == "http.response.start":
                process_time = time.time() - start_time
                response = Response(
                    status_code=message["status"],
                    headers=message.get("headers", [])
                )
                logger.info(
                    f"{request.method} {request.url.path} - {response.status_code} - {process_time:.2f}s"
                )
            await send(message)

        return await self.app(scope, receive, send_wrapper)


def add_middleware(app):
    """
    Add all middleware to the FastAPI application
    """
    # CORS middleware
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],  # Should be configured properly in production
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    # Trusted host middleware
    app.add_middleware(TrustedHostMiddleware, allowed_hosts=["*"])

    # Request logging middleware
    app.middleware("http")(RequestLoggingMiddleware(app))
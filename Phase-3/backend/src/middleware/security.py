"""Security middleware for the Todo Chatbot API"""
from typing import Callable, Awaitable
from fastapi import Request, HTTPException, Response
from fastapi.responses import JSONResponse
import re
import time
from collections import defaultdict
from datetime import datetime, timedelta


class SecurityMiddleware:
    """Provides security middleware for the FastAPI application"""

    def __init__(self):
        # Rate limiting storage: {client_ip: [request_timestamps]}
        self.rate_limit_storage = defaultdict(list)
        self.rate_limit_window = 60  # 60 seconds
        self.rate_limit_max_requests = 100  # max requests per window

        # Common attack patterns to detect
        self.attack_patterns = [
            r"(?i)(union\s+select)",
            r"(?i)(drop\s+table)",
            r"(?i)(delete\s+from)",
            r"(?i)(insert\s+into)",
            r"(?i)(update\s+\w+\s+set)",
            r"(?i)(exec\s*\()",
            r"(?i)(execute\s*\()",
            r"(?i)(<script)",
            r"(?i)(javascript:)",
            r"(?i)(vbscript:)",
            r"(?i)(onload\s*=)",
            r"(?i)(onerror\s*=)",
            r"(?i)(<iframe)",
            r"(?i)(<object)",
            r"(?i)(<embed)",
            r"(?i)(<meta)",
            r"(?i)(document\.cookie)",
            r"(?i)(window\.location)",
            r"(?i)(eval\s*\()",
            r"(?i)(expression\s*\()",
        ]

    async def __call__(self, request: Request, call_next: Callable[..., Awaitable[Response]]) -> Response:
        """Process the request through security middleware"""
        client_ip = self.get_client_ip(request)

        # Check rate limiting
        if not self.check_rate_limit(client_ip):
            return JSONResponse(
                status_code=429,
                content={"detail": "Rate limit exceeded. Please try again later."}
            )

        # Sanitize request headers
        request = await self.sanitize_headers(request)

        # Check for malicious patterns in the request
        if await self.detect_malicious_patterns(request):
            return JSONResponse(
                status_code=400,
                content={"detail": "Request contains potentially malicious content."}
            )

        # Process the request
        response = await call_next(request)

        # Add security headers to the response
        response = await self.add_security_headers(response)

        return response

    def get_client_ip(self, request: Request) -> str:
        """Extract client IP from request"""
        # Check for X-Forwarded-For header (common in proxies/load balancers)
        forwarded = request.headers.get("x-forwarded-for")
        if forwarded:
            return forwarded.split(",")[0].strip()

        # Check for X-Real-IP header
        real_ip = request.headers.get("x-real-ip")
        if real_ip:
            return real_ip

        # Use the client host from the request
        return request.client.host if request.client else "unknown"

    def check_rate_limit(self, client_ip: str) -> bool:
        """Check if the client has exceeded the rate limit"""
        now = time.time()
        window_start = now - self.rate_limit_window

        # Remove old requests outside the window
        self.rate_limit_storage[client_ip] = [
            timestamp for timestamp in self.rate_limit_storage[client_ip]
            if timestamp > window_start
        ]

        # Check if we're under the limit
        if len(self.rate_limit_storage[client_ip]) < self.rate_limit_max_requests:
            # Add the current request
            self.rate_limit_storage[client_ip].append(now)
            return True

        return False

    async def sanitize_headers(self, request: Request) -> Request:
        """Sanitize request headers to prevent header injection"""
        # In FastAPI, headers are immutable, so we can only validate them
        # Here we'll just validate and log if there are issues
        dangerous_headers = [
            'x-forwarded-for',
            'x-real-ip',
            'x-client-ip',
            'x-originating-ip',
            'x-remote-ip',
            'x-remote-addr',
            'x-proxy-user-ip',
            'x-original-forwarded-for'
        ]

        for header, value in request.headers.items():
            if header.lower() in dangerous_headers:
                # Validate IP address format
                if not self.is_valid_ip(value.split(',')[0].strip()):
                    # Log potential header injection attempt
                    print(f"Potential header injection detected in {header}: {value}")

        return request

    def is_valid_ip(self, ip_str: str) -> bool:
        """Validate IP address format"""
        import ipaddress
        try:
            ipaddress.ip_address(ip_str)
            return True
        except ValueError:
            # Check for localhost variations
            if ip_str in ['localhost', '127.0.0.1', '::1']:
                return True
            return False

    async def detect_malicious_patterns(self, request: Request) -> bool:
        """Detect malicious patterns in the request"""
        # Check headers
        for header, value in request.headers.items():
            if self.contains_attack_pattern(value):
                return True

        # For body content, we need to read it carefully
        if request.method in ["POST", "PUT", "PATCH"]:
            try:
                # Read the body content
                body_bytes = await request.body()
                body_str = body_bytes.decode('utf-8', errors='ignore')

                if self.contains_attack_pattern(body_str):
                    return True
            except:
                # If we can't read the body, that's suspicious
                return True

        # Check query parameters
        for param, value in request.query_params.items():
            if self.contains_attack_pattern(str(value)):
                return True

        # Check path parameters
        if self.contains_attack_pattern(request.url.path):
            return True

        return False

    def contains_attack_pattern(self, text: str) -> bool:
        """Check if text contains any attack patterns"""
        if not text or not isinstance(text, str):
            return False

        for pattern in self.attack_patterns:
            if re.search(pattern, text):
                return True

        return False

    async def add_security_headers(self, response: Response) -> Response:
        """Add security headers to the response"""
        # Set security headers
        response.headers["X-Content-Type-Options"] = "nosniff"
        response.headers["X-Frame-Options"] = "DENY"
        response.headers["X-XSS-Protection"] = "1; mode=block"
        response.headers["Strict-Transport-Security"] = "max-age=31536000; includeSubDomains"
        response.headers["Referrer-Policy"] = "no-referrer"
        response.headers["Content-Security-Policy"] = "default-src 'self'; script-src 'self'; style-src 'self' 'unsafe-inline';"

        return response


# Create a singleton instance
security_middleware = SecurityMiddleware()
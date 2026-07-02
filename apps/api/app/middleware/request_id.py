"""
Request ID Middleware

Generates a unique request ID for every incoming request.
"""

import time
import uuid

from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request


class RequestIDMiddleware(BaseHTTPMiddleware):
    """
    Adds a unique request ID and request start time
    to every incoming request.
    """

    async def dispatch(self, request: Request, call_next):
        request.state.request_id = str(uuid.uuid4())
        request.state.start_time = time.perf_counter()

        response = await call_next(request)

        response.headers["X-Request-ID"] = request.state.request_id

        return response
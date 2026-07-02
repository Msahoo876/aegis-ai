"""
Request Logging Middleware

Logs every incoming HTTP request with
its processing time and request ID.
"""

import time

from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request

from app.core.logging import logger


class RequestLoggingMiddleware(BaseHTTPMiddleware):
    """
    Logs every HTTP request.
    """

    async def dispatch(self, request: Request, call_next):

        start_time = time.perf_counter()

        response = await call_next(request)

        process_time = (time.perf_counter() - start_time) * 1000

        request_id = getattr(request.state, "request_id", "N/A")

        logger.info(
            (
                f"Request ID={request_id} | "
                f"{request.method} {request.url.path} | "
                f"Status={response.status_code} | "
                f"Duration={process_time:.2f} ms"
            )
        )

        return response
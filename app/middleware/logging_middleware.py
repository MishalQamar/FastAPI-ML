from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
import logging


class LoggingMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        body = await request.body()
        logging.info(
            "Request: %s %s headers=%s body=%s",
            request.method,
            request.url,
            dict(request.headers),
            body.decode("utf-8", errors="replace"),
        )
        response = await call_next(request)
        return response
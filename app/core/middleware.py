import time
import logging
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request

logger = logging.getLogger("api")


class LoggingMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        start_time = time.time()

        logger.info(f"➡️ {request.method} {request.url.path}")

        try:
            response = await call_next(request)
        except Exception as e:
            logger.exception("Unhandled error during request")
            raise e

        process_time = round((time.time() - start_time) * 1000, 2)

        logger.info(
            f"⬅️ {request.method} {request.url.path} "
            f"Status: {response.status_code} "
            f"Time: {process_time}ms"
        )

        return response

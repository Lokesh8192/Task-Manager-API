import logging
from fastapi import Request, HTTPException
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from starlette.exceptions import HTTPException as StarletteHTTPException

from app.core.response import error_response

logger = logging.getLogger("api")


# 🔹 HTTP Exception
async def http_exception_handler(request: Request, exc: StarletteHTTPException):
    logger.warning(f"HTTP {exc.status_code} - {exc.detail}")

    return JSONResponse(
        status_code=exc.status_code,
        content=error_response(exc.detail).dict(),
    )


# 🔹 Validation Exception
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    logger.warning(f"Validation error: {exc.errors()}")

    errors = [
        {
            "field": ".".join(map(str, err["loc"])),
            "message": err["msg"],
        }
        for err in exc.errors()
    ]

    return JSONResponse(
        status_code=422,
        content=error_response("Validation failed", errors).dict(),
    )


# 🔹 General Exception
async def general_exception_handler(request: Request, exc: Exception):
    logger.exception("Unhandled server error")

    return JSONResponse(
        status_code=500,
        content=error_response("Internal Server Error").dict(),
    )

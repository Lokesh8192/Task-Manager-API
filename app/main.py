from fastapi import FastAPI
from app.database import Base, engine, SessionLocal
from app.core.init_admin import create_default_admin
from app.core.logging_config import setup_logging
from app.core.middleware import LoggingMiddleware
from app.routers import task_router
from app.routers import auth_router
from app.routers import admin_router
from app.core.config import settings

from app.core.exception_handler import (
    http_exception_handler,
    validation_exception_handler,
    general_exception_handler,
)

from fastapi.exceptions import RequestValidationError
from starlette.exceptions import HTTPException as StarletteHTTPException
from fastapi.middleware.cors import CORSMiddleware


Base.metadata.create_all(bind=engine)

setup_logging()

app = FastAPI(title="Task Manager API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # or frontend URL later
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.add_middleware(LoggingMiddleware)


# Create default admin on startup
@app.on_event("startup")
def startup_event():
    db = SessionLocal()
    try:
        create_default_admin(db)
    finally:
        db.close()


# Register handlers
app.add_exception_handler(StarletteHTTPException, http_exception_handler)
app.add_exception_handler(RequestValidationError, validation_exception_handler)
app.add_exception_handler(Exception, general_exception_handler)

app.include_router(admin_router.router)
app.include_router(auth_router.router)
app.include_router(task_router.router)

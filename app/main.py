"""This module contains the main FastAPI application."""

from contextlib import asynccontextmanager

import logfire
from anyio import to_thread
from fastapi import FastAPI
from fastapi.exceptions import RequestValidationError
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.gzip import GZipMiddleware
from fastapi.responses import ORJSONResponse

from app.common.exceptions import (
    BadGatewayError,
    CustomHTTPException,
    InternalServerError,
)
from app.core.database import get_client, setup_mongodb
from app.core.handlers import (
    bad_gateway_error_exception_handler,
    base_exception_handler,
    custom_http_exception_handler,
    internal_server_error_exception_handler,
    request_validation_exception_handler,
)
from app.core.settings import get_settings
from app.sample_module.apis import router as example_router

# Globals
settings = get_settings()


# Lifespan (startup, shutdown)
@asynccontextmanager
async def lifespan(_: FastAPI):
    """This is the startup and shutdown code for the FastAPI application."""
    # Startup code
    print("Starting server...")  # SAO Reference

    # Bigger Threadpool i.e you send a bunch of requests it will handle a max of 1000 at a time, the default is 40
    print("Increasing threadpool...")
    limiter = to_thread.current_default_thread_limiter()
    limiter.total_tokens = 1000

    # Setup mongodb
    print("Setting up mongodb...")
    await setup_mongodb()

    # Shutdown
    yield
    print("Shutting down server...")


app = FastAPI(
    title="Heavyweight FastAPI",
    lifespan=lifespan,
    default_response_class=ORJSONResponse,
    docs_url="/",
    contact={
        "name": "GrandGale Technologies",
        "url": "https://github.com/GrandGaleTechnologies",
        "email": "contact@grandgale.tech",
    },
)
# Variables
origins = ["*"]

# Middlewares
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.add_middleware(
    GZipMiddleware,
    minimum_size=5000,  # Minimum size of the response before it is compressed in bytes
)


# Exception Handlers
app.add_exception_handler(Exception, base_exception_handler)
app.add_exception_handler(RequestValidationError, request_validation_exception_handler)  # type: ignore
app.add_exception_handler(InternalServerError, internal_server_error_exception_handler)  # type: ignore
app.add_exception_handler(BadGatewayError, bad_gateway_error_exception_handler)  # type: ignore
app.add_exception_handler(CustomHTTPException, custom_http_exception_handler)  # type: ignore


# Logfire Config
if settings.LOGFIRE_TOKEN:
    logfire.configure(
        service_name="heavyweight-mongodb",
        token=settings.LOGFIRE_TOKEN,
        environment="dev" if settings.DEBUG else "prod",
    )
    logfire.instrument_fastapi(app)
    logfire.instrument_pymongo()


# Health Check
@app.get("/health", status_code=200, include_in_schema=False)
async def health_check():
    """
    This is the health check endpoint
    """
    get_client()
    return {"status": "ok"}


# Routers
app.include_router(example_router, prefix="/users", tags=["Example Docs"])

from fastapi import FastAPI, status
from fastapi.requests import Request
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.trustedhost import TrustedHostMiddleware

import time
import logging


def register_middleware(app: FastAPI):
    # CORS Middleware
    app.add_middleware(
        CORSMiddleware,
        allow_origins = ['*'],
        allow_methods = ['*'],
        allow_headers = ['*'],
        allow_credentials = True
    )

    # Trusted Host Middleware
    app.add_middleware(
        TrustedHostMiddleware,
        allowed_hosts=["*"],
    )

    # Logging Middleware
    @app.middleware("http")
    async def log_requests(request: Request, call_next):
        start_time = time.time()
        response = await call_next(request)
        duration = time.time() - start_time
        logging.info(f"Request: {request.method} {request.url} completed in {duration:.2f}s")
        return response
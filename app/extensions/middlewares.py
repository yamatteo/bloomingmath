from datetime import datetime
from logging import info, error
from traceback import format_exc

from fastapi import FastAPI
from fastapi.exceptions import RequestValidationError, HTTPException
from starlette.middleware.cors import CORSMiddleware
from starlette.requests import Request
from starlette.responses import PlainTextResponse


def log_to_file(title):
    with open("server_error.log", "a") as f:
        f.write("\n" + "#" * 40 + "\n")
        f.write(f"{title} {datetime.now().ctime()}\n\n")
        for line in format_exc().splitlines():
            f.write(line + "\n")
        f.write("#" * 40 + "\n")


async def validation_exception_handler(request: Request, exc: RequestValidationError) -> PlainTextResponse:
    # log_to_file("Invalid request")
    info(f"Tamed exception >> 422 see below...\n{str(exc)}")
    return PlainTextResponse(str(exc), status_code=422)


async def http_exception_handler(request: Request, exc: HTTPException) -> PlainTextResponse:
    # log_to_file("HTTP Exception")
    info(f"Tamed exception >> {str(exc.status_code)} {str(exc.detail)}")
    return PlainTextResponse(str(exc), status_code=exc.status_code, headers=exc.headers)


async def server_error_handler(request: Request, exc: Exception) -> PlainTextResponse:
    log_to_file("UNHANDLED EXCEPTION")
    error(f"Unhandled exception >> str(exc)")
    return PlainTextResponse(str(exc), status_code=500)


class MiddlewareEngine:
    @staticmethod
    def init_app(app: FastAPI):
        app.add_middleware(
            CORSMiddleware,
            allow_origins=[
                "http://127.0.0.1:8080", "https://127.0.0.1:8080",
                "http://127.0.0.1:8000", "https://127.0.0.1:8000",
                "http://bloomingmath.herokuapp.com", "http://bloomingmath.herokuapp.com"
            ],
            allow_credentials=True,
            allow_methods=["GET", "POST"],
            allow_headers=["Accept", "Accept-Language", "Content-Language", "Content-Type", "Authorization",
                           "Accept-Encoding", "Cache-Control", "Connection", "Content-Length", "Cookie", "Host",
                           "Origin", "Pragma", "Referer", "Sec-Fetch-Mode", "Sec-Fetch-Site", "User-Agent"],
        )
        app.add_exception_handler(RequestValidationError, validation_exception_handler)
        app.add_exception_handler(HTTPException, http_exception_handler)
        app.add_exception_handler(Exception, server_error_handler)


middleware_engine = MiddlewareEngine()

# @app.middleware("http")
# async def custom_middleware(request: Request, call_next):
#     # Something before
#     response = await call_next(request)
#     #something after
#     return response

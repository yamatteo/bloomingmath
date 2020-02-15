from os import getenv

from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException
from fastapi.exceptions import RequestValidationError
from starlette.requests import Request
from starlette.staticfiles import StaticFiles
from starlette.responses import PlainTextResponse
from starlette.middleware.cors import CORSMiddleware

from extensions.mongo import mongo_engine
from extensions.security import generate_salt
from routers import *
from models import *
from starlette.responses import FileResponse, HTMLResponse

load_dotenv()
FASTAPI_ENVIRONMENT = getenv("FASTAPI_ENVIRONMENT")
MONGODB_URI = getenv("MONGODB_URI")
MAX_FIND = int(getenv("MAX_FIND", 50))

# Create fastapi application with rendering engine, motor mongodb connection, static files and signaling system
app = FastAPI(title="App title")

app.mount("/static", StaticFiles(directory="../dist"), name="static")
mongo_engine.init_app(app, uri=MONGODB_URI, env=FASTAPI_ENVIRONMENT)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request, exc):
    print("Exception >>", exc)
    return PlainTextResponse(str(exc), status_code=422)


@app.exception_handler(HTTPException)
async def http_exception_handler(request, exc):
    print("Exception >>", str(exc.status_code), str(exc.detail))
    return PlainTextResponse(str(exc), status_code=exc.status_code, headers=exc.headers)


@app.exception_handler(Exception)
async def server_error_handler(request, exc):
    from datetime import datetime
    from traceback import format_exc
    with open("server_error.log", "a") as f:
        f.write("\n" + "#" * 40 + "\n")
        f.write(f"UNHANDLED ERROR {datetime.now().ctime()}\n\n")
        for line in format_exc().splitlines():
            f.write(line + "\n")
        f.write("#" * 40 + "\n")
    return PlainTextResponse(str(exc), status_code=500)


@app.get("/", response_class=HTMLResponse)
async def read_root(request: Request):
    with open("../dist/index.html", "r") as f:
        return f.read()


# @app.get("/ping")
# async def ping():
#     await Ping.insert_one({})
#     return {"pings": len(await Ping.find({}))}


# Add middlewares
# @app.middleware("http")
# async def next_url_redirect(request: Request, call_next):
#     """Check if 'next' query parameter is present in the request. If so, inject it as next url in an eventual Http303
#     response. """
#     try:
#         url = request.query_params["next"]
#         assert isinstance(url, str)
#         assert len(url) > 0
#         assert url[0] == "/"
#     except (AttributeError, KeyError, AssertionError):
#         url = None
#
#     response = await call_next(request)
#     if url is not None and response.status_code == 303:
#         response.headers["location"] = url
#     return response


# app.add_middleware(SessionMiddleware, secret_key=generate_salt())

# Include routers
# app.include_router(main.router)
# app.include_router(users.router, prefix="/users")
# app.include_router(groups.router, prefix="/groups")
# app.include_router(contents.router, prefix="/contents")
# app.include_router(admin.router, prefix="/admin")

if __name__ == "__main__":
    from uvicorn import run

    run(app, port=8080)

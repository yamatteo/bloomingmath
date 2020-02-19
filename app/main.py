from os import getenv

from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException
from fastapi.exceptions import RequestValidationError
from starlette.middleware.cors import CORSMiddleware
from routers import users, contents, nodes, groups
from starlette.responses import HTMLResponse
from starlette.responses import PlainTextResponse
from starlette.staticfiles import StaticFiles

from fastapi.security import OAuth2PasswordBearer
from extensions.mongo import mongo_engine

load_dotenv()
FASTAPI_ENVIRONMENT = getenv("FASTAPI_ENVIRONMENT")
MONGODB_URI = getenv("MONGODB_URI")
MAX_FIND = int(getenv("MAX_FIND", 50))

# Create fastapi application with rendering engine, motor mongodb connection, static files and signaling system
app = FastAPI(title="Bloomingmath")

app.mount("/static", StaticFiles(directory="../dist"), name="static")
mongo_engine.init_app(app, uri=MONGODB_URI, env=FASTAPI_ENVIRONMENT)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/users/urlencode_login")


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
async def read_root():
    with open("../dist/index.html", "r") as f:
        return f.read()

app.include_router(users.router, prefix="/users", tags=["users"])
app.include_router(nodes.router, prefix="/nodes", tags=["nodes"])
app.include_router(contents.router, prefix="/contents", tags=["contents"])
app.include_router(groups.router, prefix="/groups", tags=["groups"])

if __name__ == "__main__":
    from uvicorn import run

    run(app, port=8010)

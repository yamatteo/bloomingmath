from os import getenv

from dotenv import load_dotenv
from fastapi import FastAPI
from starlette.responses import HTMLResponse
from starlette.staticfiles import StaticFiles

from extensions.middlewares import middleware_engine
from extensions.mongo import mongo_engine
from routers import users, contents, nodes, groups

load_dotenv()
FASTAPI_ENVIRONMENT = getenv("FASTAPI_ENVIRONMENT", "development")
MONGODB_URI = getenv("MONGODB_URI", "mongodb://localhost:27017")
MAX_FIND = int(getenv("MAX_FIND", 50))

# App's title is used by mongo extension to locate the database
app = FastAPI(title="Bloomingmath")

app.mount("/static", StaticFiles(directory="../dist"), name="static")
mongo_engine.init_app(app, uri=MONGODB_URI, env=FASTAPI_ENVIRONMENT)
middleware_engine.init_app(app)
app.mount("/stag/static", StaticFiles(directory="../stag"), name="stag_static")


@app.get("/", response_class=HTMLResponse)
async def read_root():
    with open("../dist/index.html", "r") as f:
        return f.read()

@app.get("/stag", response_class=HTMLResponse)
async def read_stag():
    with open("../stag/index.html", "r") as f:
        return f.read()


@app.get("/reset_development_database")
async def reset_development_database():
    if FASTAPI_ENVIRONMENT == "development":
        from tests.conftest import populate

        await populate()
    else:
        raise RuntimeError("Not in development environment!")


app.include_router(users.router, prefix="/users", tags=["users"])
app.include_router(nodes.router, prefix="/nodes", tags=["nodes"])
app.include_router(contents.router, prefix="/contents", tags=["contents"])
app.include_router(groups.router, prefix="/groups", tags=["groups"])


if __name__ == "__main__":
    from uvicorn import run

    run(app, port=8010)

from typing import List

from fastapi import APIRouter, Depends, UploadFile, Form, File
from starlette.responses import StreamingResponse, FileResponse

from models import Content
from routers import admin_only
from schemas import *

router = APIRouter()


@router.api_route("/browse", methods=["GET", "POST"], dependencies=[Depends(admin_only)])
async def browse_contents() -> List[Content]:
    return await Content.find()


@router.api_route("/read", methods=["GET", "POST"], dependencies=[Depends(admin_only)])
async def read_content(find: ContentFind) -> Optional[Content]:
    return await Content.find_one(find=find.dict(exclude_unset=True))


@router.api_route("/add", methods=["GET", "POST"])
async def add_content(short: str = Form(...), long: Optional[str] = Form(None), filetype: str = Form(...),
                      content: UploadFile = File(...)) -> Content:
    if long is None:
        data = ContentAdd(short=short, filetype=filetype)
    else:
        data = ContentAdd(short=short, long=long, filetype=filetype)
    return await Content.insert_one(content=content, data=data.dict(exclude_unset=True))


@router.api_route("/edit", methods=["GET", "POST"], dependencies=[Depends(admin_only)])
async def edit_content(find: ContentFind, data: ContentEdit) -> Optional[Content]:
    return await Content.find_one_and_set(find=find.dict(exclude_unset=True), data=data.dict(exclude_unset=True))


@router.api_route("/delete", methods=["GET", "POST"], dependencies=[Depends(admin_only)])
async def delete_content(find: ContentFind) -> None:
    await Content.delete(find=find.dict(exclude_unset=True))

from typing import Callable, List, Optional

from fastapi import APIRouter, Depends
from starlette.requests import Request
from starlette.responses import Response

from models import User, Node, Group, Content
from extensions.mongo import mongo_engine
from pprint import pprint
import tempfile
from bson import ObjectId

router = APIRouter()


@router.get("/{content_id}")
async def read_content(content_id: str, request: Request):
    with tempfile.TemporaryFile() as file:
        grid_obj = (await mongo_engine.fs.find({"_id": ObjectId(content_id)}).to_list(length=5))[0]
        content = Content.parse_obj(grid_obj["metadata"])
        await mongo_engine.fs.download_to_stream(ObjectId(content_id), file)
        pprint(content)
        file.seek(0)
        data = file.read()
    return Response(content=data, media_type=f"application/{content.filetype}")


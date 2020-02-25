from fastapi import UploadFile, Form, File

import tempfile
from typing import List, Optional

from bson import ObjectId
from fastapi import APIRouter, Depends
from fastapi import UploadFile, Form, File
from starlette.requests import Request
from starlette.responses import Response

from extensions.mongo import mongo_engine
from models import Content
from routers import admin_only
from schemas import *

router = APIRouter()


@router.api_route("/browse", methods=["POST"], dependencies=[Depends(admin_only)])
async def browse_contents() -> List[Content]:
    return await Content.find()


@router.api_route("/read", methods=["POST"], dependencies=[Depends(admin_only)])
async def read_content(find: ContentFind) -> Optional[Content]:
    return await Content.find_one(find=find.dict(exclude_unset=True))


@router.api_route("/add", methods=["POST"])
async def add_content(short: str = Form(...), long: Optional[str] = Form(None), filetype: str = Form(...),
                      content: UploadFile = File(...)) -> Content:
    if long is None:
        data = ContentAdd(short=short, filetype=filetype)
    else:
        data = ContentAdd(short=short, long=long, filetype=filetype)
    return await Content.insert_one(content=content, data=data.dict(exclude_unset=True))


@router.api_route("/edit", methods=["POST"], dependencies=[Depends(admin_only)])
async def edit_content(find: ContentFind, data: ContentEdit) -> Optional[Content]:
    return await Content.find_one_and_set(find=find.dict(exclude_unset=True), data=data.dict(exclude_unset=True))


@router.api_route("/delete", methods=["POST"], dependencies=[Depends(admin_only)])
async def delete_content(find: ContentFind) -> None:
    await Content.delete(find=find.dict(exclude_unset=True))


@router.get("/{content_id}")
async def read_content(content_id: str):
    content = await Content.find_one({"id": content_id})
    data: bytes = await Content.read(content_id)
    return Response(content=data, media_type=f"application/{content.filetype}", headers={
        "Connection": "keep-alive",
        "Content-Disposition": "attachment"
    })


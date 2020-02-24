from fastapi import APIRouter, Depends, UploadFile, Form, File

from tempfile import TemporaryFile
from typing import List

from bson import ObjectId
from fastapi import APIRouter, Depends, UploadFile, Form, File
from starlette.responses import Response

from extensions.mongo import mongo_engine
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


@router.get("/{content_id}")
async def download_content(content_id: str):
    # TODO shift the file interface inside mongodb_orm
    content = await Content.find_one({"id": content_id})
    data = await Content.read(content_id)
    return Response(content=data, media_type=f"application/{content.filetype}", headers={
        "Content-Disposition": f"attachment; filename=\"{content.original_filename}\""
    })

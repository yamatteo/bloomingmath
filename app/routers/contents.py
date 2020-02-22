from typing import Optional

from fastapi import APIRouter, Depends, UploadFile, Form, File

from models import User, Node, Group, Content
from routers import get_current_user, admin_only
from extensions.mongo import mongo_engine
from tempfile import TemporaryFile
from starlette.responses import Response
from bson import ObjectId
from typing import List
from schemas import *

router = APIRouter()


@router.get("/{content_id}")
async def download_content(content_id: str):
    # TODO shift the file interface inside mongodb_orm
    with TemporaryFile() as file:
        fsfile = await mongo_engine.db["fs.files"].find_one({"_id": ObjectId(content_id)})
        content = Content.parse_obj(fsfile["metadata"])
        await mongo_engine.fs.download_to_stream(ObjectId(content_id), file)
        file.seek(0)
        data = file.read()
    return Response(content=data, media_type=f"application/{content.filetype}", headers={
        "Content-Disposition": f"attachment; filename=\"{fsfile['filename']}\""
    })


@router.api_route("/browse", methods=["GET", "POST"], dependencies=[Depends(admin_only)])
async def browse_contents() -> List[Content]:
    return await Content.find()


@router.api_route("/read", methods=["GET", "POST"], dependencies=[Depends(admin_only)])
async def read_content(find: ContentFind) -> Optional[Content]:
    return await Content.find_one(find=find.dict(exclude_unset=True))


@router.api_route("/add", methods=["GET", "POST"], dependencies=[Depends(admin_only)])
async def add_content(data: ContentAdd, content: UploadFile = File(...)) -> Content:
    return await Content.insert_one(content=content, data=data.dict(exclude_unset=True))


@router.api_route("/edit", methods=["GET", "POST"], dependencies=[Depends(admin_only)])
async def edit_content(find: ContentFind, data: ContentEdit) -> Optional[Content]:
    return await Content.find_one_and_set(find=find.dict(exclude_unset=True), data=data.dict(exclude_unset=True))


@router.api_route("/delete", methods=["GET", "POST"], dependencies=[Depends(admin_only)])
async def delete_content(find: ContentFind) -> None:
    await Content.delete(find=find.dict(exclude_unset=True))

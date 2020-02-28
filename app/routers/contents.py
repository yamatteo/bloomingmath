from typing import List

from fastapi import APIRouter, Depends
from fastapi import UploadFile, File
from starlette.responses import Response

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
async def add_content(data: ContentAdd) -> Content:
    return await Content.insert_one(data.dict(exclude_unset=True))


@router.api_route("/edit", methods=["POST"], dependencies=[Depends(admin_only)])
async def edit_content(find: ContentFind, data: ContentEdit) -> Optional[Content]:
    return await Content.find_one_and_set(find=find.dict(exclude_unset=True), data=data.dict(exclude_unset=True))


@router.api_route("/delete", methods=["POST"], dependencies=[Depends(admin_only)])
async def delete_content(find: ContentFind) -> None:
    await Content.delete_one(find=find.dict(exclude_unset=True))


@router.post("/upload/{content_id}", dependencies=[Depends(admin_only)])
async def upload_content(content_id: str, data: UploadFile = File(...)) -> Content:
    content = await Content.find_one(find={"id": content_id})
    return await content.upload(data=data)


@router.get("/download/{content_id}")
async def download_content(content_id: str):
    content = await Content.find_one({"id": content_id})
    data: bytes = await content.download()
    return Response(content=data, media_type=f"application/{content.filetype}", headers={
        "Connection": "keep-alive",
        "Content-Disposition": "attachment"
    })

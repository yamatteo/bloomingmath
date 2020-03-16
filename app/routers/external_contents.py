from typing import List

from fastapi import APIRouter, Depends, Body
from fastapi import UploadFile, File
from starlette.responses import Response

from models import ExternalContent
from routers import admin_only
from schemas import *

router = APIRouter()


@router.post("/browse", dependencies=[Depends(admin_only)])
async def browse_contents() -> List[ExternalContent]:
    return await ExternalContent.find()


@router.post("/read", dependencies=[Depends(admin_only)])
async def read_content(find: ExternalContentFind) -> Optional[ExternalContent]:
    return await ExternalContent.find_one(find=find.dict(exclude_unset=True))


@router.post("/add", dependencies=[Depends(admin_only)])
async def add_content(data: ExternalContentAdd) -> ExternalContent:
    return await ExternalContent.insert_one(data.dict(exclude_unset=True))


@router.post("/edit", dependencies=[Depends(admin_only)])
async def edit_content(find: ExternalContentFind, data: ExternalContentEdit) -> Optional[ExternalContent]:
    return await ExternalContent.find_one_and_set(find=find.dict(exclude_unset=True), data=data.dict(exclude_unset=True))


@router.post("/delete", dependencies=[Depends(admin_only)])
async def delete_content(find: ExternalContentFind) -> None:
    await ExternalContent.delete_one(find=find.dict(exclude_unset=True))

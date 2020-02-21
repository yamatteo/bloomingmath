from typing import Optional

from fastapi import APIRouter, Depends, UploadFile, Form, File

from models import User, Node, Group, Content
from routers import get_current_user, admin_only
from extensions.mongo import mongo_engine
from tempfile import TemporaryFile
from starlette.responses import Response
from bson import ObjectId

router = APIRouter()


@router.get("/{content_id}")
async def read_content(content_id: str):
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


@router.get("/browse")
async def browse_contents():
    return [content.export() for content in await Content.find()]


@router.get("/read")
async def read_content(content_id: str):
    content = await Content.find_one({"id": content_id})
    return content.export()


@router.post("/add")
async def add_content(content_data: UploadFile = File(...), content_short: str = Form(...),
                      content_filetype: str = Form(...), admin: User = Depends(admin_only)):
    print("Adding...")
    file_id = await Content.insert_one({"short": content_short, "filetype": content_filetype})
    grid_in = mongo_engine.fs.open_upload_stream_with_id(
        file_id,
        content_data.filename,
        metadata={"short": content_short, "filetype": content_filetype, "id": file_id, "collection_name": "contents"}
    )
    with content_data.file as f:
        await grid_in.write(f.read())
        await grid_in.close()
    return {"new content's id": str(file_id)}


@router.post("/edit")
async def edit_content(content_id: str, short: Optional[str] = None, long: Optional[str] = None,
                       filetype: Optional[str] = None, admin: User = Depends(admin_only)):
    assert admin is not None
    data = {}
    if short is not None:
        data["short"] = short
    if long is not None:
        data["long"] = long
    if filetype is not None:
        data["filetype"] = filetype
    return await Content.find_one_and_set(find={"id": content_id}, data=data)


@router.post("/delete")
async def delete_content(content_id: str, admin: User = Depends(admin_only)):
    assert admin is not None
    return await Content.delete_one({"id": content_id})

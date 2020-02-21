from typing import List, Optional

from fastapi import APIRouter, Depends, Body

from models import User, Group, Node
from routers import get_current_user, admin_only, Inbody

#
router = APIRouter()


#

@router.post("/push_self")
async def push_self(group_id: str = Body(..., embed=True), current_user: User = Depends(get_current_user)):
    await Group.find_one_and_add_to_set(find={"id": group_id}, data={"members": current_user.self_ref()})
    return False


@router.post("/pull_self")
async def pull_self(group_id: str = Body(..., embed=True), current_user: User = Depends(get_current_user)):
    await Group.find_one_and_pull(find={"id": group_id}, data={"members": current_user.self_ref()})
    return False


@router.post("/push_node")
async def push_self(group_id: str = Body(..., embed=True), node_id: str = Body(..., embed=True),
                    admin: User = Depends(admin_only)):
    assert admin is not None
    group = await Group.find_one_and_add_to_set(
        find={"id": group_id},
        data={"nodes": Node.ref(node_id)}
    )
    return group.export()


@router.post("/pull_node")
async def pull_self(group_id: str = Body(..., embed=True), node_id: str = Body(..., embed=True),
                    admin: User = Depends(admin_only)):
    assert admin is not None
    group = await Group.find_one_and_pull(
        find={"id": group_id},
        data={"nodes": Node.ref(node_id)}
    )
    return group.export()


@router.get("/browse")
async def browse_groups():
    return [group.export() for group in await Group.find({})]


@router.get("/read")
async def read_group(group_id: str):
    return await Group.find_one({"id": group_id})


@router.post("/edit")
async def edit_group(group_id: str = Body(..., embed=True), short: Optional[str] = Body(None, embed=True),
                     long: Optional[str] = Body(None, embed=True),
                     members_ids: Optional[List[str]] = Body(None, embed=True),
                     nodes_ids: Optional[List[str]] = Body(None, embed=True), admin: User = Depends(admin_only)):
    assert admin is not None
    data = {}
    if short is not None:
        data["short"] = short
    if long is not None:
        data["long"] = long
    if members_ids is not None:
        data["members"] = [{"id": _id, "collection_name": "users"} for _id in members_ids]
    if nodes_ids is not None:
        data["nodes"] = [{"id": _id, "collection_name": "nodes"} for _id in nodes_ids]
    return (await Group.find_one_and_set(find={"id": group_id}, data=data)).export()


@router.post("/add")
async def add_group(short: str = Inbody(...), long: str = Inbody(...), admin: User = Depends(admin_only)):
    assert admin is not None
    return await Group.insert_one({"short": short, "long": long})


@router.post("/delete")
async def delete_group(group_id: str, admin: User = Depends(admin_only)):
    assert admin is not None
    return await Group.delete_one({"id": group_id})

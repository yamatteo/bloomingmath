from typing import List, Optional

from fastapi import APIRouter, Depends, Body

from models import User, Group, Node
from routers import get_current_user, admin_only, Inbody
from schemas import GroupEdit, GroupFind, GroupAdd

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


@router.post("/browse", dependencies=[Depends(admin_only)])
async def browse_groups():
    return await Group.find()


@router.post("/read", dependencies=[Depends(admin_only)])
async def read_group(find: GroupFind, with_nodes: bool = Body(False), with_other_nodes: bool = Body(False)):
    group = await Group.find_one(find=find.dict(exclude_unset=True))
    group_export = group.dict()
    if with_nodes:
        group_export["nodes"] = await Node.find({"id": {"$in": [ node.id for node in group.nodes ]}})
    if with_other_nodes:
        group_export["other_nodes"] = await Node.find({"id": {"$nin": [ node.id for node in group.nodes ]}})
    return group_export


@router.post("/edit", dependencies=[Depends(admin_only)])
async def edit_group(find: GroupFind, data: GroupEdit):
    return await Group.find_one_and_set(find=find.dict(exclude_unset=True), data=data.dict(exclude_unset=True))


@router.post("/add", dependencies=[Depends(admin_only)])
async def add_group(data: GroupAdd) -> Group:
    return await Group.insert_one(data.dict(exclude_unset=True))


@router.post("/delete", dependencies=[Depends(admin_only)])
async def delete_group(find: GroupFind):
    print("find", find)
    return await Group.delete_one(find=find.dict(exclude_unset=True))

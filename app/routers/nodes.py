from typing import Optional

from fastapi import APIRouter, Depends, Body

from models import User, Content, Node, Group, ExternalContent
from routers import get_current_user, admin_only
from schemas import NodeAdd, NodeEdit, NodeFind

#
router = APIRouter()


@router.post("/push_content")
async def push_content(node_id: str = Body(..., embed=True), content_id: str = Body(..., embed=True),
                       admin: User = Depends(admin_only)):
    assert admin is not None
    node = await Node.find_one_and_add_to_set(
        find={"id": node_id},
        data={"contents": Content.ref(content_id)}
    )
    return node.export()


@router.post("/pull_content")
async def pull_content(node_id: str = Body(..., embed=True), content_id: str = Body(..., embed=True),
                    admin: User = Depends(admin_only)):
    assert admin is not None
    node = await Node.find_one_and_pull(
        find={"id": node_id},
        data={"contents": Content.ref(content_id)}
    )
    return node.export()


@router.post("/push_external_content")
async def push_external_content(node_id: str = Body(..., embed=True), external_content_id: str = Body(..., embed=True),
                       admin: User = Depends(admin_only)):
    assert admin is not None
    node = await Node.find_one_and_add_to_set(
        find={"id": node_id},
        data={"external_contents": ExternalContent.ref(external_content_id)}
    )
    return node.export()


@router.post("/pull_external_content")
async def pull_external_content(node_id: str = Body(..., embed=True), external_content_id: str = Body(..., embed=True),
                    admin: User = Depends(admin_only)):
    assert admin is not None
    node = await Node.find_one_and_pull(
        find={"id": node_id},
        data={"external_contents": ExternalContent.ref(external_content_id)}
    )
    return node.export()


@router.get("/current")
async def current_nodes(current_user: User = Depends(get_current_user)):
    groups = await Group.find({"members": current_user})
    nodes_ids = [node.id for group in groups for node in group.nodes]
    return [node.export() for node in await Node.find({"id": {"$in": nodes_ids}})]


@router.post("/browse", dependencies=[Depends(admin_only)])
async def browse_nodes():
    return await Node.find()


@router.post("/read", dependencies=[Depends(admin_only)])
async def read_node(find: NodeFind, with_contents: bool = Body(False), with_other_contents: bool = Body(False)):
    node = await Node.find_one(find=find.dict(exclude_unset=True))
    node_export = node.dict()
    if with_contents:
        node_export["contents"] = await Content.find({"id": {"$in": [ content.id for content in node.contents ]}})
    if with_other_contents:
        node_export["other_contents"] = await Content.find({"id": {"$nin": [ content.id for content in node.contents ]}})
    return node_export


@router.post("/edit", dependencies=[Depends(admin_only)])
async def edit_node(find: NodeFind, data: NodeEdit):
    return await Node.find_one_and_set(find=find.dict(exclude_unset=True), data=data.dict(exclude_unset=True))


@router.post("/add", dependencies=[Depends(admin_only)])
async def add_node(data: NodeAdd):
    return await Node.insert_one(data=data.dict(exclude_unset=True))


@router.post("/delete", dependencies=[Depends(admin_only)])
async def delete_node(find: NodeFind):
    return await Node.delete_one(find=find.dict(exclude_unset=True))

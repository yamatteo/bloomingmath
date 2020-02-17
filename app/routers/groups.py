
from fastapi import APIRouter, Form, Depends, HTTPException, Body

from routers import get_current_user, admin_only
from models import User, Group, List, Optional

#
router = APIRouter()
#

@router.post("/push_self")
async def push_self(group_id: str = Body(..., embed=True), current_user: User = Depends(get_current_user)):
    await Group.find_one_and_add_to_set(filter={"id": group_id}, push={"members": current_user.id})
    return False

@router.post("/pull_self")
async def pull_self(group_id: str = Body(..., embed=True), current_user: User = Depends(get_current_user)):
    await Group.find_one_and_pull(filter={"id": group_id}, pull={"members": current_user.id})
    return False

@router.post("/push_node")
async def push_self(group_id: str = Body(..., embed=True), node_id: str = Body(..., embed=True), admin: User = Depends(admin_only)):
    await Group.find_one_and_add_to_set(filter={"id": group_id}, push={"nodes": node_id})
    return False

@router.post("/pull_node")
async def pull_self(group_id: str = Body(..., embed=True), node_id: str = Body(..., embed=True), admin: User = Depends(admin_only)):
    await Group.find_one_and_pull(filter={"id": group_id}, pull={"node": node_id})
    return False

@router.get("/browse")
async def browse_groups():
    return [group.dict() for group in await Group.find({})]

@router.get("/read")
async def read_group(group_id: str):
    return await Group.find_one({"id": group_id})

@router.post("/edit")
async def edit_group(group_id: str = Body(..., embed=True), short: Optional[str] = Body(None, embed=True), long: Optional[str] = Body(None, embed=True), members: Optional[List[str]] = Body(None, embed=True), admin_only: bool = Depends(admin_only)):
    set = {}
    if short is not None:
        set["short"] = short
    if long is not None:
        set["long"] = long
    if members is not None:
        set["members"] = members
    return await Group.find_one_and_set(filter={"id": group_id}, set=set)

@router.post("/add")
async def add_group(short: str, long: str, admin_only: bool = Depends(admin_only)):
    return await Group.insert_one({"short": short, "long": long})

@router.post("/delete")
async def delete_group(group_id: str, admin_only: bool = Depends(admin_only),):
    return await Group.delete_one({"id": group_id})
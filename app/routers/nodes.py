from fastapi import APIRouter, Form, Depends, HTTPException, Body

from routers import get_current_user, admin_only
from models import User, Node, Group, Optional

#
router = APIRouter()


#
@router.get("/current")
async def current_nodes(current_user : User = Depends(get_current_user)):
    groups = await Group.find({"members": current_user.id})
    print("Current nodes > groups", groups)
    nodes_id = [ node_id for group in groups for node_id in group.nodes ]
    print("Current nodes > nodes_id", nodes_id)
    return [ node.dict() for node in await Node.find({"id": {"$in":nodes_id}})]

@router.get("/browse")
async def browse_nodes():
    return [node.dict() for node in await Node.find({})]


@router.get("/read")
async def read_node(node_id: str):
    return await Node.find_one({"id": node_id})


@router.post("/add")
async def add_node(short: str, long: Optional[str] = "", admin_only: bool = Depends(admin_only)):
    return await Node.insert_one({"short": short, "long": long})


@router.post("/edit")
async def edit_node(node_id: str, short: Optional[str] = None, long: Optional[str] = None, admin_only: bool = Depends(admin_only)):
    set = {}
    if short is not None:
        set["short"] = short
    if long is not None:
        set["long"] = long
    return await Node.find_one_and_set(filter={"id": node_id}, set=set)


@router.post("/delete")
async def delete_node(node_id: str, admin_only: bool = Depends(admin_only), ):
    return await Node.delete_one({"id": node_id})

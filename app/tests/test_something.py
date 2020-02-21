from json import dumps, loads

from bson import ObjectId
from pytest import mark

from routers import users


# setup is a package fixture defined in conftest.py


@mark.asyncio
async def test_admin_create_group(setup):
    """Proves that can login and use admin api.

    All api uses application/json body and not urlencode, except for login.
    """
    me, app, client, admin_log, user_log, logout = setup

    admin_log()
    res = client.post("/groups/add", data=dumps({"short": "New group 34", "long": "Detailed description of group 34."}))
    assert ObjectId.is_valid(loads(res.text)["id"])

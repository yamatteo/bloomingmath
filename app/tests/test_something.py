from json import dumps, loads

from bson import ObjectId
from pytest import mark

from models import User


# setup is a package fixture defined in conftest.py


@mark.asyncio
async def ntest_admin_create_group(setup):
    """Proves that can login and use admin api.

    All api uses application/json body and not urlencode, except for login.
    """
    me, app, client, admin_log, user_log, logout = setup

    admin_log()
    res = client.post("/groups/add", data=dumps({"short": "New group 34", "long": "Detailed description of group 34."}))
    assert ObjectId.is_valid(loads(res.text)["id"])


@mark.asyncio
async def test_users_rest(setup):
    me, app, client, admin_log, user_log, logout = setup

    admin_log()
    res = client.get("/users/browse")
    data = loads(res.text)
    assert len(data) == 2
    assert User.parse_obj(data[0])

    res = client.post("/users/add", data=dumps({"email": "other@example.com", "password": "pass", "is_blocked": True}))
    data = loads(res.text)
    assert User.parse_obj(data)
    assert len(await User.find()) == 3

    res = client.post("/users/read", data=dumps({"email": "other@example.com"}))
    data = loads(res.text)
    assert data["email"] == "other@example.com"
    assert User.parse_obj(data)

    res = client.post("/users/edit", data=dumps(
        {"find": {"email": "other@example.com"}, "data": {"password": "0000", "is_blocked": False}}))
    data = loads(res.text)
    u = User.parse_obj(data)
    assert u.is_blocked is False
    res = client.post("/users/login", data=dumps({"email": "other@example.com", "password": "pass"}))
    assert res.status_code == 401
    res = client.post("/users/login", data=dumps({"email": "other@example.com", "password": "0000"}))
    data = loads(res.text)
    assert "access_token" in data.keys()
    client.post("/users/delete", data=dumps({"email": "other@example.com"}))

    assert len(await User.find()) == 2


@mark.asyncio
async def test_user_routine(setup):
    me, app, client, admin_log, user_log, logout = setup

    logout()
    res = client.post("/users/login", data=dumps({"email": "user@example.com", "password": "0000"}))
    assert res.status_code == 401
    res = client.post("/users/login", data=dumps({"email": "user@example.com", "password": "pass"}))
    assert res.status_code == 200
    data = loads(res.text)
    assert "access_token" in data

    user_log()
    res = client.get("/users/current")
    data = loads(res.text)
    assert "nodes" in data.keys()
    print(data)


@mark.asyncio
async def test_contents_rest(setup):
    me, app, client, admin_log, user_log, logout = setup

    admin_log()
    res = client.post("/contents/browse")
    data = loads(res.text)
    assert isinstance(data, list)
    assert len(data) == 1

    with open("tests/example.pdf", "rb") as f:
        data = {"short": "An other example of pdf.", "filetype": "pdf",
                "long": "This is an optional description that can be added to any file to help users."}
        res = client.post("/contents/add", files={"content": f}, data=data)
        data = loads(res.text)
        assert data["id"] != "000000000000000000000000"
        assert data["original_filename"] == "example.pdf"

    res = client.post("/contents/read", data=dumps({"filetype": "pdf", "short": "An other example of pdf."}))
    data = loads(res.text)
    assert data["long"] == "This is an optional description that can be added to any file to help users."

    res = client.post("/contents/read", data=dumps({"filetype": "mp3"}))
    assert loads(res.text) is None

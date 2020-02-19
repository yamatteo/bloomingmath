from pytest import mark


@mark.asyncio
async def test_admin_create_group(setup):
    me, app, client, admin_log, user_log, logout = setup
    from routers import users
    app.include_router(users.router, prefix="/users", tags=["users"])

    from json import dumps
    # admin_log()
    res = client.get("/users/current")
    print(res.text)
    res = client.post("/users/urlencode_login", data={"username": "admin@example.com", "password": "pass"})
    # res = client.post("/users/login", data=dumps({"email": "admin@example.com", "password": "pass"}))

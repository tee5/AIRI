#!/usr/bin/env python
# coding: utf-8

import os
import requests
import responder
import airi_client

address = os.environ["API_ADDRESS"]
port = int(os.environ["API_PORT"])
client = airi_client.AiriClient(address, port)

api = responder.API(secret_key=os.environ["SECRET_KEY"])


@api.route(before_request=True)
def prepare_response(req, resp):
    print(f"start [app] prepare_response: req.session={req.session}, resp.session={resp.session}, cookie={req.cookies}")
    
    if "empno" in req.session:
        pass
    elif req.url.path == "/login":
        pass
    else:
        api.redirect(resp=resp, location="/login")

@api.route("/")
def root(req, resp):
    print(f"start [app] root: session={req.session}, cookie={req.cookies}")
    # if "empno" in req.session and req.session["empno"] != "":
    #     api.redirect(resp=resp, location="/users")
    # else:
    #     api.redirect(resp=resp, location="/login")
    api.redirect(resp=resp, location="/users")

@api.route("/users")
def users(req, resp):
    print(f"start [app] users: session={req.session}, cookie={req.cookies}")
    # if "empno" not in req.session or req.session["empno"] == "":
    #     api.redirect(resp=resp, location="/login")
    users = client.get_users()
    current_user = client.get_user(req.session["empno"])
    resp.html = api.template("users.html", session=resp.session, current_user=current_user, users=users)

@api.route("/user/{empno}/browse")
def browse_user(req, resp, *, empno):
    print(f"start [app] browse_user: session={req.session}, cookie={req.cookies}")
    # if "empno" not in req.session or req.session["empno"] == "":
    #     api.redirect(resp=resp, location="/login")
    user = client.get_user(empno)
    resp.html = api.template("browse_user.html", session=resp.session, user=user)

@api.route("/login")
async def login(req, resp):
    print(f"start [app] login: session={req.session}, cookie={req.cookies}")
    # if "empno" in req.session and req.session["empno"] != "":
    #     api.redirect(resp=resp, location="/users")

    print("before:", resp.session)
    resp.session = {}
    print("after:", resp.session)

    print("req.method:", req.method)
    if req.method == "post":
        data = await req.media()
        empno = "" if "empno" not in data else data["empno"]
        password = "" if "password" not in data else data["password"]

        r = client.login(empno, password)
        print(r)
        if r["success"]:
            resp.session["empno"] = empno
            api.redirect(resp=resp, location="/users")
        else:
            resp.html = api.template("login.html", message="社員番号かパスワードが間違ってる")
    else:
        resp.html = api.template("login.html")

@api.route("/logout")
def logout(req, resp):
    print(f"start [app] logout: session={req.session}, cookie={req.cookies}")
    print("before:", resp.session)
    resp.session = {}
    print("after:", resp.session)
    resp.html = api.template("logout.html")
    


if __name__ == "__main__":
    param = {
        "address": os.environ["APP_ADDRESS"],
        "port": int(os.environ["APP_PORT"]),
        "debug": bool(os.environ["APP_DEBUG"])
    }
    api.run(**param)

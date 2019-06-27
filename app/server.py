#!/usr/bin/env python
# coding: utf-8

import os
import requests
import responder
import airi_client

address = os.environ["API_ADDRESS"]
port = int(os.environ["API_PORT"])
client = airi_client.AiriClient(address, port)

api = responder.API(
    secret_key=os.environ["SECRET_KEY"],
    static_dir="static",
    static_route="/static"
)

def auth(empno, password):
    users = client.get_users()

@api.route(before_request=True)
def prepare_response(req, resp):
    print("start prepare_response:", req.session)

@api.route("/")
def root(req, resp):
    if "empno" in req.session and req.session["empno"] != "":
        api.redirect(resp=resp, location="/users")
    else:
        api.redirect(resp=resp, location="/login")

@api.route("/users")
def users(req, resp):
    if "empno" not in req.session or req.session["empno"] == "":
        api.redirect(resp=resp, location="/login")
    users = client.get_users()
    resp.html = api.template("users.html", users=users)

@api.route("/user/{empno}/browse")
def browse_user(req, resp, *, empno):
    print("start app browse_user:")
    if "empno" not in req.session or req.session["empno"] == "":
        api.redirect(resp=resp, location="/login")
    user = client.get_user(empno)
    resp.html = api.template("browse_user.html", user=user)

@api.route("/login")
async def login(req, resp):
    print("start login:")
    if "empno" in req.session and req.session["empno"] != "":
        api.redirect(resp=resp, location="/users")

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
    print("start app logout:")
    resp.session["empno"] = ""
    resp.cookies["Responder-Session"] = ""
    api.redirect(resp=resp, location="/login")


if __name__ == "__main__":
    param = {
        "address": os.environ["APP_ADDRESS"],
        "port": int(os.environ["APP_PORT"]),
        "debug": bool(os.environ["APP_DEBUG"])
    }
    api.run(**param)

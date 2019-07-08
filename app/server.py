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
async def prepare_response(req, resp):
    print(f"start [app] prepare_response: req.session={req.session}, resp.session={resp.session}, cookie={req.cookies}")

    # ログイン状況に応じた制御
    print("path 1")
    if req.url.path == "/login":
        # loginページへのアクセスはログイン必要なし
        print("path 2")
        return
    elif req.url.path == "/logout":
        # loginページへのアクセスはログイン必要なし
        print("path 3")
        return
    elif "empno" in req.session:
        print("path 4")
        if req.session["empno"] == "":
            # empno が "" か None なら要ログイン
            print("path 4.1")
            await api.redirect(resp=resp, location="/login")
            print("path 4.2")
            return
        else:
            print("path 4.3")
            return
    else:
        # それ以外はloginページへリダイレクト
        print("path 5")
        await api.redirect(resp=resp, location="/login")
        print("path 5.5")
    print("path 6")
@api.route("/")
def root(req, resp):
    print(f"start [app] root: session={req.session}, cookie={req.cookies}")
    api.redirect(resp=resp, location="/users")

@api.route("/users")
def users(req, resp):
    print(f"start [app] users: session={req.session}, cookie={req.cookies}")
    users = client.get_users()
    current_user = client.get_user(req.session["empno"])
    resp.html = api.template("users.html", session=resp.session, current_user=current_user, users=users)

@api.route("/user/browse/{empno}")
def browse_user(req, resp, *, empno):
    print(f"start [app] browse_user: session={req.session}, cookie={req.cookies}")
    user = client.get_user(empno)
    resp.html = api.template("browse_user.html", session=resp.session, user=user)

@api.route("/user/edit/{empno}")
async def edit_user(req, resp, *, empno):
    print(f"start [app] edit_user: session={req.session}, cookie={req.cookies}, method={req.method}")
    user = client.get_user(empno)
    print(f"user={user}")
    if req.method == "get":
        resp.html = api.template("edit_user.html", session=resp.session, user=user, message="")
    elif req.method == "post":
        data = await req.media()
        print(f"data={data}")
        
        data["empno"] = [user["empno"]]

        result = client.edit_user(data)

        if result:
            message = "OK"
        else:
            message = "NG"
        resp.html = api.template("edit_user.html", session=resp.session, user=user, message=message)
    else:
        resp.status_code = 400
        resp.redirect(resp=resp, location="/static/error/404.html")


@api.route("/user/create")
async def create_user(req, resp):
    print(f"start [app] create_user: session={req.session}, cookie={req.cookies}")
    if req.method == "get":
        resp.html = api.template("create_user.html", session=resp.session, message="")
    elif req.method == "post":
        data = await req.media()
        print(data["empno"])
        print(data["lastname_ja"])
        result = client.create_user(data)
        if result:
            message = "OK"
        else:
            message = "NG"
        resp.html = api.template("create_user.html", session=resp.session, message=message)
    else:
        resp.status_code = 400
        resp.redirect(resp=resp, location="/static/error/404.html")


@api.route("/login")
async def login(req, resp):
    print(f"start [app] login: req.session={req.session}, resp.session={resp.session}, cookie={req.cookies}")
    # session情報をクリア
    print("before:", req.session, resp.session)
    resp.session["empno"] = ""
    print("after:", req.session, resp.session)

    print("req.method:", req.method)
    if req.method == "post":
        # POSTリクエストの場合はPOSTデータを確認
        data = await req.media()
        empno = "" if "empno" not in data else data["empno"]
        password = "" if "password" not in data else data["password"]

        r = client.login(empno, password)
        print(r)
        if r["success"]:
            # 問題なければログインしてusersページへ
            resp.session["empno"] = empno
            api.redirect(resp=resp, location="/users")
        else:
            # 問題あればそれを通知
            resp.html = api.template("login.html", message="社員番号かパスワードが間違ってる")
    else:
        # GETリクエストの場合は普通にloginページへ
        resp.html = api.template("login.html")

@api.route("/logout")
def logout(req, resp):
    print(f"start [app] logout: req.session={req.session}, resp.session={resp.session}, cookie={req.cookies}")
    # セッション情報をクリア
    print("before:", req.session, resp.session)
    resp.session["empno"] = ""
    print("after:", req.session, resp.session)
    resp.html = api.template("logout.html")


if __name__ == "__main__":
    param = {
        "address": os.environ["APP_ADDRESS"],
        "port": int(os.environ["APP_PORT"]),
        "debug": bool(os.environ["APP_DEBUG"])
    }
    api.run(**param)

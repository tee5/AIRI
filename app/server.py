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
    
    # ログイン状況に応じた制御
    if "empno" in req.session:
        # session情報にempnoがログイン必要なし
        pass
    elif req.url.path == "/login":
        # loginページへのアクセスはログイン必要なし
        pass
    else:
        # それ以外はloginページへリダイレクト
        api.redirect(resp=resp, location="/login")

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

@api.route("/user/{empno}/browse")
def browse_user(req, resp, *, empno):
    print(f"start [app] browse_user: session={req.session}, cookie={req.cookies}")
    user = client.get_user(empno)
    resp.html = api.template("browse_user.html", session=resp.session, user=user)

@api.route("/login")
async def login(req, resp):
    print(f"start [app] login: session={req.session}, cookie={req.cookies}")
    # session情報をクリア
    resp.session = {}

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
    print(f"start [app] logout: session={req.session}, cookie={req.cookies}")
    # セッション情報をクリア
    resp.session = {}
    resp.html = api.template("logout.html")
    

if __name__ == "__main__":
    param = {
        "address": os.environ["APP_ADDRESS"],
        "port": int(os.environ["APP_PORT"]),
        "debug": bool(os.environ["APP_DEBUG"])
    }
    api.run(**param)

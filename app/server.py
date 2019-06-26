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
    static_dir='static',
    static_route='/static'
)

def auth(empno, password):
    users = client.get_users()

@api.route(before_request=True)
def prepare_response(req, resp):
    print("start prepare_response:", req.session)

@api.route("/")
def root(req, resp):
    if "empno" not in req.session:
        api.redirect(resp=resp, location='/login')
    else:
        api.redirect(resp=resp, location='/users')

@api.route("/users")
def users(req, resp):
    if "empno" not in req.session:
        api.redirect(resp=resp, location='/login')
    users = client.get_users()
    resp.html = api.template("users.html", users=users)


@api.route("/login")
def login(req, resp):
    resp.html = api.template("login.html")

@api.route("/logout")
def login(req, resp):
    resp.html = api.template("login.html")


if __name__ == "__main__":
    param = {
        "address": os.environ["APP_ADDRESS"],
        "port": int(os.environ["APP_PORT"]),
        "debug": bool(os.environ["APP_DEBUG"])
    }
    api.run(**param)

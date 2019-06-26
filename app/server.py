#!/usr/bin/env python
# coding: utf-8

import requests
import responder

api = responder.API()


@api.route(before_request=True)
def prepare_response(req, resp):
    print(req.session)

@api.route("/")
@api.route("/users")
def users(req, resp):
    if "empno" not in req.session:
        api.redirect(resp=resp, location='/login')
    resp.html = api.template("users.html")


@api.route("/login")
def login(req, resp):
    resp.session['empno'] = '0123'
    resp.html = api.template("login.html")


if __name__ == "__main__":
    api.run(port=8080, debug=True)

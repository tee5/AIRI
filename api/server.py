#!/usr/bin/env python
# coding: utf-8

import os
import json
import responder
from sqlalchemy import create_engine
from sqlalchemy import Column, Integer, String, text, DateTime
from sqlalchemy.sql.functions import current_timestamp
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm.exc import NoResultFound

from models import User

db_connect = os.environ["DB_CONNECT"]
db_encoding = os.environ["DB_ENCODING"]
db_echo = bool(os.environ["DB_ECHO"])
engine = create_engine(db_connect, encoding=db_encoding, echo=db_echo)
Session = sessionmaker(autocommit=False, autoflush=False, bind=engine)
#Session = sessionmaker(bind=engine)

api = responder.API()

@api.route("/users")
class UsersResource(object):
    def on_get(self, req, resp):
        resp.headers = {"Content-Type": "application/json; charset=utf-8"}
        session = Session()
        try:
            users = session.query(User).all()
            result = []
            for user in users:
                result.append(user.to_dict())
            resp.text = json.dumps(result, ensure_ascii=False, indent=4)
        except Exception as e:
            print(type(e), e)
            resp.status_code = 500

@api.route("/user/{empno}")
class UserResource(object):
    def on_get(self, req, resp, *, empno):
        print("start GET /user/{empno}", empno)
        resp.headers = {"Content-Type": "application/json; charset=utf-8"}
        session = Session()
        try:
            result = session.query(User).filter_by(empno=empno).one()
            resp.content = json.dumps(result.to_dict(), ensure_ascii=False, indent=4)
        except NoResultFound as e:
            resp.status_code = 404
        except Exception as e:
            resp.status_code = 500

    async def on_post(self, req, resp, *, empno):
        """ edit """
        print("start POST /user/{empno}", empno)
        resp.headers = {"Content-Type": "application/json; charset=utf-8"}
        data = await req.media()
        session = Session()
        user = session.query(User).filter_by(empno=empno).one()
        user.firstname_ja = data["firstname_ja"]
        user.lastname_ja = data["lastname_ja"]
        user.firstname_en = data["firstname_en"]
        user.lastname_en = data["lastname_en"]
        user.email = data["email"]
        user.admin = data["admin"]
        try:
            session.commit()
            resp.status_code = 200
        except Exception as e:
            resp.status_code = 500

    async def on_put(self, req, resp, *, empno):
        """ create """
        print("start PUT /user/{empno}", empno)
        resp.headers = {"Content-Type": "application/json; charset=utf-8"}
        data = await req.media()
        user = User()
        user.empno = empno
        user.password = data["password"]
        user.firstname_ja = data["firstname_ja"]
        user.lastname_ja = data["lastname_ja"]
        user.firstname_en = data["firstname_en"]
        user.lastname_en = data["lastname_en"]
        user.email = data["email"]
        user.admin = data["admin"]
        try:
            session = Session()
            session.add(user)
            session.commit()
            resp.status_code = 201
        except Exception as e:
            resp.status_code = 500


@api.route("/login")
class LoginResource(object):
    async def on_post(self, req, resp):
        print("start api login:")
        resp.headers = {"Content-Type": "application/json; charset=utf-8"}
        try:
            data = await req.media()
        except Exception as e:
            print("except:",type(e), e)
        print("data:", data)
        session = Session()

        try:
            user = session.query(User).filter_by(empno=data["empno"], password=data["password"]).one()
            print(user)
            resp.content = json.dumps({"success": 1}, ensure_ascii=False, indent=4)
        except NoResultFound as e:
            print("NoResultFound")
            resp.content = json.dumps({"success": 0}, ensure_ascii=False, indent=4)
        except Exception as e:
            resp.status_code = 500



if __name__ == "__main__":
    param = {
        "address": os.environ["API_ADDRESS"],
        "port": int(os.environ["API_PORT"]),
        "debug": bool(os.environ["API_DEBUG"])
    }
    api.run(**param)

#!/usr/bin/env python
# coding: utf-8

import os
import json
import responder
from sqlalchemy import create_engine
from sqlalchemy import Column, Integer, String, text, DateTime
from sqlalchemy.sql.functions import current_timestamp
from sqlalchemy.orm import sessionmaker

from models import User

db_connect = os.environ["db_connect"]
db_encoding = os.environ["db_encoding"]
db_echo = bool(os.environ["db_echo"])
engine = create_engine(db_connect, encoding=db_encoding, echo=db_echo)
Session = sessionmaker(bind=engine)

api = responder.API()


@api.route("/users")
def get_users(req, resp):
    resp.headers = {"Content-Type": "application/json; charset=utf-8"}

    session = Session()
    users = session.query(User).all()
    result = []
    for user in users:
        result.append(user.serialize)
    resp.content = json.dumps(result, ensure_ascii=False, indent=4)

@api.route("/user/{empno}")
def get_user(req, resp, *, empno):
    resp.headers = {"Content-Type": "application/json; charset=utf-8"}
    session = Session()
    result = session.query(User).filter_by(User.empno = empno).one()
    resp.content = json.dumps(result[0], ensure_ascii=False, indent=4)


if __name__ == "__main__":
    api.run(port=8080)

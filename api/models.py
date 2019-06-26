#!/usr/bin/env python
# coding: utf-8

import os
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, text, DateTime
from sqlalchemy.sql.functions import current_timestamp

Base = declarative_base()


class User(Base):
    __tablename__ = "user"
    empno = Column(String(4), primary_key=True, nullable=False)
    password = Column(String(255), primary_key=True, nullable=False)
    firstname_ja = Column(String(255), nullable=False)
    lastname_ja = Column(String(255), nullable=False)
    firstname_en = Column(String(255), nullable=False)
    lastname_en = Column(String(255), nullable=False)
    email = Column(String(255), nullable=False)
    created_at = Column(DateTime, nullable=False, server_default=current_timestamp())
    updated_at = Column(DateTime, nullable=False, server_default=current_timestamp())
    deleted = Column(Integer, nullable=False, server_default=text("0"))

    @property
    def serialize(self):
        return {
            "empno": self.empno,
            "firstname_ja": self.firstname_ja,
            "lastname_ja": self.lastname_ja,
            "firstname_en": self.firstname_en,
            "lastname_en": self.lastname_en,
            "email": self.email,
            "created_at": self.created_at.isoformat(),
            "updated_at": self.updated_at.isoformat(),
            "deleted": self.deleted,
        }

    def __repr__(self):
        return "<User(empno={empno}, password={password}, firstname_ja={firstname_ja}, lastname_ja={lastname_ja}, firstname_en={firstname_en}, lastname_en={lastname_en}, email={email}, created_at={created_at}, updated_at={updated_at}, deleted={deleted}>".format(
            empno=self.empno,
            password="****",
            firstname_ja=self.firstname_ja,
            lastname_ja=self.lastname_ja,
            firstname_en=self.firstname_en,
            lastname_en=self.lastname_en,
            email=self.email,
            created_at=self.created_at.isoformat(),
            updated_at=self.updated_at.isoformat(),
            deleted=self.deleted,
        )


db_connect = os.environ["db_connect"]
db_encoding = os.environ["db_encoding"]
db_echo = bool(os.environ["db_echo"])

engine = create_engine(db_connect, encoding=db_encoding, echo=db_echo)
Base.metadata.bind = engine
Base.metadata.create_all(engine)

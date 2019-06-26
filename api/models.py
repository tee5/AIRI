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
    empno = Column(String(4), primary_key=True, nullable=False, index=True, unique=True)
    password = Column(String(255), nullable=False)
    firstname_ja = Column(String(255), nullable=False)
    lastname_ja = Column(String(255), nullable=False)
    firstname_en = Column(String(255), nullable=False)
    lastname_en = Column(String(255), nullable=False)
    email = Column(String(255), nullable=False)
    created_at = Column(DateTime, nullable=False, server_default=current_timestamp())
    updated_at = Column(DateTime, nullable=False, server_default=current_timestamp())
    admin = Column(Integer, nullable=False, server_default=text("0"))
    deleted = Column(Integer, nullable=False, server_default=text("0"))

    def to_dict(self):
        """ cast to dict for json serialize.(ignore password)

        Returns:
            bool: casted dict
        """
        return {
            "empno": self.empno,
            # "password": self.password,
            "firstname_ja": self.firstname_ja,
            "lastname_ja": self.lastname_ja,
            "firstname_en": self.firstname_en,
            "lastname_en": self.lastname_en,
            "email": self.email,
            "created_at": self.created_at.isoformat(),
            "updated_at": self.updated_at.isoformat(),
            "admin": self.admin,
            "deleted": self.deleted
        }

    def __repr__(self):
        return "<User(empno={empno}, password={password}, firstname_ja={firstname_ja}, lastname_ja={lastname_ja}, firstname_en={firstname_en}, lastname_en={lastname_en}, email={email}, created_at={created_at}, updated_at={updated_at}, admin={admin}, deleted={deleted})>".format(
            empno=self.empno,
            password="****",
            firstname_ja=self.firstname_ja,
            lastname_ja=self.lastname_ja,
            firstname_en=self.firstname_en,
            lastname_en=self.lastname_en,
            email=self.email,
            created_at=self.created_at.isoformat(),
            updated_at=self.updated_at.isoformat(),
            admin=self.admin,
            deleted=self.deleted
        )

class Division(Base):
    __tablename__ = "division"
    division_id = Column(Integer, primary_key=True, nullable=False, unique=True, autoincrement=True)
    division_code = Column(String(16), nullable=False)
    division_name_ja = Column(String(80), nullable=False)
    division_name_en = Column(String(80), nullable=False)
    created_at = Column(DateTime, nullable=False, server_default=current_timestamp())
    updated_at = Column(DateTime, nullable=False, server_default=current_timestamp())
    deleted = Column(Integer, nullable=False, server_default=text("0"))

    def to_dict(self):
        """ cast to dict for json serialize.(ignore password)

        Returns:
            bool: casted dict
        """
        return {
            "division_id": self.division_id,
            "division_code": self.division_code,
            "division_name_ja": self.division_name_ja,
            "division_name_en": self.division_name_en,
            "created_at": self.created_at,
            "updated_at": self.updated_at,
            "deleted": self.deleted
        }

    def __repr__(self):
        return "<Division(division_id={division_id}, division_code={division_code}, division_name_ja={division_name_ja}, division_name_en={division_name_en}, created_at={created_at}, updated_at={updated_at}, deleted={deleted})>".format(
            division_id=self.division_id,
            division_code=self.division_code,
            division_name_ja=self.division_name_ja,
            division_name_en=self.division_name_en,
            created_at=self.created_at,
            updated_at=self.updated_at,
            deleted=self.deleted
        )


class UserDivision(Base):
    __tablename__ = "user_division"
    empno = Column(String(4), primary_key=True, nullable=False, index=True)
    division_id = Column(Integer, primary_key=True, nullable=False, index=True)
    admin = Column(Integer, nullable=False, server_default=text("0"))
    created_at = Column(DateTime, nullable=False, server_default=current_timestamp())
    updated_at = Column(DateTime, nullable=False, server_default=current_timestamp())
    deleted = Column(Integer, nullable=False, server_default=text("0"))

    def to_dict(self):
        """ cast to dict for json serialize.(ignore password)

        Returns:
            bool: casted dict
        """
        return {
            "empno": self.empno,
            "division_id": self.division_id,
            "admin": self.admin,
            "created_at": self.created_at,
            "updated_at": self.updated_at,
            "deleted": self.deleted
        }

    def __repr__(self):
        return "<UserDivision(empno={empno}, division_id={division_id}, admin={admin}, created_at={created_at}, updated_at={updated_at}, deleted={deleted})>".format(
            empno=self.empno,
            division_id=self.division_id,
            admin=self.admin,
            created_at=self.created_at,
            updated_at=self.updated_at,
            deleted=self.deleted
        )

db_connect = os.environ["DB_CONNECT"]
db_encoding = os.environ["DB_ENCODING"]
db_echo = bool(os.environ["DB_ECHO"])

engine = create_engine(db_connect, encoding=db_encoding, echo=db_echo)
Base.metadata.bind = engine
Base.metadata.create_all(engine)

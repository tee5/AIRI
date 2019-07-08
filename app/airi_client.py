#!/usr/bin/env python

import json
import requests

class AiriClient(object):
    def __init__(self, address, port):
        self.address = address
        self.port = port

    @property
    def base_path(self):
        return f"http://{self.address}:{self.port}"

    def get_users(self):
        resp = requests.get(self.base_path + "/users")
        return resp.json()

    def get_user(self, empno):
        resp = requests.get(self.base_path + "/user/" + empno)
        return resp.json()

    def create_user(self, data):
        empno = data["empno"]
        resp = requests.put(self.base_path + "/user/" + empno, data=data)
        return resp.status_code == 201

    def login(self, empno, password):
        print(empno, password)
        data = {
            "empno": empno,
            "password": password
        }
        print(data)
        r = requests.post(self.base_path + "/login", data=data)
        print(r)
        return r.json()


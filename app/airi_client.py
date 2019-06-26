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

        
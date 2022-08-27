import json
import os
import sys

def setup():
    dir_path = os.path.dirname(os.path.realpath(__file__))
    dir_path = dir_path.split("\\")[:-1]
    dir_path.append("DataBase")
    sys.path.append("\\".join(dir_path))

setup()

import DataBaseConnector


def read_config():
    dir_path = os.path.dirname(os.path.realpath(__file__))
    dir_path = dir_path.split("\\")[:-1]
    dir_path.append("Config")
    dir_path.append("config.json")
    address =  "\\".join(dir_path)

    with open(address) as d:
        dictData = json.load(d)
    return dictData

def check_username_password(username, password):
    inp = f"Select idusers FROM multivitamin.users WHERE password=\"{password}\" AND username=\"{username}\";"
    return DataBaseConnector.run_with_output(inp)[0][0]

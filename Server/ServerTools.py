import json
import os
import sys




def setup():
    '''add DataBse folder to the path so I can import its file'''
    dir_path = os.path.dirname(os.path.realpath(__file__))
    dir_path = dir_path.split("\\")[:-1]
    dir_path.append("DataBase")
    sys.path.append("\\".join(dir_path))

setup()

import DataBaseConnector


def read_config():
    '''read config file as json and return as a dict'''
    dir_path = os.path.dirname(os.path.realpath(__file__))
    dir_path = dir_path.split("\\")[:-1]
    dir_path.append("Config")
    dir_path.append("config.json")
    address =  "\\".join(dir_path)

    with open(address) as d:
        dictData = json.load(d)
    return dictData

def check_username_password(username, password):
    '''return id of there user with the username and password and if not raise an error '''
    inp = f"Select idusers FROM multivitamin.users WHERE password=\"{password}\" AND username=\"{username}\";"
    return DataBaseConnector.run_with_output(inp)[0][0]

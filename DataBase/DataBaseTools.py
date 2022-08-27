import json
import os


def read_config():
    dir_path = os.path.dirname(os.path.realpath(__file__))
    dir_path = dir_path.split("\\")[:-1]
    dir_path.append("Config")
    dir_path.append("config.json")
    address =  "\\".join(dir_path)

    with open(address) as d:
        dictData = json.load(d)
    return dictData
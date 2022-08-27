import requests
import ServerTools
import json
import sys
import os
import random

def setup():
    dir_path = os.path.dirname(os.path.realpath(__file__))
    dir_path = dir_path.split("\\")[:-1]
    dir_path.append("DataBase")
    sys.path.append("\\".join(dir_path))

setup()

import DataBaseConnector

config = ServerTools.read_config()

def get_the_question_structure(question_type):
    url = config["Printer_URL"]+"/structure"
    x = requests.get(url)
    return json.loads(x.text)[question_type]


def get_the_team_question(team_id):
    team_id = str(team_id)
    inp = f"Select idquestion FROM multivitamin.printed_questions WHERE idteam={team_id};"
    for i in DataBaseConnector.run_with_output(inp):
        yield i[0]

def check_rules(team_id):
    return len(list(get_the_team_question(team_id))) < int(config["Max_Question_team"])


def choose_question(team_id, question_type):
    if(not check_rules(team_id)):
        raise Exception
    
if __name__=="__main__":
    #print(get_the_question_structure("set3"))
    print(list(get_the_team_question(1001)))
    print(check_rules(1003))
    print(choose_question(1002, "set3"))

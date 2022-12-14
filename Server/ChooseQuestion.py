import requests
import ServerTools
import json
import sys
import os
import random
from datetime import datetime

def setup():
    '''add Database folder to the path to import its files'''
    dir_path = os.path.dirname(os.path.realpath(__file__))
    dir_path = dir_path.split("\\")[:-1]
    dir_path.append("DataBase")
    sys.path.append("\\".join(dir_path))

setup()

import DataBaseConnector

config = ServerTools.read_config()

def get_the_question_structure(question_type="?"):
    """make a request to the printer server and get the sturecture of the questions and return 
    the questions of the input type"""
    url = config["Printer_URL"]+"/structure"
    x = requests.get(url)
    if question_type == "?":
        return json.loads(x.text)
    return json.loads(x.text)[question_type]


def give_type(question_id):
    question_id = str(question_id)+'.pdf'
    for i in get_the_question_structure().items():
        if question_id in i[1]:
            return i[0]

def get_the_team_question(team_id):
    """return all the questions of the input team"""
    team_id = str(team_id)
    inp = f"Select idquestion FROM multivitamin.printed_questions WHERE idteam={team_id};"
    for i in DataBaseConnector.run_with_output(inp):
        yield i[0]

def get_the_team_question_in_hand(team_id):
    """return the questions of the input team that haven't gaved back"""
    team_id = str(team_id)
    inp = f"Select idquestion FROM multivitamin.printed_questions WHERE idteam={team_id} AND status=0;"
    for i in DataBaseConnector.run_with_output(inp):
        yield i[0]

def check_rules(team_id):
    """check if the team has less than max_question in hand"""
    return len(list(get_the_team_question_in_hand(team_id))) < int(config["Max_Question_team"])

def choose_question(team_id, question_type):
    """choose a question for a team from a certain type and return the question id"""
    choice = []
    for i in get_the_question_structure(question_type):
        choice.append(i[:-4])
    for i in get_the_team_question(team_id):
        i = str(i)
        if i in choice:
            choice.remove(i)
    return random.choice(choice)

def type_money(question_type):
    return int(question_type.split("#")[-1])

def team_money(team_id):
    inp = f"Select score FROM multivitamin.teams WHERE idteams={team_id};"
    return int(DataBaseConnector.run_with_output(inp)[0][0])

def team_name(team_id):
    inp = f"Select name FROM multivitamin.teams WHERE idteams={team_id};"
    return DataBaseConnector.run_with_output(inp)[0][0]

def give_question(team_id, question_type):
    if(not check_rules(team_id)):
        raise Exception
    question = choose_question(team_id, question_type)
    cost_score = int(type_money(question_type))    
    team_score = int(team_money(team_id))
    min_score = int(config["Min_Score"])

    if team_score - cost_score < min_score:
        raise Exception
    
    return question

def make_printer_request(team_id, question_type):
    question_number = give_question(team_id, question_type)
    req = dict()
    req["username"] = config["Printer_UserName"]
    req["password"] = config["Printer_Password"]
    req["question_address"] = "\\"+question_type +"\\" + str(question_number)+".pdf"
    req["question_code"] = str(question_number)
    req["major"] = str(question_type.split("#")[0])
    req["question_type"] = str(question_type.split("#")[1])
    req["recive_time"] = datetime.now().strftime("%H:%M:%S") 
    req["price"] = str(type_money(question_type))
    req["team_code"] = str(team_id)
    req["team_name"] = team_name(team_id)
    req["score"] = str(- int(type_money(question_type))+ int(team_money(team_id)))
    url = config["Printer_URL"]+"/print"
    x = requests.post(url, json= req)
    return json.loads(x.text), question_number
    

def make_printer_request_special(team_id, question_number, price):
    req = dict()
    question_type = give_type(question_number)
    
    req["username"] = config["Printer_UserName"]
    req["password"] = config["Printer_Password"]
    req["question_address"] = "\\"+question_type +"\\" + str(question_number)+".pdf"
    req["question_code"] = str(question_number)
    req["major"] = str(question_type.split("#")[0])
    req["question_type"] = str(question_type.split("#")[1])
    req["recive_time"] = datetime.now().strftime("%H:%M:%S") 
    req["price"] = str(price)
    req["team_code"] = str(team_id)
    req["team_name"] = team_name(team_id)
    req["score"] = str(- price+ int(team_money(team_id)))

    url = config["Printer_URL"]+"/print"
    x = requests.post(url, json= req)
    return json.loads(x.text), question_number
    
if __name__=="__main__":
    #print(get_the_question_structure("set3"))
    #print(list(get_the_team_question(1001)))
    #print(check_rules(1003))
    #print(give_question(1002, "set3"))
#    print(team_money(1001))    
#    print(give_question(1003, "set3#5"))
#    print(make_printer_request("1001", "set3#very_hard#5"))
#    print(team_name("1003"))
#    print(list(get_the_team_question_in_hand(1003)))
    print(give_type(22))
    pass


from flask import Flask,request ,jsonify
from flask_restful import reqparse, abort, Api, Resource
import ServerTools
import os
import sys 
from ChooseQuestion import make_printer_request, type_money
from datetime import datetime

def setup():
    dir_path = os.path.dirname(os.path.realpath(__file__))
    dir_path = dir_path.split("\\")[:-1]
    dir_path.append("DataBase")
    sys.path.append("\\".join(dir_path))

setup()

import DataBaseConnector


app = Flask(__name__)
api = Api(app)



class GiveQuestionToTeams(Resource):
    def post(self):
        data = request.get_json(force=True)
        try:
            user_id = ServerTools.check_username_password(data["username"], data["password"])
        except:
            return '{message: password is wronge}'
        try:
            response, question_id = make_printer_request(data["team_code"], data["question_type"])
            inp = f"INSERT INTO multivitamin.printed_questions (idteam, idquestion, iduser_give, time_give)  VALUES  ('{data['team_code']}','{question_id}', '{user_id}', '{datetime.now().strftime('%H:%M:%S') }');"
            DataBaseConnector.run_without_ouput(inp)
            inp = f"update multivitamin.teams set score=score-{type_money(data['question_type'])} where idteams={data['team_code']};"
            DataBaseConnector.run_without_ouput(inp)            
            return '{message: eveything is fine}'
        except:
            return '{message: error}'

class GetQuestionFromTeam(Resource):
    def post(self):
        data = request.get_json(force=True)
        try:
            user_id = ServerTools.check_username_password(data["username"], data["password"])
        except:
            return '{message: password is wronge}'

        try:
            inp = f"UPDATE `multivitamin`.`printed_questions` SET `iduser_get` = '{user_id}', `time_get` = '{datetime.now().strftime('%H:%M:%S')}', `status` = '1' WHERE (idteam={data['team_code']} AND idquestion={data['question_code']});"
            DataBaseConnector.run_without_ouput(inp)
            return '{message: eveything is fine}'
        except:
            return '{message: error}'


class PutScore(Resource):
    def post(self):
        data = request.get_json(force=True)
        try:
            user_id = ServerTools.check_username_password(data["username"], data["password"])
        except:
            return '{message: password is wronge}'

        try:
            inp = f"UPDATE `multivitamin`.`printed_questions` SET `iduser_score` = '{user_id}',status=2, `time_score` = '{datetime.now().strftime('%H:%M:%S')}', `score` = '{data['score']}' WHERE (idteam={data['team_code']} AND idquestion={data['question_code']} AND status=1);"
            x = DataBaseConnector.run_without_ouput(inp)
            if x>0:
                inp = f"update multivitamin.teams set score=score+{data['score']} where idteams={data['team_code']};"
                DataBaseConnector.run_without_ouput(inp)     
                return '{message: eveything is fine}'
            return '{message: nothing changed}'
        except:
            return '{message: error}'

api.add_resource(GiveQuestionToTeams, '/questions/give')
api.add_resource(GetQuestionFromTeam, '/questions/get')
api.add_resource(PutScore, '/questions/score')



if __name__ == '__main__':
    app.run(debug=True, port=3000)


"""
{
        "username": "admin",
        "password": "helloworld",
        "question_type": "set1",
        "team_code":"1008"
}
"""
from flask import Flask,request ,jsonify
from flask_restful import reqparse, abort, Api, Resource
from ChooseQuestion import choose_question , team_money
import ServerTools
import os
import sys 
from ChooseQuestion import make_printer_request, type_money, make_printer_request_special
from datetime import datetime
import socket


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
            temp = dict()
            temp["message"] = "password is wrong"
            return temp
        try:
            response, question_id = make_printer_request(data["team_code"], data["question_type"])
            inp = f"INSERT INTO multivitamin.printed_questions (idteam, idquestion, iduser_give, time_give)  VALUES  ('{data['team_code']}','{question_id}', '{user_id}', '{datetime.now().strftime('%H:%M:%S') }');"
            DataBaseConnector.run_without_ouput(inp)
            inp = f"update multivitamin.teams set score=score-{type_money(data['question_type'])} where idteams={data['team_code']};"
            DataBaseConnector.run_without_ouput(inp)  
            temp = dict()
            temp["message"] = "eveything is fine"
            return temp
        except:
            temp = dict()
            temp["message"] = "error"
            return temp

class GetQuestionFromTeam(Resource):
    def post(self):
        data = request.get_json(force=True)
        try:
            user_id = ServerTools.check_username_password(data["username"], data["password"])
        except:
            temp = dict()
            temp["message"] = "password is wrong"
            return temp

        try:
            inp = f"UPDATE `multivitamin`.`printed_questions` SET `iduser_get` = '{user_id}', `time_get` = '{datetime.now().strftime('%H:%M:%S')}', `status` = '1' WHERE (idteam={data['team_code']} AND idquestion={data['question_code']});"
            x = DataBaseConnector.run_without_ouput(inp)
            temp = dict()
            if x > 0:
                temp["message"] = "eveything is fine"
            else:
                temp["message"] = "nothing changed"

            return temp
        except:
            temp = dict()
            temp["message"] = "error"
            return temp

class PutScore(Resource):
    def post(self):
        data = request.get_json(force=True)
        try:
            user_id = ServerTools.check_username_password(data["username"], data["password"])
        except:
            temp = dict()
            temp["message"] = "password is wrong"
            return temp

        try:
            inp = f"UPDATE `multivitamin`.`printed_questions` SET `iduser_score` = '{user_id}',status=2, `time_score` = '{datetime.now().strftime('%H:%M:%S')}', `score` = '{data['score']}' WHERE (idteam={data['team_code']} AND idquestion={data['question_code']} AND status=1);"
            x = DataBaseConnector.run_without_ouput(inp)
            if x>0:
                inp = f"update multivitamin.teams set score=score+{data['score']} where idteams={data['team_code']};"
                DataBaseConnector.run_without_ouput(inp)     
                temp = dict()
                temp["message"] = "eveything is fine"
                return temp
            temp = dict()
            temp["message"] = "nothing changed"
            return temp
        except:
            temp = dict()
            temp["message"] = "error"
            return temp

class ScoreBoard(Resource):
    def get(self):
        inp = f"SELECT name, score FROM multivitamin.teams"
        ans = dict()
        for i in DataBaseConnector.run_with_output(inp):
            ans[i[0]] = i[1]
        return ans

class PasswordCheck(Resource):
    def post(self):
        data = request.get_json(force=True)
        try:
            user_id = ServerTools.check_username_password(data["username"], data["password"])
            temp = dict()
            temp["message"] = "password is correct"
            temp["status"] = "200"
            return temp
        except:
            temp = dict()
            temp["message"] = "password is wrong"
            temp["status"] = "400"
            return temp

class SellQuestion(Resource):
    def post(self):
        data = request.get_json(force=True)
        try:
            user_id = ServerTools.check_username_password(data["username"], data["password"])
        except:
            temp = dict()
            temp["message"] = "password is wrong"
            return temp

        try:
            inp = f"UPDATE `multivitamin`.`printed_questions` SET `iduser_get` = '{user_id}', `time_get` = '{datetime.now().strftime('%H:%M:%S')}', `status` = '1' WHERE (idteam={data['team_code']} AND idquestion={data['question_code']});"
            x = DataBaseConnector.run_without_ouput(inp)
            
            temp = dict()
            if x > 0:
                inp = f"INSERT INTO `multivitamin`.`auction` (`idteam_sell`, `idquestion`, `price`, `User_sell`) VALUES ({data['team_code']}, {data['question_code']}, {data['price']}, {user_id});"
                x = DataBaseConnector.run_without_ouput(inp)
                temp["message"] = "eveything is fine"
            else:
                temp["message"] = "nothing changed"

            return temp
        except:
            temp = dict()
            temp["message"] = "error"
            return temp    

class BuyQuestion(Resource):
   def post(self):
        data = request.get_json(force=True)
        try:
            user_id = ServerTools.check_username_password(data["username"], data["password"])
        except:
            temp = dict()
            temp["message"] = "password is wrong"
            return temp
        inp = f"SELECT * FROM multivitamin.auction WHERE idauction={data['idauction']} AND status=0"
        database = DataBaseConnector.run_with_output(inp)
        if len(database) < 1:
            temp = dict()
            temp["message"] = "nothing to buy"
            return temp
        database = database[0]
        if team_money(data["team_code"]) < database[3]:
            temp = dict()
            temp["message"] = "teams doesn't have enough money"
            return temp

        inp = f"SELECT * FROM multivitamin.printed_questions WHERE idteam={data['team_code']} AND idquestion={database[2]}"
        
        if len(DataBaseConnector.run_with_output(inp)) > 0:
            temp = dict()
            temp["message"] = "teams has got this question before"
            return temp

        inp = f"update multivitamin.teams set score=score-{database[3]} where idteams={data['team_code']};"
        DataBaseConnector.run_without_ouput(inp) 

        inp = f"INSERT INTO multivitamin.printed_questions (idteam, idquestion, iduser_give, time_give)  VALUES  ('{data['team_code']}','{database[2]}', '{user_id}', '{datetime.now().strftime('%H:%M:%S') }');"
        DataBaseConnector.run_without_ouput(inp)

        inp = f"UPDATE `multivitamin`.`auction` SET `idteam_buy` = {data['team_code']}, `User_buy` = {user_id}, `status` = '1' WHERE (`idauction` = {data['idauction']});"
        DataBaseConnector.run_without_ouput(inp)
        
        make_printer_request_special(data["team_code"], database[2], database[3])

        temp = dict()
        temp["message"] = "everything is ok"
        return temp

class AuctionBoard(Resource):
    def get(self):
        inp = f"SELECT * FROM multivitamin.auction WHERE status=0"
        ans = dict()
        for i in DataBaseConnector.run_with_output(inp):
            ans[i[2]] = i[3]
        return ans

api.add_resource(GiveQuestionToTeams, '/questions/give')
api.add_resource(GetQuestionFromTeam, '/questions/get')
api.add_resource(PutScore, '/questions/score')
api.add_resource(ScoreBoard, "/board/score")
api.add_resource(AuctionBoard, "/board/auction")
api.add_resource(PasswordCheck, "/user/input")
api.add_resource(SellQuestion, "/auction/get")
api.add_resource(BuyQuestion, "/auction/give")

if __name__ == '__main__':
    app.run(debug=True, port=3000, host=socket.gethostbyname_ex(socket.gethostname())[-1][-1])


"""
{
        "username": "admin",
        "password": "helloworld",
        "question_type": "set1",
        "team_code":"1008"
}
"""
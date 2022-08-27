from flask import Flask,request ,jsonify
from flask_restful import reqparse, abort, Api, Resource
import ChooseQuestion


app = Flask(__name__)
api = Api(app)


class GiveQuestionToTeams(Resource):
    def post(self):
        data = request.get_json(force=True)
        return "sad"


api.add_resource(GiveQuestionToTeams, '/questions/give')


if __name__ == '__main__':
    app.run(debug=True)

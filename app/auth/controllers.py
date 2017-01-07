from flask_restful import Resource


class Index(Resource):

    def get(self):
        return {"message": "Hello!!"}


class Register(Resource):

    def get(self):
        return {"message": "Kindly Register!"}

class Login(Resource):

    def get(self):
        return {"message": "Kindly Login!"}

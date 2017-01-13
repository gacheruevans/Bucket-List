import json
import jwt
from app import db
from app.auth.models import Users
from config import Config
from datetime import datetime, timedelta
from flask import jsonify, request
from flask_restful import Resource, abort


class Login(Resource):
    """
    This class contains the login function.
    """

    def get(self):
        return jsonify({"message": "Welcome to the BucketList API."
                        " Register a new user by sending a"
                        " POST request to /auth/register. "
                        "Login by sending a POST request to"
                        " /auth/login to get started."})

    def post(self):

        data = json.loads(request.get_data(as_text=True))
        if not data:
            abort(
                401,
                message="No params passed. Kindly fill\
                 you username and password")
        username = data['username']
        password = data['password']

        if not username or not password:
            abort(401,
                  message="Kindly fill in the missing details")

        user = Users.query.filter_by(username=username).first()
        if user is None:
            abort(400, message="User does not exist")
        if user.verify_password(password):
            payload = {
                'sub': user.id,
                'exp': datetime.utcnow() + timedelta(minutes=30)
            }
            token = jwt.encode(payload, Config.SECRET_KEY, algorithm='HS256')
            return jsonify({"message": "Welcome {}".format(user.username),
                            "token": token.decode('utf-8')})
        abort(401, message="Invalid password")


class Register(Resource):
    """
    This is the class for the registration resources.
    GET: Provides the registration instructions.
    POST: Adds a user o the database.
    """

    def get(self):
        return jsonify({"message": "To register,"
                        "send a POST request with username, password and email"
                        " to /auth/register."})

    def post(self):
        data = json.loads(request.get_data(as_text=True))
        if not data:
            abort(400,
                  message="No params passed. Kindly \
                  fill you username, email and password")
        if len(data.keys()) < 3:
            abort(400,
                  message="Ensure you provide a username, email and password")
        if not data['username'] or not data['email'] or not data['password']:
            abort(400,
                  message="Kindly fill in the missing details")

        username = data['username']
        email = data['email']
        password = data['password']

        if len(password) < 4:
            abort(400,
                  message="Password should be 4 or more characters")

        user = Users.query.filter_by(username=username).first()
        if user is not None:
            abort(400, message="User already exists")

        try:
            new_user = Users(
                username=username,
                email=email,
                password=password
            )
            db.session.add(new_user)
            db.session.commit()
            return {'message': "{} created successfully".format(username)}, 201
        except Exception:
            abort(500, message="User not created")

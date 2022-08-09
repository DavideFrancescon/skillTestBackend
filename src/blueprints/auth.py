from hashlib import algorithms_available
import json
from lib2to3.pgen2 import token
import secrets
from flask import Blueprint
from sqlalchemy import and_, bindparam, text
from src.database.models import User
from src.database import session
from flask import Flask, request, jsonify, make_response
import uuid  # for public id
from werkzeug.security import generate_password_hash, check_password_hash
# imports for PyJWT authentication
import jwt
from datetime import datetime, timedelta
from functools import wraps

from src.database.models.Color import Colors

auth_blueprint = Blueprint("auth", __name__)
SECRET_KEY = "testprova2"


def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None
        # jwt is passed in the request header
        print(request.headers)
        if 'x-access-token' in request.headers:
            token = request.headers['x-access-token']
        # return 401 if token is not passed
        if not token:
            return jsonify({'message': 'Token is missing'}), 401

        # decoding the payload to fetch the stored details
        data = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
        current_user = session.query(User).filter_by(
            public_id=data['public_id']).first()
        # returns the current logged in users contex to the routes
        return f(current_user, *args, **kwargs)

    return decorated


@auth_blueprint.route("/login", methods=["POST"])
def login():
    login_data = request.json
    if("email" in login_data and "password" in login_data):
        query = "select * from usertable JOIN colors on person = public_id where email = '%s'" % login_data["email"]
        user = session.execute(query).first()
        user_return = {}
        for item in user.keys():
            user_return[item] = user[item]

        if user is None:
            return make_response('wrong credentials 1', 401)

        if(check_password_hash(user.password, login_data["password"])):
            token = jwt.encode({
                'public_id': user.public_id,
                'exp': datetime.utcnow() + timedelta(days=30)
            }, SECRET_KEY, algorithm="HS256")
            return {'token': token, "user": user_return}, 201
        else:
            return make_response('wrong credentials 2 {} {}'.format(generate_password_hash(login_data["password"]), user.password), 401)
    else:
        return make_response('wrong credentials'), 401


@auth_blueprint.route('/signup', methods=['POST'])
def signup():
    login_data = request.json
    if(not ("name" in login_data and "password" in login_data and "email" in login_data)):
        return make_response("missing username, mail or password", 401)

    name, email = login_data['name'], login_data['email']
    password = login_data['password']
    user = session.query(User)\
        .filter_by(email=email)\
        .first()
    if not user:
        # database ORM object
        user = User(
            public_id=str(uuid.uuid4()),
            name=name,
            email=email,
            password=generate_password_hash(password)
        )
        # insert user
        session.add(user)
        session.commit()
        return make_response("user created successfully", 201)
    else:
        # returns 202 if user already exists
        return make_response('User already exists. Please Log in.', 202)

#  -*- coding: utf-8 -*-
from flask_restful import Resource, request
from flask_login import login_user, current_user
from flask import session
from . import api
from ..models.user import User

class Login(Resource):
    def post(self):
        signup_obj = request.get_json()
        user = User(signup_obj['username'])

        if not user.verify_password(signup_obj['password']):
            return_code = 401
            message = { 'status': 'failure', 'message': 'username doesn\'t exist or password incorrect.' }
        else:
            user.login()
            login_user(user, remember=True)
            return_code = 200
            message = { 'status': 'success', 'message': 'Successful login!'}

        return message, return_code

api.add_resource(Login, '/login')
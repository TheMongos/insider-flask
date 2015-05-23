from flask_restful import Resource, request
from flask_login import login_user, current_user
from . import api
from ..models.user import User

class Login(Resource):
    def post(self):
        signup_obj = request.get_json()
        user = User(signup_obj['username'])

        if not user.verify_password(signup_obj['password']):
            message = 'Invalid login.'
        else:
            user.login()
            login_user(user)
            message = 'Successful login'

        return message

api.add_resource(Login, '/login')
from flask_restful import Resource, request
from . import api
from ..models.user import User

class Signup(Resource):
    def post(self):
        signup_obj = request.get_json()
        signup_status = User(signup_obj['username']).register(signup_obj['password']
        									,signup_obj['email']
        									,signup_obj['first_name']
        									,signup_obj['last_name'])
        if signup_status == True:
        	return_code = 200
        	message = { 'status': 'success', 'message': 'User created successfully!'}
        else:
        	return_code = 409
        	message = { 'status': 'failure', 'message': 'username or email already exists.' }

        return message, return_code

api.add_resource(Signup, '/signup')
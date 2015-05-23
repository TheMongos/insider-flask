from flask_restful import Resource
from . import api

class Item(Resource):
    def get(self, item_id):
    	#TO-DO
        pass

    def post(self):
    	signup_obj = request.get_json()
        signup_status = User(signup_obj['username']).register(signup_obj['password']
        									,signup_obj['email']
        									,signup_obj['first_name']
        									,signup_obj['last_name'])
        return {'hello' : 'nurse'}

api.add_resource(Item, '/item/<int:item_id>', '/item')
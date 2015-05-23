from flask_restful import Resource
from . import api

class Category(Resource):
    def post(self):
    	#TO-DO
        pass

api.add_resource(Category, '/category')
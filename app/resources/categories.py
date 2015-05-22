from flask_restful import Resource
from . import api

class Category(Resource):
    def post(self):
        pass

api.add_resource(Category, '/category')